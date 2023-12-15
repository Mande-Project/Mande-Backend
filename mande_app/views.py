from .models import Worker_Job, Service, Job
from mande_notifications.models import Notification
from users.models import CustomUser, Worker, Customer
from django.db import transaction
from django.http import HttpResponse
from django.utils import timezone
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.extra.rate_limiter import RateLimiter
from rest_framework.views import APIView, Response
from .serializers import JobSerializer

import json

class JobsAPI(APIView):
    def get(self, request):
        serializer = JobSerializer(Job.objects.all(), many=True)
        data = serializer.data

        return Response({"status":"success","data":data},status=200)

class Worker_JobAPI(APIView):
    geolocator = Nominatim(user_agent="mandeAPI")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    def get(self,request):
        data = []

        try:
            id_user = request.GET.get('id_user', None)
        except:
            return HttpResponse("No id provided",status=401)
        
        coor1 = CustomUser.objects.get(id=id_user).coordinate

        for w in Worker_Job.objects.all():
            if(w.active):
                distance = None
                
                if w.worker.user.coordinate != None and coor1 != None:
                    distance = geodesic((coor1.latitude,coor1.longitude),
                                        (w.worker.user.coordinate.latitude,w.worker.user.coordinate.latitude)).km

                aux = {
                    "id_worker_job":w.id,
                    "id_worker":w.worker.user.id,
                    "first_name":w.worker.user.first_name,
                    "last_name":w.worker.user.last_name,
                    "email":w.worker.user.email,
                    "phone":w.worker.user.phone,
                    "worker_available":w.worker.is_available,
                    "job":w.job.name,
                    "price":w.price,
                    "description":w.description,
                    "distance":distance,
                    "rating":w.worker.rating,
                    "photo":w.worker.user.photo
                }

                data.append(aux)

        return Response({"status":"success","data":data})
    
    def post(self,request):
        with transaction.atomic():
            try:
                id_user = self.request.data['id_user']
            except:
                return HttpResponse("No id provided",status=401)
            
            try:
                id_job = self.request.data['id_job']
            except:
                return HttpResponse("No id of job provided",status=401)
            
            try:
                price = self.request.data['price']
                description = self.request.data['description']
            except:
                return HttpResponse("No price or description provided",status=401)

            user = CustomUser.objects.get(id=id_user)
            if not(len(Worker.objects.filter(user=user)) == 1):
                return HttpResponse("User is not a worker",status=401)
            
            if len(Worker_Job.objects.filter(worker=Worker.objects.get(user=user),
                                    job=Job.objects.get(id=id_job))) == 1:
                
                worker_job = Worker_Job.objects.get(worker=Worker.objects.get(user=user),
                                    job=Job.objects.get(id=id_job))

                if(worker_job.active):    
                    return HttpResponse("Job is already added",status=401)
                else:
                    worker_job.active = True
                    worker_job.price = price
                    worker_job.description = description
                    worker_job.save()
                    return HttpResponse(f"Job updated and set active to worker user with id {id_user}",status=200)
            
            Worker_Job.objects.create(worker=Worker.objects.get(user=user),
                                    job=Job.objects.get(id=id_job),
                                    price=price,
                                    description=description)
            
            Notification.objects.create(
                subject="New job offer",
                body=f"Hi, you recently added a new job offer for {Job.objects.get(id=id_job).name}. You can cancel it in the app if you want to. If you have any questions, please contact us.",
                as_customer=False,
                user=user)
            
            return HttpResponse(f"Job added to worker user with id {id_user}",status=200)

    def delete(self,request):
        with transaction.atomic():
            try:
                id_user = self.request.data['id_user']
            except:
                return HttpResponse("No id of user provided",status=401)
            
            try:
                id_job = self.request.data['id_job']
            except:
                return HttpResponse("No id of job provided",status=401)

            user = CustomUser.objects.get(id=id_user)
            if not(len(Worker.objects.filter(user=user)) == 1):
                return HttpResponse("User is not a worker",status=401)
            
            if not(len(Worker_Job.objects.filter(worker=Worker.objects.get(user=user),
                                    job=Job.objects.get(id=id_job))) == 1):
                return HttpResponse("Worker is not related to the job",status=401)
            
            worker_job = Worker_Job.objects.get(worker=Worker.objects.get(user=user),
                                    job=Job.objects.get(id=id_job))
            worker_job.active = False
            worker_job.save()
            
            Notification.objects.create(
                subject="Job offer canceled",
                body=f"Hi, you recently canceled a job offer for {Job.objects.get(id=id_job).name}. You can add it again in the app if you want to. If you have any questions, please contact us.",
                as_customer=False,
                user=user)

            return HttpResponse(f"Job set inactive to worker user with id {id_user}",status=200)

class ServiceAPI(APIView):
    def get(self,request):

        try:
            id_user = request.GET.get('id_user', None)
        except:
            return HttpResponse("No id provided",status=401)
        
        try:
            CustomUser.objects.get(id=id_user)
        except:
            return HttpResponse("User does not exist",status=401)

        data = []
        aux = Service.objects.all()

        if(Customer.objects.filter(user=id_user).exists()):
            services = []
            for s in aux:
                if(s.user.id == int(id_user)):
                    services.append(s)
        elif(Worker.objects.filter(user=id_user).exists()):
            services = []
            for s in aux:
                if(s.worker_job.worker.user.id == int(id_user)):
                    services.append(s)
                
        for s in services:
            aux = {
                "id_service":s.id,
                "c_first_name":s.user.first_name,
                "c_last_name":s.user.last_name,
                "c_email":s.user.email,
                "c_phone":s.user.phone,
                "w_first_name":s.worker_job.worker.user.first_name,
                "w_last_name":s.worker_job.worker.user.last_name,
                "w_email":s.worker_job.worker.user.email,
                "w_phone":s.worker_job.worker.user.phone,
                "job":s.worker_job.job.name,
                "hours":s.hours,
                "cost":s.cost,
                "status":s.status,
                "date":s.date,
                "description":s.description,
                "rating": s.rating
            }
            data.append(aux)
        
        return Response({"status":"success","data":data})
    
    def post(self,request):
        with transaction.atomic():
            id_user = self.request.data['id_user']
            worker_job = Worker_Job.objects.get(id=self.request.data['id_worker_job'])
            worker = worker_job.worker

            if(not worker.is_available):
                return HttpResponse("Worker is not available",status=401)
            
            if(not worker_job.active):
                return HttpResponse("Job offer by this Worker is not active",status=401)

            worker.is_available = False
            worker.save()

            user = CustomUser.objects.get(id=id_user)
            
            Service.objects.create(
                user=user,
                worker_job=worker_job,
                date=timezone.now(),
                status='A',
                hours=self.request.data['hours'],
                cost=float(worker_job.price)*float(self.request.data['hours']),
                rating=None,
                description=self.request.data['description'])
            
            Notification.objects.create(
                subject="New service request",
                body=f"Hi, you recently requested a new service for {worker_job.job.name} to the worker {worker.user.first_name}. You can cancel it in the app if you want to. If you have any questions, please contact us.",
                as_customer=True,
                user=user)
            
            Notification.objects.create(
                subject="New service request",
                body=f"Hi, you recently received a new service request for {worker_job.job.name} from {user.first_name}. You can cancel it in the app if you want to. If you have any questions, please contact us.",
                as_customer=False,
                user=worker.user)
            
            return HttpResponse(f"Service requested by customer {id_user} created, job:{worker_job.job.name}",status=200)
    
    def patch(self,request):
        with transaction.atomic():
            service = Service.objects.get(id=self.request.data['id_service'])

            if(not service.status == 'A'):
                return HttpResponse("Service already ended or canceled",status=401)

            service.status = 'F'
            service.rating = self.request.data['rating']
            service.save()
            
            worker = service.worker_job.worker

            # Counting the number of services where the worker has been rated
            num_services = 0
            for s in Service.objects.all():
                if(s.worker_job.worker == worker and s.rating != None and s.status == 'F'):
                    num_services += 1

            # Calculating the new rating
            worker.rating = (worker.rating*(num_services-1) + float(self.request.data['rating']))/(num_services)
            worker.is_available = True
            worker.save()

            Notification.objects.create(
                subject="Service completed",
                body=f"The service with id {service.id} was completed. The job related to {service.worker_job.job.name} with the worker {worker.user.first_name} is now finished. You can check more offers in our app. If you have any questions, please contact us.",
                as_customer=True,
                user=service.user)
            
            Notification.objects.create(
                subject="Service completed",
                body=f"The service with id {service.id} was completed. The job related to {service.worker_job.job.name} offered to the customer {service.user.first_name} is now finished, you are now available to offer your services to another customer. You can check more offers in our app. If you have any questions, please contact us.",
                as_customer=False,
                user=worker.user)
            
            return HttpResponse(f"Service with id {self.request.data['id_service']} updated",status=200)

    def delete(self,request):
        service = Service.objects.get(id=self.request.data['id_service'])

        if(not service.status == 'A'):
                return HttpResponse("Service already ended or canceled",status=401)
        
        service.status = 'C'
        service.save()
        
        worker = service.worker_job.worker
        worker.is_available = True
        worker.save()

        Notification.objects.create(
                subject="Service canceled",
                body=f"The service with id {service.id} was canceled. The job related to {service.worker_job.job.name} with the worker {worker.user.first_name} is nos longer on process. You can check more offers in our app. If you have any questions, please contact us.",
                as_customer=True,
                user=service.user)
        
        Notification.objects.create(
                subject="Service canceled",
                body=f"The service with id {service.id} was canceled. The job related to {service.worker_job.job.name} offered to the customer {service.user.first_name} is nos longer on process, you are now available to offer your services to another customer. You can check more offers in our app. If you have any questions, please contact us.",
                as_customer=False,
                user=worker.user)

        return HttpResponse(f"Service with id {self.request.data['id_service']} was canceled",status=200)
