
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *


def register(request):
	# print(request.user)
	if request.user.is_authenticated:
		return redirect('/dashboard/'+str(request.user))
	else:
		form = CreateUserForm()
		
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			# print(request.POST)
			# print(form)
			if form.is_valid():
				form.save()

				user = form.cleaned_data.get('username')
				# print(user)
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'register.html', context)

def login(request):

	if request.user.is_authenticated:
		return redirect('/dashboard/'+str(request.user))
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				auth.login(request, user)
				request.session['username'] = username
				return redirect('/dashboard/'+username)
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'login.html', context)
	


@login_required(login_url='login')
def dashboard(request,user):

	if str(request.user) == user:
		if request.method == 'POST':
			print(request.POST)
			id = request.POST.get('id')
			post = Post.objects.get(id = id)
			post.likes += 1
			post.save()


		
		user_all = User.objects.get(username = user)
		# posts = Post.objects.filter(username = user_all).all()
		

		followings = Follow.objects.filter(username = user_all)
		posts = []
		for following in followings :
			post = Post.objects.filter(username = following.other_user).all()
			if post :
				posts.append(post)

		# print(posts[0][0].description)
		total_posts = len(posts)
		# posts = Post.objects.filter(username = followings).all()
		# followings = Follow.objects.filter(other_user = user_all).count()
		
		context = {'user' : user, 'total_posts':total_posts, 'posts':posts, 'followings':followings}
		return render(request, 'dashboard.html', context)
	return HttpResponse("wrong user")


@login_required(login_url='login')
def user(request,user):
	
	if str(request.user) == user:
		user_all = User.objects.get(username = user)
		posts = Post.objects.filter(username = user_all).all()
		total_posts = posts.count()

		followings = Follow.objects.filter(username = user_all).count()
		followers = Follow.objects.filter(other_user = user_all).count()
		
		context = {'user' : user, 'total_posts':total_posts, 'posts':posts, 'followers':followers, 'followings':followings}
		return render(request, 'user.html', context)
	return HttpResponse("wrong user")

@login_required(login_url='login')
def all_user(request,user):

	if str(request.user) == user:
		form = FollowForm()
		if request.method == "POST":
			print(request.POST)
			username = request.POST.get('username')
			other_user = request.POST.get('other_user')

			data = request.POST.dict()
			data['username'] = User.objects.get(username = username)
			data['other_user'] = User.objects.get(username = other_user)
			form = FollowForm(data)
			print(form)
			if form.is_valid():
					form.save()
					return redirect('/allusers/'+user)

		
		user_all = User.objects.get(username = user)
		followings = Follow.objects.filter(username = user_all).all()
		users = User.objects.all().exclude(username = user)
		# users1 = User.objects.all().exclude(username = followings)
		user1  = []
		for u in users:
			for f in followings:
				print(f.other_user)
				if u != f.other_user :
					print(u)
					user1.append(u)
		
		user1 = list(set(user1))
		print(user1)

		context = {'user':user,'form':form, 'user1':user1}
		return render(request, 'users.html',context)
	return HttpResponse("wrong user")

@login_required(login_url='login')
def new_post(request,user):
	if str(request.user) == user:
		form = CreatePostForm()
		user_all = User.objects.filter(username = user).all()
		
		if request.method == 'POST':
			
			data = request.POST.dict()
			data['username']=user_all[0]
	        
			form = CreatePostForm(data)
			if form.is_valid():
				form.save()

				return redirect('/user/'+user)
		context = {'user_all':user_all[0],'form':form}
		return render(request, 'create_post.html', context)
	return render(request, 'users.html',context)

@login_required(login_url='login')
def logout(request):
	auth.logout(request)
	return redirect('login')