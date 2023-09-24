# Mande-Bakend
Repository of Mande Backend Project

## Setting up Django environment

**Create virtual environment for Django**

```
virtualenv venv
```

**Activate the virtual environment**

Linux:
```
source venv/bin/activate
```

Windows:
```
.\venv\Scripts\activate
```

**Install project dependencies**
```
pip install -r requirements.txt
```

**Create and migrate schema data in database**
```
python manage.py makemigrations

python manage.py migrate

```

**Test application**

```
python manage.py runserver
```

**To open django application in web browser, go to http://localhost:8000/**

## Testing

**Open examples/requests.sh for examples**
