from django.shortcuts import render
from forum.models import Post
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from forum.authhelper import get_signin_url
from django.shortcuts import render
from django.contrib.auth import authenticate , login
from .forms import LoginForm
from forum.outlookservice import get_me
from forum.authhelper import get_token_from_code

def home(request):
  redirect_uri = request.build_absolute_uri(reverse('forum:gettoken'))
  sign_in_url = get_signin_url(redirect_uri)
  return HttpResponse('<a href="' + sign_in_url +'">Click here to sign in and view your mail</a>')

def gettoken(request):
  auth_code = request.GET['code']
  redirect_uri = request.build_absolute_uri(reverse('forum:gettoken'))
  token = get_token_from_code(auth_code, redirect_uri)
  access_token = token['access_token']
  user = get_me(access_token)

  # Save the token in the session
  request.session['access_token'] = access_token
  request.session['user_email'] = user['mail']
  context = { 'email': user['mail'] ,
     'name': user['displayName']
  }
  myEmail = user['mail']
  if myEmail is None:
    redirect_uri = request.build_absolute_uri(reverse('forum:gettoken'))
    sign_in_url = get_signin_url(redirect_uri)
    return HttpResponse('<title>Bad Request</title>'+'<p>Sorry but you need to sign in with a kings email</p>'+ '<br>' + '<a href="' + sign_in_url +'">Click here to give it another shot</a>')
  return render(request , 'theForum.html' , context)
  
def user_login(request):
   if request.method == 'POST':
      form = LoginForm(request.POST)
      if form.is_valid():
         cd = form.cleaned_data
         user = authenticate(username=cd['username'], password=cd['password'])
         if user is not None:
            if user.is_active:
               login(request, user)
               return HttpResponse('Authenticated successfully')
            else:
               return HttpResponse('Disabled account')
         else:
            return HttpResponse('Invalid Login')
   else:
      form = LoginForm()
   return render(request,  'account/connect.html', {'form': form})
      
    
def index(request):
   posts = Post.objects.all()
   return render(request,'inventory/index.html',{
       'posts' : posts,
   })

