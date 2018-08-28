from .models import AddToDatabase,user,editinfo
from django import forms
import uuid
class LoginForm(forms.Form):
    username=forms.CharField(max_length=50)
    password=forms.CharField(max_length=50)
	
		
class Signup(forms.Form):
    username=forms.CharField(max_length=50)
    password=forms.CharField(max_length=50)
    npassword=forms.CharField(max_length=50)
    email=forms.EmailField()
	
    def save(self):
        new_entry = user.objects.create(
        username = self.cleaned_data['username'],
		password = self.cleaned_data['password'],
        email = self.cleaned_data['email'],
		)
        return new_entry

class paste(forms.Form):
	data_text=forms.CharField(max_length=50000)
	exp_time=forms.IntegerField()
	data_title=forms.CharField(max_length=500)
	edit_p=forms.CharField(max_length=50)
	username_id=forms.IntegerField()
	syntax=forms.CharField(max_length=50)
	
	def save(self):
		new_entry = AddToDatabase.objects.create(
        data_text = self.cleaned_data['data_text'],
		exp_time = self.cleaned_data['exp_time'],
        data_title = self.cleaned_data['data_title'],
		edit_p = self.cleaned_data['edit_p'],
		username_id=self.cleaned_data['username_id'],
		syntax=self.cleaned_data['syntax'],
		
		)
		return new_entry
class editf(forms.Form):
	edit_text=forms.CharField(max_length=50000)
	data_title=forms.CharField(max_length=500)
	syntax=forms.CharField(max_length=50)
	share_id2=forms.CharField(max_length=1000)
	def save(self):
		new_entry=editinfo.objects.create(
		edit_text=self.cleaned_data['edit_text'],
		data_title=self.cleaned_data['data_title'],
		syntax=self.cleaned_data['syntax'],
		share_id2=self.cleaned_data['share_id2'],
		)
		return new_entry