from django.db import models

# Create your models here.
import uuid
from datetime import datetime,timezone

	
class user(models.Model):
	username = models.CharField(max_length=50, unique=True)
	password = models.CharField(max_length=50)
	email=models.EmailField()
	sp_id= models.UUIDField(default=uuid.uuid4,unique=True)
	signed_in=models.CharField(max_length=10,default='no')
class AddToDatabase(models.Model):
	username = models.ForeignKey(user, on_delete=models.CASCADE)
	random_url = models.UUIDField(default=uuid.uuid4,unique=True)
	data_text=models.CharField(max_length=50000,null=True)
	created_on = models.DateTimeField(auto_now_add=True,null=True)
	exp_time=models.IntegerField(null=True)
	data_title=models.CharField(max_length=500,null=True)
	share_id=models.UUIDField(default=uuid.uuid4,unique=True)
	edit_p=models.CharField(max_length=50,null=True)
	syntax=models.CharField(max_length=50,null=True)
	
	def chk_exp(self):
		now = datetime.now(timezone.utc)
		created=self.created_on
		td=(now-created).total_seconds()
		if self.exp_time==0:
			pass
		elif td >= self.exp_time:
			delinfo.objects.create(
			random_url=self.random_url,
			username_id=self.username_id,
			)
			self.delete()
class delinfo(models.Model):
	random_url=models.UUIDField(unique=True)
	username_id=models.IntegerField()
class editinfo(models.Model):
	share_id=models.UUIDField(default=uuid.uuid4,unique=True)
	share_id2=models.CharField(null=True,max_length=1000)
	created = models.DateTimeField(auto_now_add=True,null=True)
	edit_text=models.CharField(max_length=50000)
	data_title=models.CharField(max_length=500,null=True)
	syntax=models.CharField(max_length=50,null=True)
	

