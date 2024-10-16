# Online catalog educational project on Django
![pipeline](https://gitlab.crja72.ru/django/2024/autumn/course/students/169883-mishaveret-course-1187/badges/main/pipeline.svg)

# Make sure you have these basic dependencies
* python >3.9

# Clone repository
```bash
git clone https://gitlab.crja72.ru/django/2024/autumn/course/students/169883-mishaveret-course-1187
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



## Cd to lyceum/ and run server
```bash
cd lyceum

python3 manage.py runserver
```



![ER diaram](https://gitlab.crja72.ru/django/2024/autumn/course/students/169883-mishaveret-course-1187/-/blob/main/ER.jpg?ref_type=heads)
