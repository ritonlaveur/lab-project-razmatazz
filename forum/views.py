from django.shortcuts import render
from django.http import Http404
from forum.models import Post
from forum.models import Comment

from django.utils import timezone
from django.shortcuts import redirect

# post and comment forms
from .forms import PostForm
from .forms import CommentForm

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from forum.authhelper import get_signin_url
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
  posts = Post.objects.all()
  return render(request,'forum/index.html',{
       'posts' : posts,
       'email' : user['mail'],
       'user_name' : user['displayName']
   })

def post_new(request):
   if request.method == "POST":
      form = PostForm(request.POST)
      if form.is_valid():
         post = form.save(commit=False)
         post.author = request.session['user_email']
         post.date = timezone.now()
         post.save()
         return redirect('post_detail', id=post.id)
   else:
      form = PostForm()
   return render(request,'forum/post_edit.html', {'form':form})

def comment_new(request,id):
   if request.method == "POST":
      form = CommentForm(request.POST)
      if form.is_valid():
         comment = form.save(commit=False)
         comment.post = Post.objects.get(id=id)
         comment.author = request.session['user_email']
         comment.date = timezone.now()
         comment.save()
         return  redirect('post_detail',id=id)
   else:
      form = CommentForm()
   post = Post.objects.get(id=id)
   return render(request,'forum/comment_edit.html',{'form':form,'post':post})

def index(request):
   posts = Post.objects.all()
   return render(request,'forum/index.html',{
       'posts' : posts,
   })

def post_detail(request,id):
   try:
      post = Post.objects.get(id=id)
      comments = Comment.objects.filter(post__id=id)
   except Post.DoesNotExist:
      raise Http404('This post does not exist')
   return render(request,'forum/post_detail.html',{
      'post' : post,
      'comments' : comments
   })

def post_delete(request,id):

   post = Post.objects.get(id=id)
   post.delete()

   return redirect('index')

def post_detail(request,id):
   try:
      post = Post.objects.get(id=id)
      comments = Comment.objects.filter(post__id=id)
   except Post.DoesNotExist:
      raise Http404('This post does not exist')
   return render(request,'forum/post_detail.html',{
      'post' : post,
      'comments' : comments
   })

def post_delete(request,id):
   post = Post.objects.get(id=id)
   if post.author == request.session['user_email']:
      post.delete()
   return redirect('index_home')
