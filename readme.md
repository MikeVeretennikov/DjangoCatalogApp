![pipeline](https://gitlab.crja72.ru/django/2024/autumn/course/students/169883-mishaveret-course-1187/badges/master/pipeline.svg)

# Commands to run the project for windows/unix 

## Create venv
```
python -m venv venv
or
python3 -m venv venv
```

## Activate venv
```
source venv/Scripts/activate
or 
source venv/bin/activate
```

## Install dependencies
### for prod mode
```
pip install -r requirements/prod.txt
or 
pip3 install -r requirements/prod.txt
```
### for dev mode
```
pip install -r requirements/dev.txt
or 
pip3 install -r requirements/dev.txt
```
### for test mode
```
pip install -r requirements/test.txt
or 
pip3 install -r requirements/test.txt
```

## Create local .env file (copy the template file)
```
cp .env_template .env
```
### Create variables SECRET_KEY and DEBUG there



## Cd to lyceum/ and run server
```
cd lyceum

python manage.py runserver
or 
python3 manage.py runserver
```
