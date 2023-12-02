from django.test import TestCase, Client
from rest_framework.test import APIClient
from users.models import Worker
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
        
        c.post('/mande_app/worker_job/', {
            "id_user": 6,
            "id_job": 2,
            "price": 20000,
            "description": "Montaje de lamparas"
        })

        c.post('/mande_app/worker_job/', {
            "id_user": 4,
            "id_job": 6,
            "price": 15000,
            "description": "Corte de cesped"
        })

        c.post('/mande_app/worker_job/', {
            "id_user": 6,
            "id_job": 4,
            "price": 200000,
            "description": "Figuras abstractas"
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
            "id_user": 5,
            "id_job": 1,
            "price": 10000,
            "description": "Trabajo de plomeria"
            })
        
        assert response.content.decode() == "Job added to worker user with id 5"
        assert response.status_code == 200

    def test_client_select_job(self):
        client = Client()   
        response = client.post('/mande_app/worker_job/', {
            "id_user": 2,
            "id_job": 1,
            "price": 10000,
            "description": "Trabajo de plomeria"
            })

        assert response.content.decode() == "User is not a worker"
        assert response.status_code == 401

    def test_job_twice_added(self):
        client = Client()   
        client.post('/mande_app/worker_job/', {
            "id_user": 5,
            "id_job": 1,
            "price": 10000,
            "description": "Trabajo de plomeria"
            })
        
        response = client.post('/mande_app/worker_job/', {
            "id_user": 5,
            "id_job": 1,
            "price": 10000,
            "description": "Trabajo de plomeria"
            })
        
        assert response.content.decode() == "Job is already added"
        assert response.status_code == 401


    def test_job_deletion(self):
        client = Client()
    
        client.post('/mande_app/worker_job/', {
            "id_user": 5,
            "id_job": 1,
            "price": 10000,
            "description": "Trabajo de plomeria"
        })

        data={"id_user": 5, "id_job": 1}    
        response = client.delete('/mande_app/worker_job/', data=data,content_type='application/json')

        assert response.content.decode() == "Job set inactive to worker user with id 5"
        assert Worker_Job.objects.get(worker=Worker.objects.get(user=5),job=Job.objects.get(id=1)).active == False
        assert response.status_code == 200

    def test_job_deletion_without_job(self):
        client = Client()
        data={"id_user": 5}
        response = client.delete('/mande_app/worker_job/', data=data,content_type='application/json')

        assert response.content.decode() == "No id of job provided"
        assert response.status_code == 401

    def test_job_deletion_user_not_related(self):
        client = Client()
        data={"id_user": 5, "id_job": 1}
        response = client.delete('/mande_app/worker_job/', data=data,content_type='application/json')

        assert response.content.decode() == "Worker is not related to the job"
        assert response.status_code == 401

    def test_job_search(self):
        client = APIClient()
        response = client.get('/mande_app/worker_job/?id_user=1')

        assert response.status_code == 200
        assert len(response.data['data']) == 3   

    def test_job_search_inactive(self):
        client = APIClient()

        for wj in Worker_Job.objects.all():
            wj.active = False
            wj.save()

        response = client.get('/mande_app/worker_job/?id_user=1')

        assert response.status_code == 200
        assert len(response.data['data']) == 0

    def test_job_reactivation(self):
        client = Client()

        data={"id_user": 6, "id_job": 2}    
        response = client.delete('/mande_app/worker_job/', data=data,content_type='application/json')

        assert response.content.decode() == "Job set inactive to worker user with id 6"
        assert Worker_Job.objects.get(worker=Worker.objects.get(user=6),job=Job.objects.get(id=2)).active == False
        assert response.status_code == 200
        
        response = client.post('/mande_app/worker_job/', {
            "id_user": 6,
            "id_job": 2,
            "price": 25000,
            "description": "Montaje de lamparas grandes"
        })  

        worker_job = Worker_Job.objects.get(worker=Worker.objects.get(user=6),job=Job.objects.get(id=2))

        assert response.content.decode() == "Job updated and set active to worker user with id 6"
        assert worker_job.active == True
        assert worker_job.price == 25000
        assert worker_job.description == "Montaje de lamparas grandes"
        assert response.status_code == 200

    def test_service_creation(self):
        client = Client()

        data = {
            "id_user": 2,
            "id_worker_job": 1,
            "hours": 2,
            "description": "Instalacion de lamparas en el baño"
        }

        response = client.post('/mande_app/services/', data=data)

        assert response.status_code == 200
        assert response.content.decode() == "Service requested by customer 2 created, job:Electricista"
        assert len(Service.objects.all()) == 1
        assert Worker.objects.get(user=6).is_available == False 

    def test_service_creation_worker_not_available(self):
        client = Client()

        data = {
            "id_user": 2,
            "id_worker_job": 1,
            "hours": 6,
            "description": "Instalacion de lamparas en jardin"
        }
        client.post('/mande_app/services/', data=data)

        data = {
            "id_user": 2,
            "id_worker_job": 1,
            "hours": 2,
            "description": "Instalacion de lamparas en el baño"
        }

        response = client.post('/mande_app/services/', data=data)

        assert response.status_code == 401
        assert response.content.decode() == "Worker is not available"

    def test_service_end(self):
        client = Client()

        data = {
            "id_user": 2,
            "id_worker_job": 1,
            "hours": 2,
            "description": "Instalacion de lamparas en el baño"
        }

        client.post('/mande_app/services/', data=data)

        data = {
            "id_service": 1,
            "rating": 4.2
        }

        response = client.patch('/mande_app/services/', data=data, content_type='application/json')

        assert response.status_code == 200
        assert response.content.decode() == "Service with id 1 updated"
        assert Service.objects.get(id=1).status == 'F'
        assert Service.objects.get(id=1).rating == 4.2
        assert Worker.objects.get(user=6).is_available == True
    
    def test_service_end_twice(self):
        client = Client()

        data = {
            "id_user": 2,
            "id_worker_job": 1,
            "hours": 2,
            "description": "Instalacion de lamparas en el baño"
        }

        client.post('/mande_app/services/', data=data)

        data = {
            "id_service": 1,
            "rating": 4.2
        }

        client.patch('/mande_app/services/', data=data, content_type='application/json')

        data = {
            "id_service": 1,
            "rating": 4.2
        }

        response = client.patch('/mande_app/services/', data=data, content_type='application/json')

        assert response.status_code == 401
        assert response.content.decode() == "Service already ended or canceled"

    def test_worker_rating_update(self):
        client = Client()

        #Service 1
        data_s_1 = {
            "id_user": 2,
            "id_worker_job": 1,
            "hours": 2,
            "description": "Instalacion de lamparas en el baño"
        }

        client.post('/mande_app/services/', data=data_s_1)

        data_e_1 = {"id_service": 1,"rating": 4.2}
        client.patch('/mande_app/services/', data=data_e_1, content_type='application/json')

        assert Worker.objects.get(user=6).rating == 4.2

        #Service 2
        data_s_2 = {
            "id_user": 1,
            "id_worker_job": 1,
            "hours": 2,
            "description": "Instalacion de lamparas en el baño"
        }

        client.post('/mande_app/services/', data=data_s_2)

        data_e_2 = {"id_service": 2,"rating": 3}
        client.patch('/mande_app/services/', data=data_e_2, content_type='application/json')

        assert Worker.objects.get(user=6).rating == (4.2+3)/2

        #Service 3
        data_s_3 = {
            "id_user": 1,
            "id_worker_job": 1,
            "hours": 2,
            "description": "Ciudad Moderna"
        }

        client.post('/mande_app/services/', data=data_s_3)

        data_e_3 = {"id_service": 3,"rating": 5}
        client.patch('/mande_app/services/', data=data_e_3, content_type='application/json')

        assert Worker.objects.get(user=6).rating == (5+3+4.2)/3

    def test_service_get(self):
        client = Client()

        #Service 1
        data_s_1 = {
            "id_user": 2,
            "id_worker_job": 1,
            "hours": 2,
            "description": "Instalacion de lamparas en el baño"
        }

        client.post('/mande_app/services/', data=data_s_1)
        client.patch('/mande_app/services/', data={"id_service": 1,"rating": 4.2}, content_type='application/json')

        #Service 2
        data_s_2 = {
            "id_user": 1,
            "id_worker_job": 1,
            "hours": 2,
            "description": "Instalacion de lamparas en el baño"
        }

        client.post('/mande_app/services/', data=data_s_2)

        #Service 3
        data_s_3 = {
            "id_user": 1,
            "id_worker_job": 2,
            "hours": 2,
            "description": "N/A"
        }

        client.post('/mande_app/services/', data=data_s_3)

        client = APIClient()
        response = client.get('/mande_app/services/?id_user=1',content_type='application/json')
        
        assert len(response.data['data']) == 2
        assert response.status_code == 200

        client = APIClient()
        response = client.get('/mande_app/services/?id_user=2',content_type='application/json')
        assert len(response.data['data']) == 1
        assert response.status_code == 200

        client = APIClient()
        response = client.get('/mande_app/services/?id_user=6',content_type='application/json')
        assert len(response.data['data']) == 2
        assert response.status_code == 200