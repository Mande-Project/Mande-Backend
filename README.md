# Mande-Backend
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

**Note**: If you get errors in the following steps, try deleting all migration files. Database schema is still being updated

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

## Running the dockerized application

**Get in the Dockerfile directory's level and put there the .env file**

**Then, run the following command to build the docker image**


```
docker image build -t mande_backend .
```

**Create a running docker container from the recently created image**

```
docker run -dit -p 8000:8000 mande_backend
```

**The last command will output the container's id**

**Now, run the following the command to start the application inside the running container replacing +container-id+ for the one you got**

```
docker exec -it +container-id+ sh runserver.sh
```

**That's it! The application should response in http://localhost:8000**
