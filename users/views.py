from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.http import HttpResponse
from djoser import utils, signals
from djoser.conf import settings
from djoser.views import UserViewSet
from djoser.compat import get_user_email
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.views import APIView, Response 
from .models import *
from .validators import *
from .serializers import CustomUserCreateSerializer, CustomUserSerializer

class CustomerViewSet(APIView):
    def get(self,request):
        with transaction.atomic():
            try:
                id = request.data['id']
                if Customer.objects.filter(user__id=id).exists():
                    customer = Customer.objects.get(user__id=id)
                    user = {
                        'id':customer.user.id,
                        'email':customer.user.email,
                        'phone':customer.user.phone,
                        'username':customer.user.username,
                        'first_name':customer.user.first_name,
                        'last_name':customer.user.last_name,
                        'photo':customer.user.photo,
                        'coordinate':customer.user.coordinate,
                    }
                    return Response({"status":"success","data":user})
                else:
                    return HttpResponse(f'No matching customer with id {id} found', status=401)
                
            except:      
                customers = Customer.objects.all()
                queryset = []
                for customer in customers:
                    user = {
                        'id':customer.user.id,
                        'email':customer.user.email,
                        'phone':customer.user.phone,
                        'username':customer.user.username,
                        'first_name':customer.user.first_name,
                        'last_name':customer.user.last_name,
                        'photo':customer.user.photo,
                        'coordinate':customer.user.coordinate,
                    }
                    queryset.append(user)
                return Response({"status":"success","data":queryset})

class WorkerViewSet(APIView):
    def get(self,request):
        with transaction.atomic():
            try:
                id = request.data['id']
                if Worker.objects.filter(user__id=id).exists():
                    worker = Worker.objects.get(user__id=id)
                    user = {
                        'id':worker.user.id,
                        'email':worker.user.email,
                        'phone':worker.user.phone,
                        'username':worker.user.username,
                        'first_name':worker.user.first_name,
                        'last_name':worker.user.last_name,
                        'photo':worker.user.photo,
                        'coordinate':worker.user.coordinate,
                    }
                    return Response({"status":"success","data":user})
                else:
                    return HttpResponse(f'No matching worker with id {id} found', status=401)
                
            except:      
                workers = Worker.objects.all()
                queryset = []
                for worker in workers:
                    user = {
                        'id':worker.user.id,
                        'email':worker.user.email,
                        'phone':worker.user.phone,
                        'username':worker.user.username,
                        'first_name':worker.user.first_name,
                        'last_name':worker.user.last_name,
                        'photo':worker.user.photo,
                        'coordinate':worker.user.coordinate,
                    }
                    queryset.append(user)
                return Response({"status":"success","data":queryset})

class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = settings.USER_ID_FIELD

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self,request,*args,**kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=self.request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save(*args, **kwargs)
            signals.user_registered.send(
                sender=self.__class__, user=user, request=self.request
            )

            image = self.request.FILES.get('image')
            if image:
                user.photo = image
                user.save()

            if request.data['role'] == 'customer':
                customer = Customer(
                    user = user,
                )
                customer.save()

            elif request.data['role'] == 'worker':
                worker = Worker(
                    user = user,
                    rating = 0,
                    is_available = True,
                )
                worker.save()

            context = {"user": user}
            to = [get_user_email(user)]
            if settings.SEND_ACTIVATION_EMAIL:
                settings.EMAIL.activation(self.request, context).send(to)
            elif settings.SEND_CONFIRMATION_EMAIL:
                settings.EMAIL.confirmation(self.request, context).send(to)
        
        return HttpResponse(user, status=200)
        
    def perform_update(self, request, *args, **kwargs):
        super().perform_update(request)
        user = request.instance
        signals.user_updated.send(
            sender=self.__class__, user=user, request=self.request
        )

        image = self.request.FILES.get('image')
        if image:
            user.photo = image
            user.save()

        user.password = make_password(request.data['password'])
        user.save()

        # should we send activation email after update?
        if settings.SEND_ACTIVATION_EMAIL and not user.is_active:
            context = {"user": user}
            to = [get_user_email(user)]
            settings.EMAIL.activation(self.request, context).send(to)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if instance == request.user:
            utils.logout_user(self.request)
            
        with transaction.atomic():
            user = self.get_object()
            user.is_active = False
            user.save()

            return HttpResponse('User was set to inactive')
        
    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomUserCreateSerializer
        else:
            return CustomUserSerializer          