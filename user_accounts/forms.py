from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *



# from .models import Order


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'password1', 'password2']


class FollowForm(ModelForm):
	class Meta:
		model = Follow
		fields = ['username','other_user']


class CreatePostForm(ModelForm):
	class Meta:
		model = Post
		fields = ['image','description','username']