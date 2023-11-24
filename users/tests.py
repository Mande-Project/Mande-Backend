from django.test import TestCase, Client
from .models import CustomUser

# Create your tests here.
class TestUser(TestCase):
    def setUp(self):
        c = Client()
        response = c.post('/api_users/users/', {
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

    def test_repasswordmissing(self):
        c = Client()
        response = c.post('/api_users/users/', {
            "email":"ismaelrgomez85@yopmail.com",
            "first_name":"Ismael",
            "last_name":"Gomez",
            "username":"IsmaelGomez10",
            "phone":"6436134211456",
            "role": "customer",
            "password":"MandeIsmael2023",
            "address":"Calle 123 # 45-67, Cali, Colombia"
            })
        
        assert response.status_code == 400

    def test_addressmissing(self):
        c = Client()
        response = c.post('/api_users/users/', {
            "email":"ismaelrgomez85@yopmail.com",
            "first_name":"Ismael",
            "last_name":"Gomez",
            "username":"IsmaelGomez10",
            "phone":"6436134211456",
            "role": "customer",
            "password":"MandeIsmael2023",
            
        })

        assert response.status_code == 400

    def test_addressnotexists(self):
        c = Client()
        response = c.post('/api_users/users/', {
            "email":"ismaelrgomez85@yopmail.com",
            "first_name":"Ismael",
            "last_name":"Gomez",
            "username":"IsmaelGomez10",
            "phone":"6436134211456",
            "role": "customer",
            "password":"MandeIsmael2023",
            "address":"Somethin weird here to made an error"
            })

    def test_allcustomers(self):
        c = Client()
        response = c.get('/api_users/customer/')
        assert len(response.data['data']) == 3

    def test_allworkers(self):
        c = Client()
        response = c.get('/api_users/worker/')
        assert len(response.data['data']) == 3

    def test_login(self):
        c = Client()
        s = CustomUser.objects.get(id=1)
        s.is_active = True
        s.save()

        response = c.post('/api_users/auth/jwt/create/', {
            "email":"samueltrujillo85@yopmail.com",
            "password":"MandeSamuel2023"
        })
        
        assert response.status_code == 200

    def test_patchuser(self):
        c = Client()
        s = CustomUser.objects.get(id=1)
        s.is_active = True
        s.save()
        
        response = c.post('/api_users/auth/jwt/create/', {
            "email":"samueltrujillo85@yopmail.com",
            "password":"MandeSamuel2023"
        })

        data = {"first_name":"monica","last_name":"ramirez","phone":"54767623453"}

        response = c.patch('/api_users/users/me/',data, headers={'Authorization': 'JWT ' + response.data['access']}, content_type='application/json')
        s.refresh_from_db()

        assert response.status_code == 200
        assert s.first_name == "monica"
        assert s.last_name == "ramirez"
        assert s.phone == "54767623453"

    def test_userdeletion(self):
        c = Client()
        s = CustomUser.objects.get(id=1)
        s.is_active = True
        s.save()

        data = {
            "email":"samueltrujillo85@yopmail.com",
            "password":"MandeSamuel2023"
        }
        
        response = c.post('/api_users/auth/jwt/create/', data)

        response = c.delete('/api_users/users/me/', data, headers={'Authorization': 'JWT ' + response.data['access']}, content_type='application/json')
        s.refresh_from_db()

        assert response.status_code == 200
        assert s.is_active == False