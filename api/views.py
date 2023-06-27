from rest_framework.response import Response
from api.models import Profile, File
from api.serializers import ProfileSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import status
# from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse


# For deleting files in media/rdocs
# import threading
# import shutil
import os
from django.conf import settings

# Creating CSV
import polars as pl
import random

# For analyzer
import PyPDF2
from collections import Counter
import re

from io import BytesIO 
from docx import Document


from rest_framework.permissions import BasePermission

class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
# Create your views here.
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            rdocs = []
            email = serializer.validated_data['email']
            keywords_received = serializer.validated_data['keywords_received']
            profile = Profile.objects.create(email=email, keywords_received=keywords_received)

            for rdoc in serializer.validated_data['rdoc']:
                file = File(profile=profile, rdoc=rdoc)
                file.save()
                rdocs.append(file.rdoc.name)        

            # -------Creating saving_keyword and file_list For calling analysis method
            # Saving_keywords to be accessed in analyze_pdf method
            saving_keywords = serializer.validated_data['keywords_received']
            file_list = serializer.validated_data['rdoc']
            # calling analysis method
            result = self.analyze_pdf(file_list, saving_keywords)
            

            # -------Creating file path for later on
            file_path = os.path.join(settings.MEDIA_ROOT, 'rdocs/', email)
            # print(file_path)

            # -------loop to seperate filenames from rdocs/{email}/filename.pdf
            rdocs_names = []
            for i in rdocs:
                i = i.split('/')
                j = i[-1]
                rdocs_names.append(j)
                # The actual seperation ends here

                # Next in the seme loop Delete files after certain time
                # t = threading.Timer(1, self.cleanup_folder, args=[file_path + '/' + j])
                # t.start()
                # print(j)

            # This would Deleting files in media/rdocs after analysis completed but no w we're using django.cleanup
            # for filename in rdocs:
            #     default_storage.delete(filename)

            # -------Creating df
            data = {'Candidate':rdocs_names, 'Profile_Match':result}
            df = pl.DataFrame(data) 
            # print(df)
            # Creating csv
            try:
                os.mkdir(file_path)
            except FileExistsError:
                # directory already exists
                pass
            
            while(True):
                try:
                    ran_num = str(random.randint(0,1000))
                    df.write_csv(file_path + '/' + ran_num + 'report.csv')
                    # print('csv created suscessfully')
                    break
                except FileExistsError:
                    continue

            filename = ran_num + 'report.csv'
            file_url = 'https://krishmaharjan.pythonanywhere.com/' + settings.MEDIA_URL + 'rdocs/' + email + '/' + filename
            
            # JSON response
            return Response({
                'msg': 'Resumes Analysed Successfully',
                'status': 'success',
                'email': email,
                'Resume Names': rdocs_names,
                'Match Percentage': result,
                'csv_file': file_url}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

    
    # def get(self, request, format=None):
    #     candidates = Profile.objects.all()
    #     serializer = ProfileSerializer(candidates, many=True)
    #     return Response({'msg': 'Resumes fetched Suscessfully', 'status':'suscess', 'candidates':serializer.data}, status=status.HTTP_200_OK)
    

    # Analysis Method

    

    def analyze_pdf(self, file_list, string_keys):
        keycheck = []
        results = []
        char = [',', '[', ']', '(', ')', '-', '_', '.']

        # Converting string of keys_received to list
        keys_received = string_keys.split(',' or ', ')

        # Converting key received to lowercase for analysis
        for key in keys_received:
            key = key.lower()
            key = key.strip()
            keycheck.append(key)

        # taking resumes and converting it to text
        results = []
        for file in file_list:
            if file.name.endswith('.pdf'):
                with file.open(mode='rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    num_pages = pdf_reader.getNumPages()
                    text = ''
                    for i in range(num_pages):
                        page = pdf_reader.getPage(i)
                        text += page.extractText()
            elif file.name.endswith('.docx'):
                with file.open(mode='rb') as f:
                    print(f)
                    # print(f.read())
                    
                    in_memory_file = BytesIO(f.read())
                    print(in_memory_file)
                    doc = Document(in_memory_file)
                    fullText = []
                    for para in doc.paragraphs:
                        fullText.append(para.text)
                    text = '\\n'.join(fullText)
            else:
                continue

            word_occurance = Counter(text.split()).most_common()
            analysis_list = []
            result = []
            cleaned_data = []

            for item in word_occurance:
                kwd = re.sub(r'\W+', '', item[0])
                count = item[1]
                cleaned_data.append((kwd, count))

            # converting tuple's first element to string and then list 
            for wd in cleaned_data:
                wd = str(wd[0])
                analysis_list.append(wd)

            # Analyzing words
            for i in keycheck:
                for word in analysis_list:
                    word = str(word)
                    word = word.lower()

                    # removing characters form string
                    for cr in char:
                        word = word.replace(str(cr), '')

                    # checking if the text in the words have keywords
                    if i == word:
                        result.append(i)
            result = list(set(result))

            no_of_kwds = len(keycheck)
            no_of_result = len(result)

            # By how much percent did the resume matched with the Keywords
            match_precent = (no_of_result/no_of_kwds)*100

            results.append(match_precent)
        return results


    
    # Cleanup Folder method used in post method
    # def cleanup_folder(self, folder_path):
    #     shutil.rmtree(folder_path)