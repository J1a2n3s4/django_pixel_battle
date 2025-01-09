from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.core.files import File
from .models import time_adress
from django.shortcuts import redirect
from .forms import userform
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
import datetime



def login_or_register(request):
    #only register, no need for a login page.

    #if user send a form basically  
    if request.method == "POST":
        form = userform(request.POST)

        if form.is_valid():

            if User.objects.filter(username = form.cleaned_data["name"]).exists():
                #adding an error message to html content.
                return render(request,'login_or_register.html',{'form':form,'problem':["username already exists."]})
            if User.objects.filter(email = form.cleaned_data["name"]).exists():
                #adding an error message to html content.
                return render(request,'login_or_register.html',{'form':form,'problem':["email already exists."]})
            
            #creating new user and assigning a datetime of gaining ability for new pixel. 
            #datetime is in special model to still use default django User model.

            new_user = User.objects.create_user(form.cleaned_data["name"],form.cleaned_data["email"],form.cleaned_data["password"])
            new_user.save()
            new_mail = time_adress(email = form.cleaned_data["email"],due = datetime.datetime.now())
            new_mail.save()
            return redirect("/main/")
    else:
        
        form = userform()
    return render(request,'login_or_register.html',{'form':form})


def notime(request):
    #sending a HTML page with message of having your turn given.
    return render(request,'notime.html')

def main_page(request):

    pixelpos = 0
    pixelcolor = ''

    f = open("canvas.pbf", "r")#reading canvas from local file.
    myfile = File(f)
    strlist = myfile.read().split(",")
    array2d = []


    for i in range(50):#creating content for html table
        array = []
        for j in range (100):
            array.append(strlist[100*i+j])
        array2d.append(array)
    
    content = {'two_d':array2d}
    myfile.close()

    #if user send a form basically
    if request.method == "POST":
        #defining which place in canvas file was edited
        pixelpos = (int(request.POST["y"])-1)*100+(int(request.POST["x"])-1)
        match request.POST["color"]:
            case "white":
                pixelcolor = 'w'
            case "red":
                pixelcolor = 'r'
            case "green":
                pixelcolor = 'g'
            case "blue":
                pixelcolor = 'b'
            case "gray":
                pixelcolor = 'a'
            case "yellow":
                pixelcolor = 'y'

        #checking if given user has the right password as in HTML form
        form_user = User.objects.filter(username = request.POST.get("username"))[0]
        if form_user.check_password(request.POST["password"]):
            #checking if given user has access to making a pixel
            if time_adress.objects.all().filter(email = form_user.email)[0].due > datetime.datetime.now():
                return redirect("/notime/")
            else:
                #writing changes to local file and taking away user's pixel drawing ability for 1 minute.
                timenew = time_adress.objects.all().filter(email = form_user.email)[0]
                timenew.due = datetime.datetime.now() + datetime.timedelta(minutes=1)
                timenew.save()
                f = open("canvas.pbf", "w")
                writefile = File(f)
                strlist[pixelpos] = pixelcolor
                for i in strlist:
                    writefile.write(i+",")
                writefile.close()
        else:
            #adding an error message to html content.
            content = {'badpassword': "Wrong password or username.", 'two_d':array2d}
    
    return render(request,'main.html',content)


def sorry(request):
    return render(request,'sorry_no_git.html')