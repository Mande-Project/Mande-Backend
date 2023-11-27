from django.test import TestCase, Client
from rest_framework.test import APIClient
from .models import Job, Service, Worker_Job

# Create your tests here.
class TestMandeApp(TestCase):
    def setUpTestData():
        Job.objects.create(name="Plomero")
        Job.objects.create(name="Electricista")
        Job.objects.create(name="Carpintero")
        Job.objects.create(name="Pintor")
        Job.objects.create(name="Construccion")
        Job.objects.create(name="Jardinero")

        c = Client()
        c.post('/api_users/users/', {
            "email":"samueltrujillo85@yopmail.com",
            "first_name":"Samuel",
            "last_name":"Trujillo",
            "username":"SamuelTrujillo10",
            "phone":"34573232113",
            "role": "customer",
            "password":"MandeSamuel2023",
            "re_password":"MandeSamuel2023",
            "address":"Calle 123 # 45-67, Cali, Colombia"
            })

        
        c.post('/api_users/users/', {
            "email":"manuelgalindo85@yopmail.com",
            "first_name":"Manuel",
            "last_name":"Galindo",
            "username":"ManuelGalindo10",
            "phone":"23421345262",
            "role": "customer",
            "password":"MandeManuel2023",
            "re_password":"MandeManuel2023",
            "address":"Carrera 60A # 11-15, Cali, Colombia"
            })
        
        c.post('/api_users/users/', {
            "email":"saralopez85@yopmail.com",
            "first_name":"Sara",
            "last_name":"Lopez",
            "username":"SaraLopez10",
            "phone":"23627324563",
            "role": "customer",
            "password":"MandeSara2023",
            "re_password":"MandeSara2023",
            "address":"Carrera 53A #5B-23, Cali, Colombia"
            })
        
        c.post('/api_users/users/', {
            "email":"santiagopaz85@yopmail.com",
            "first_name":"Santiago",
            "last_name":"Paz",
            "username":"SantiagoPaz10",
            "phone":"312234557324",
            "role": "worker",
            "password":"MandeSantiago2023",
            "re_password":"MandeSantiago2023",
            "address":"Carrera 17C #33C-38, Cali, Colombia"
            })
        
        c.post('/api_users/users/', {
            "email":"mariavargas85@yopmail.com",
            "first_name":"Maria",
            "last_name":"Vargas",
            "username":"MariaVargas10",
            "phone":"6253114543523",
            "role": "worker",
            "password":"MandeMaria2023",
            "re_password":"MandeMaria2023",
            "address":"Cra. 80 #11 A-51, Cali, Colombia"
            })
        
        c.post('/api_users/users/', {
            "email":"luisangulo85@yopmail.com",
            "first_name":"Luis",
            "last_name":"Angulo",
            "username":"LuisAngulo10",
            "phone":"8584111534512",
            "role": "worker",
            "password":"MandeLuis2023",
            "re_password":"MandeLuis2023",
            "address":"Calle 52 #3-29, Cali, Valle del Cauca"
            })

    def test_jobs(self):
        client = Client()   
        response = client.get('/mande_app/jobs/')

        assert len(response.data['data']) == 6
        assert response.data['data'][0]['name'] == 'Plomero'
        assert response.data['data'][2]['name'] == 'Carpintero'
        assert response.data['data'][5]['name'] == 'Jardinero'

    def test_select_job(self):
        client = Client()   
        response = client.post('/mande_app/worker_job/', {
            "id": 5,
            "job": 1,
            "price": 10000,
            "description": "Trabajo de plomeria"
            })
        
        assert response.content.decode() == "Job added to worker user with id 5"
        assert response.status_code == 200

    def test_client_select_job(self):
        client = Client()   
        response = client.post('/mande_app/worker_job/', {
            "id": 2,
            "job": 1,
            "price": 10000,
            "description": "Trabajo de plomeria"
            })

        assert response.content.decode() == "User is not a worker"
        assert response.status_code == 401

    def test_job_twice_added(self):
        client = Client()   
        client.post('/mande_app/worker_job/', {
            "id": 5,
            "job": 1,
            "price": 10000,
            "description": "Trabajo de plomeria"
            })
        
        response = client.post('/mande_app/worker_job/', {
            "id": 5,
            "job": 1,
            "price": 10000,
            "description": "Trabajo de plomeria"
            })
        
        assert response.content.decode() == "Job is already added"
        assert response.status_code == 401


    def test_job_deletion(self):
        client = Client()
        data={"id": 5, "job": 1}
        client.post('/mande_app/worker_job/', {
            "id": 5,
            "job": 1,
            "price": 10000,
            "description": "Trabajo de plomeria"
        })
        
        response = client.delete('/mande_app/worker_job/', data=data,content_type='application/json')

        assert response.status_code == 200

    def test_job_deletion_without_job(self):
        client = Client()
        data={"id": 5}
        response = client.delete('/mande_app/worker_job/', data=data,content_type='application/json')

        assert response.content.decode() == "No id of job provided"
        assert response.status_code == 401

    def test_job_deletion_user_not_related(self):
        client = Client()
        data={"id": 5, "job": 1}
        response = client.delete('/mande_app/worker_job/', data=data,content_type='application/json')

        assert response.content.decode() == "Worker is not related to the job"
        assert response.status_code == 401

    def test_job_search(self):
        client = APIClient()
        data={"id": 5, "job": 1}
        client.post('/mande_app/worker_job/', {
            "id": 5,
            "job": 1,
            "price": 10000,
            "description": "Trabajo de plomeria"
        })

        client.post('/mande_app/worker_job/', {
            "id": 6,
            "job": 2,
            "price": 20000,
            "description": "Montaje de lamparas"
        })

        client.post('/mande_app/worker_job/', {
            "id": 4,
            "job": 6,
            "price": 15000,
            "description": "Corte de cesped"
        })
        
        data = {"id": 2}
        response = client.get('/mande_app/worker_job/?id=1')

        assert response.status_code == 200
        assert len(response.data['data']) == 3        