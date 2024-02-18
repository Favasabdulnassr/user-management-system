from django.shortcuts import render, redirect
from myapp.models import Users
from django.contrib import messages, auth
from django.contrib.auth import authenticate
import re
from django.views.decorators.cache import never_cache
 
# Create your views here.
def login(request):
    if 'name' in request.session:
        return redirect('table')
    if 'username' in request.session:
        return redirect('logged')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = Users.objects.filter(name=username, password=password)
        if user is not None:
            # auth.login(request, user)   # Set the user in the session
            request.session['username'] = username #set the 'username' key
            return redirect('logged')
        else:
            messages.error(request, "Invalid password or username")
    return render(request, "login.html")  

def Logged(request):
    if 'username' in request.session:
        username = request.session['username'] 
        return render(request, 'logged.html',{'username':username})

    else:
        return redirect('login')
        
 

def validate_email(email):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    if not re.match(email_pattern, email):
        return False
    return True

def validate_password(password):
    password_pattern = r'^(?=.*[a-zA-Z]).{8,}$'
    if not re.match(password_pattern, password):
        return False
    return True


def validate_username(username):
    username_pattern = r'^[a-zA-Z0-9]+$'
    if not re.match(username_pattern, username):
        return False
    return True
 
def Signup(request):
    if 'username' in request.session:
        return redirect('logged')
    if 'name' in request.session:
        return redirect('table')
    
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST.get('password')  # Get password as a string
        confirm_password = request.POST.get('passwordConfirm') # get confirm password as a string
        phone = request.POST.get('phone') #get phone number  as a string

        #check if passwords match
        if password != confirm_password:
            messages.error(request, "passwords do not match")
            return redirect('signup')
        
        #convert  phone to integers
        try:
            phone = int(phone)
        except ValueError:
            messages.error(request, "Invalid phone number format") 
            return redirect('signup')


        if not validate_username(username):
            messages.error(request, "Username should only contain charadcters")
            return redirect('signup')
        
        if Users.objects.filter(name=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')
        
        elif Users.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken")
            return redirect('signup')
        
        elif not validate_email(email):
            messages.error(request, "Invalid email format")
            return redirect('signup')
        
        elif not validate_password(password):
            messages.error(request, "password should be atleast 8 characters")
            return redirect('signup')
        
        else:
            user = Users()
            user.name = username
            user.email = email
            user.password = password
            user.phone = phone
            user.save()
            messages.info(request, "User creaated successfully.")

    else:
        return render(request, 'signup.html')
    
    return redirect('login')
    

@never_cache
def Logout(request):
    if 'username' in request.session:
        request.session.flush()
        return redirect('logged')
    if 'name' in request.session:
        request.session.flush()
        return redirect('table')

    return render(request, 'login.html')

def Adminlogin(request):
    if 'username' in request.session:
        return redirect('logged')
    
    if 'name' in request.session:
         return redirect('table')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            request.session['name']= username
            # auth_login(request,user)
            return redirect('table')
        else:
            messages.error(request, "password or username is invalid")
            return render(request, 'adminlogin.html')

    return render(request, 'adminlogin.html')    

    
    return render(request, 'login.html')

def table(request):
    if 'name' not in request.session:
        return redirect('login')
    if 'name' in request.session:
        user = Users.objects.all() 

        context = {
            'user':user
        }
        return render(request, 'table.html', context)
    else:
        messages.error(request, "you must be logged in to access this page.")
        return redirect('adminlogin')


def Add(request):
    if 'name' not in request.session:
        return redirect('login')
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')

        user = Users(
            name = name,
            email = email,
            password = password,
            phone = phone
        )
        user.save()
        return redirect('table')
    else:
        return redirect('table')


 

# def Edit(request):
#     user = Users.objects.all()

#     context = {
#         'user':user,
#     }
#     return redirect(request,'table.html', context)

def Update(request,id):
    
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')


        user = Users(
            id = id,
            name = name,
            email = email,
            password = password,
            phone = phone
        )
        user.save()
        return redirect('table')
    else:
        return redirect('table')

def Delete(request, id):
    user = Users.objects.filter(id = id)
    user.delete()
    context = {
        'user':user,
    }
    return redirect('table')
def search(request):
    if 'name' in request.session:
        query = request.GET['query']
        allPosts = Users.objects.filter(name__icontains=query)
        params = {'allPosts': allPosts}
        return render(request,'search.html',params)
    else:
        return redirect('login')

