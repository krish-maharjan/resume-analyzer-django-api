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

Url for the API [http://127.0.0.1:8000/api/resume/]

The request looks somthing like this:
![image](https://user-images.githubusercontent.com/99157652/233817830-7c07fdbb-5f94-47df-8fdd-30ea3ddfb4d8.png)

keywords must be comma seperated, rdoc is where you provide your files which can range from 1 to as many as you want.  

Now you're good to go and can use it in your project or with https://github.com/krishmzn/resume-analyzer-nextjs
