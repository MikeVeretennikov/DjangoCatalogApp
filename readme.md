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
```
pip install -r requirements.txt
or 
pip3 install -r requirements.txt
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
