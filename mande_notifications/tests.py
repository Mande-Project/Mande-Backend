from django.test import TestCase, Client
from .models import Notification
from users.models import CustomUser

class TestNotification(TestCase):
    def setUpTestData():
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

    def test_create_notification_customer(self):
        c = Client()
    
        response = c.post('/api_notifications/notifications/', {
            "subject":"TEST SUBJECT",
            "body": "We have to tell you that this is a test body",
            "as_customer":True,
            "user": 1
        })
        
        n = Notification.objects.get(id=1)

        assert n.body == "We have to tell you that this is a test body"

        assert response.status_code == 201

    
    def test_create_notification_worker(self):
        c = Client()

        response = c.post('/api_notifications/notifications/', {
            "subject":"TEST SUBJECT",
            "body": "We have to tell you that this is a test body",
            "as_customer":False,
            "user": 2
        })
        
        n = Notification.objects.get(id=1)

        assert n.body == "We have to tell you that this is a test body"

        assert response.status_code == 201


    def test_get_notifications_orm(self):
        c = Client()

        c.post('/api_notifications/notifications/', {
            "subject":"Service completed",
            "body": "We confirm that a service offered by one of our workers has been marked as completed",
            "as_customer":True,
            "user": 1
        })

        c.post('/api_notifications/notifications/', {
            "subject":"Completed task",
            "body": "You have just marked a task as completed",
            "as_customer":False,
            "user": 2
        })


        c.post('/api_notifications/notifications/', {
            "subject":"Other type of notifications",
            "body": "Notifications are a flexible mechanism to keep registry of important events",
            "as_customer":True,
            "user": 1
        })


        c.post('/api_notifications/notifications/', {
            "subject":"Other type of notifications",
            "body": "Notifications are a flexible mechanism to keep registry of important events",
            "date": "2023-09-20",
            "as_customer":False,
            "user": 2
        })
        
        n_c = Notification.objects.filter(user=1, as_customer=True)

        n_w = Notification.objects.filter(user=2, as_customer=False)

        assert n_c[0].subject == "Service completed"

        assert n_c[1].subject == "Other type of notifications"

        assert n_w[0].subject == "Completed task"

        assert n_w[1].subject == "Other type of notifications"


    def test_get_notifications_request(self):
        c = Client()

        c.post('/api_notifications/notifications/', {
            "subject":"Service completed",
            "body": "We confirm that a service offered by one of our workers has been marked as completed",
            "as_customer":True,
            "user": 1
        })

        c.post('/api_notifications/notifications/', {
            "subject":"Completed task",
            "body": "You have just marked a task as completed",
            "as_customer":False,
            "user": 2
        })


        c.post('/api_notifications/notifications/', {
            "subject":"Other type of notifications",
            "body": "Notifications are a flexible mechanism to keep registry of important events",
            "as_customer":True,
            "user": 1
        })


        c.post('/api_notifications/notifications/', {
            "subject":"Other type of notifications",
            "body": "Notifications are a flexible mechanism to keep registry of important events",
            "date": "2023-09-20",
            "as_customer":False,
            "user": 2
        })

        res_1 = c.get('/api_notifications/list_filter_user/1/')

        assert res_1.data[0]['subject'] == "Service completed"

        assert res_1.data[1]['subject'] == "Other type of notifications"

        res_2 = c.get('/api_notifications/list_filter_user/2/')

        assert res_2.data[0]['subject'] == "Completed task"

        assert res_2.data[1]['subject'] == "Other type of notifications"

    def test_update_notifications(self):
        c = Client()

        res1 = c.post('/api_notifications/notifications/', {
            "subject":"Service completed",
            "body": "We confirm that a service offered by one of our workers has been marked as completed",
            "as_customer":True,
            "user": 1
        })

        assert res1.status_code == 201

        res2 = c.patch('/api_notifications/notifications/1/', {
            "id": 1,
            "subject":"Notification has been updated"
        }, content_type='application/json')

        assert res2.status_code == 200

        n = Notification.objects.get(id=1)

        assert n.subject == "Notification has been updated"

    def test_create_customer_notification_for_worker(self):
        c = Client()

        res1 = c.post('/api_notifications/notifications/', {
            "subject": "Service completed",
            "body": "testing subject",
            "as_customer": False,
            "user": 1
        })

        assert res1.status_code == 400

        # Notification was not created so it cannot be found

        res2 = c.get('/api_notifications/notifications/1')

        res3 = c.get(res2.url)

        assert res3.status_code == 404

    def test_create_worker_notification_for_customer(self):
        c = Client()

        res1 = c.post('/api_notifications/notifications/', {
            "subject":"Service completed",
            "body": "testing subject",
            "as_customer": True,
            "user": 2  
        })

        assert res1.status_code == 400

        # Notification was not created so it cannot be found

        res2 = c.get('/api_notifications/notifications/1')

        res3 = c.get(res2.url)

        assert res3.status_code == 404


        
        
        





        
    