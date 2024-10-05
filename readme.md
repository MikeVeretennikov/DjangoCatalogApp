![pipeline](https://gitlab.crja72.ru/django/2024/autumn/course/students/169883-mishaveret-course-1187/badges/main/pipeline.svg)

# Commands to run the project for windows/unix 
 
## Create venv 
```bash
python -m venv venv
or
python3 -m venv venv
```

## Activate venv
```bash
source venv/Scripts/activate
or 
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
cp .env_template .env
```
### Create variables SECRET_KEY and DEBUG there



## Cd to lyceum/ and run server
```bash
cd lyceum

python3 manage.py runserver
```
