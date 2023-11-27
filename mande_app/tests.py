from django.test import TestCase, Client
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

    def test_jobs(self):
        client = Client()   
        response = client.get('/mande_app/jobs/')

        assert len(response.data['data']) == 6
        assert response.data['data'][0]['name'] == 'Plomero'
        assert response.data['data'][2]['name'] == 'Carpintero'
        assert response.data['data'][5]['name'] == 'Jardinero'
        