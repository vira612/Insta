from django.db import models
from django.contrib.auth.models import User

import uuid


class Post(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	image = models.CharField(max_length=200, null=True)
	description = models.CharField(max_length=200, null=True)
	likes = models.IntegerField(default=0)
	username = models.ForeignKey(User, on_delete=models.DO_NOTHING)

	def __str__(self):
		return self.description

	
class Follow(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	username = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='following')
	other_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='follower')

	# def __str__(self):
	# 	return self.username