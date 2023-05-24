# Analysis Method
    def analyze_pdf(self, file_list, string_keys):
        
        keycheck = [ ]
        results = [ ]
        char = [',', '[', ']', '(', ')', '-', '_', '.']

        # Converting string of keys_received to list
        keys_received = string_keys.split(',' or ', ')
        
        # print(keys_received)

        # Converting key received to lowercase for analysis
        # print('__Converting key received to lowercase for analysis__')
        for key in keys_received:
            key = key.lower()
            key = key.strip()
            # print(key)
            keycheck.append(key)

        # taking tesumes and converting it to text
        results = []
        for file in file_list:
            with file.open(mode='rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                num_pages = pdf_reader.getNumPages()
                text = ''
                for i in range(num_pages):
                    page = pdf_reader.getPage(i)
                    text += page.extractText()
            word_occurance = Counter(text.split()).most_common()
                # results.append(text)
            analysis_list = [ ]
            result = [ ]
            cleaned_data = []

            # print(word_occurance)
            for item in word_occurance:
                kwd = re.sub(r'\W+', '', item[0])
                count = item[1]
                cleaned_data.append((kwd, count))

            # converting tuple's first element to string and then list 
            for wd in cleaned_data:
                wd = str(wd[0])
                analysis_list.append(wd)
                # print(wd)
            # print(analysis_list)


            # Analyzing words
            for i in keycheck:
                for word in analysis_list:
                    word = str(word)
                    word = word.lower()
                    # print(word)

                    # removing characters form string
                    for cr in char:
                        word = word.replace(str(cr), '')
                    # print(word)

                    # checking if the text in the words have keywords
                    if i == word:
                        result.append(i)
                        # print(i)
            result = list(set(result))
            # print(result)
            
            no_of_kwds = len(keycheck)
            no_of_result = len(result)
            # print(no_of_kwds, no_of_result)

            # By how much percent did the resume matched with the Keywords
            match_precent = (no_of_result/no_of_kwds)*100

            # print(match_precent)
            results.append(match_precent)
        return results
    
    # Cleanup Folder method used in post method
    def cleanup_folder(self, folder_path):
        shutil.rmtree(folder_path)