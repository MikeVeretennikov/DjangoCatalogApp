# Online catalog educational project on Django
![pipeline](https://gitlab.crja72.ru/django/2024/autumn/course/students/169883-mishaveret-course-1187/badges/main/pipeline.svg)

# Make sure you have these basic dependencies
* python >3.9

# Clone repository
```bash
git clone https://gitlab.crja72.ru/django/2024/autumn/course/students/169883-mishaveret-course-1187 repository
```

# Commands to run the project
 
## Create venv 
```bash
python3 -m venv venv
```

## Activate venv
```bash
source venv/bin/activate
```

## Install dependencies
### for prod mode
```bash
pip3 install -r requirements/prod.txt
```
### for dev mode
```bash
pip3 install -r requirements/dev.txt
```
### for test mode
```bash
pip3 install -r requirements/test.txt
```

## Create local .env file (copy the template file)
```bash
cp .env.example .env
```
### Create variables SECRET_KEY and DEBUG there



## Cd to working dir and run server
```bash
cd repository/lyceum/

python3 manage.py runserver
```

# Internalization 
### cd to root/lyceum and make locale dir
```bash
cd lyceum
mkdir locale
```
### make translation files for your languages specifying -l param
```bash
django-admin makemessages -l en
django-admin makemessages -l ru
```
### compile bin files for translation
```bash
django-admin compilemessages -l en
django-admin compilemessages -l ru
```
### in the created files django.po specify translation for tags "msgstr" 


# Database diagram
![ER diagram](https://gitlab.crja72.ru/django/2024/autumn/course/students/169883-mishaveret-course-1187/-/raw/main/ER.jpg?raw=True)
