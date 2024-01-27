# resume-analyzer-api

## Getting started

Install necessary packages for this api on through this command if not installed yet

```bash
pip install -r requirements.txt
```

Next, run environment firstly through this command

```bash
python manage.py runserver
```

First of all we need user auttoken for analyzing resume. Now, go to api/login put pusername and password OR if you don't have one yet create it from api/resume:
![image](https://github.com/krishmzn/resume-analyzer-django-api/assets/99157652/e7674d52-b77b-4fa1-8a7a-6f88461ff887)


Url for the API [http://127.0.0.1:8000/api/resume/]

The request looks somthing like this:
![image](https://github.com/krishmzn/resume-analyzer-django-api/assets/99157652/646c9f2e-afbb-4cba-b4dc-1e1752005c58)
![image](https://user-images.githubusercontent.com/99157652/233817830-7c07fdbb-5f94-47df-8fdd-30ea3ddfb4d8.png)

keywords must be comma seperated, rdoc is where you provide your files which can range from 1 to as many as you want.  

Now you're good to go and can use it in your project or with https://github.com/krishmzn/resume-analyzer-nextjs

[resume-analyzer-postman.webm](https://github.com/krishmzn/resume-analyzer-django-api/assets/99157652/70c91174-ed1f-483d-98d6-e3b029b93060)
