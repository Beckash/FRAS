# from channels.auth import login, logout
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .EmailBackEnd import EmailBackEnd
from .models import Contact


def main_home(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'index.html')


def password_reset(request):
    return render(request, 'index.html')


@csrf_exempt
def contact(request):
    if request.method != "POST":
        # messages.error(request, "Method Not Allowed!")
        return HttpResponse('error')
    else:
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        flag = False
        try:
            contact_info = Contact(name=name, email=email, message=message)
            contact_info.save()
            flag = True
        except:
            flag = False
        if flag:
            return HttpResponse("ok")
        else:
            return HttpResponse("error")


def loginPage(request):
    return render(request, 'login.html')

@csrf_exempt
def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd().authenticate(request, username=request.POST.get('username'),
                                         # password=request.POST.get('password'), user_type=request.POST.get('role'))
                                         password=request.POST.get('password'))
        if user != None:
            login(request, user)
            user_type = user.user_type
            # return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
            if user_type == '1':
                return redirect('admin_home')

            elif user_type == '2':
                # return HttpResponse("Staff Login")
                return redirect('staff_home')

            elif user_type == '3':
                # return HttpResponse("Student Login")
                return redirect('student_home')
            elif user_type == '4':
                # return HttpResponse("Head Login")
                return redirect('head_home')
            else:
                messages.error(request, "Invalid Login!")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            # return HttpResponseRedirect("/")
            return redirect('login')


def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: " + request.user.email + " User Type: " + request.user.user_type)
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    # logout(request)
    # return HttpResponseRedirect('/')
    return render(request, 'index.html')
