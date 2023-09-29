from .models import CustomUser


# Component: create_user
# Description: Auxilary function that creates a new CustomUser instance, 
# if given email already exists returns False. SHOULD BE CALLED INSIDE A TRY-EXCEPT BLOCK
# Author: paul.rojas@correounivalle.edu.co, paulrodrigorojasecl@gmail.com

def create_user(data):
    email=data['email']
    password=data['password']
    phone=data['phone']
    username=data['username']
    first_name=data['first_name']
    last_name=data['last_name']
    
    if not CustomUser.objects.filter(email=email).exists():
        user = CustomUser(
            email=email,
            password=password,
            phone=phone,
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_active=True
        )
        user.set_password(data['password'])
        user.save()
        
        return user
    else:
        return False