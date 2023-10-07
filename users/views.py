from djoser.views import UserViewSet
from rest_framework import permissions
from .models import *
from .serializers import CustomUserCreateSerializer, CustomUserSerializer

class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomUserCreateSerializer
        return CustomUserSerializer

""" 
# Component: customer_register
# Description: View - Endpoint that creates new users for new Customer instances
# Author: paul.rojas@correounivalle.edu.co, paulrodrigorojasecl@gmail.com

@api_view(['POST'])
def customer_register(request):
    if request.method == 'POST':
        try:

            data = {
                'email':request.data.get('email'),
                'password':request.data.get('password'),
                'phone':request.data.get('phone'),
                'username':request.data.get('username'),
                'first_name':request.data.get('first_name'),
                'last_name':request.data.get('last_name')
            }

            user = create_user(data)

            if user:

                client = Customer(
                    user = user,
                )

                client.save()

                return HttpResponse("Customer successfully registered", status=200)
            else:
                return HttpResponse("That user has already been registered", status=400)    
            
        except Exception as e:
            print(e)
            return HttpResponse("An error has ocurred", status=400)
        
    else:
        return HttpResponse("Unsupported method", status=405)
               


# Component: worker_register
# Description: View - Endpoint that creates new users for new Worker instances
# Author: paul.rojas@correounivalle.edu.co, paulrodrigorojasecl@gmail.com

@api_view(['POST'])
def worker_register(request):
    if request.method == 'POST':
        try:

            data = {
                'email':request.data.get('email'),
                'password':request.data.get('password'),
                'phone':request.data.get('phone'),
                'username':request.data.get('username'),
                'first_name':request.data.get('first_name'),
                'last_name':request.data.get('last_name')
            }

            user = create_user(data)

            if user:

                client = Worker(
                    user = user,
                )

                client.save()

                return HttpResponse("Worker successfully registered", status=200)
            else:
                return HttpResponse("That user has already been registered", status=400)    
            
        except Exception as e:
            print(e)
            return HttpResponse("An error has ocurred", status=400)
        
    else:
        return HttpResponse("Unsupported method", status=405)     
        

# Component: customer_login
# Description: View - Endpoint that allows to create a session in the application for a Customer user
# Author: paul.rojas@correounivalle.edu.co, paulrodrigorojasecl@gmail.com

@api_view(['POST'])
def customer_login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password);

        if Customer.objects.filter(user__email=email).exists():
            user = authenticate(email=email, password=password)

            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return JsonResponse({'token':token.key}, status=200)

        return HttpResponse('No matching customer and password were found', status=401)
    

# Component: worker_login
# Description: View - Endpoint that allows to create a session in the application for a Worker user
# Author: paul.rojas@correounivalle.edu.co, paulrodrigorojasecl@gmail.com

@api_view(['POST'])
def worker_login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password);

        if Worker.objects.filter(user__email=email).exists():
            user = authenticate(email=email, password=password)

            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return JsonResponse({'token':token.key}, status=200)

        return HttpResponse('No matching customer and password were found', status=401)
    
    

# Component: user_logout
# Description: View - Endpoint that logouts from the current session
# Author: paul.rojas@correounivalle.edu.co, paulrodrigorojasecl@gmail.com


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            request.user.auth_token.delete()
            return HttpResponse('User was successfully logout')
        except Exception as e:
            return HttpResponse('Internal error ocurred', status=500) """