from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from django.template import loader
from .models import AddToDatabase,user,delinfo,editinfo
from .forms import LoginForm,Signup,paste,editf
from django.views.decorators.cache import cache_control,never_cache

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Home(request):
    error=''
    form=LoginForm()
    share1=AddToDatabase.objects.values_list('share_id',flat=True).order_by('-created_on')
    for i in share1:
        c=get_object_or_404(AddToDatabase,share_id=i)
        c.chk_exp()
    share=AddToDatabase.objects.values_list('share_id',flat=True).order_by('-created_on')[:3]
    author=AddToDatabase.objects.values_list('username_id',flat=True).order_by('-created_on')[:3]
    list1=[]
    for i in author:
        v=get_object_or_404(user,id=i).username
        list1.append(v)
    latest_th=AddToDatabase.objects.values_list('data_title',flat=True).order_by('-created_on')[:3]
    if request.POST:
        form = LoginForm(request.POST)

        if form.is_valid():
            try:
                q= get_object_or_404(user, username=form.cleaned_data['username'])
            except:
                error="username not registered"
                return render(request, 'pastebin_app/index.html', {'form':form,'error':error,'randomurls':share,'latest':latest_th,'list1':list1,})
            if form.cleaned_data['password']==q.password :
                a=get_object_or_404(user, username=form.cleaned_data['username'])
                a.signed_in="yes"
                a.save()
                return redirect("pastebin_app:userpage", random_id=q.sp_id)
            else:
                error="password is incorrect"
                return render(request, 'pastebin_app/index.html', {'form':form,'error':error,'randomurls':share,'latest':latest_th,'list1':list1,})
    return render(request, 'pastebin_app/index.html', {'form':form,'error':error,'randomurls':share,'latest':latest_th,'list1':list1,})

@never_cache
def post(request, random_url):
    template = "pastebin_app/paste.html"
    b=0
    try:
        form_detail = get_object_or_404(AddToDatabase, random_url=random_url)
        username_id=form_detail.username_id
        q=get_object_or_404(user, id=username_id)
        if q.signed_in=="yes":
            username=get_object_or_404(user, id=username_id).username
            paste=form_detail.data_text
            title=form_detail.data_title
            edit_p=form_detail.edit_p
            syntax=form_detail.syntax
            a=1
            if edit_p=="no":
                a=0
            if syntax=="html":
                b=1
            elif syntax=="css":
                b=2
            elif syntax=="c":
                b=3
            elif syntax=="c#":
                b=4
            elif syntax=="java":
                b=5
            elif syntax=="js":
                b=6
            elif syntax=="python":
                b=7
            elif syntax=="ruby":
                b=8
            elif syntax=="cpp":
                b=9
            else:
                b=0
            date=form_detail.created_on
            random_id=get_object_or_404(user, id=username_id).sp_id
            share_id=form_detail.share_id
            return render(request, template, {'paste':paste,'title':title,'username':username,'date':date,'random_id':random_id,'share_id':share_id,'edit_p':a,'random_url':random_url,'b':b,})
        else:
            return redirect('pastebin_app:home')
    except:
        idq=get_object_or_404(delinfo,random_url=random_url).username_id
        random_id=get_object_or_404(user,id=idq).sp_id
        return HttpResponseRedirect(reverse('pastebin_app:deleted', args=(random_id,)))
@never_cache
def mypost(request, random_id):
	q=get_object_or_404(user, sp_id=random_id)
	if q.signed_in=="yes":
		username=q.username
		username_id=q.id
		randomurl=AddToDatabase.objects.values_list('random_url',flat=True).filter(username_id=username_id)
		for i in randomurl:
			c=get_object_or_404(AddToDatabase,random_url=i)
			c.chk_exp()
		myposts=AddToDatabase.objects.values_list('data_text',flat=True).filter(username_id=username_id)
		titles=AddToDatabase.objects.values_list('data_title',flat=True).filter(username_id=username_id)
		randomurls=AddToDatabase.objects.values_list('random_url',flat=True).filter(username_id=username_id)
		template = "pastebin_app/mypost.html"
		return render(request, template, {'username':username,'myposts':myposts,'titles':titles,'randomurls':randomurls,'random_id':random_id,})
	else:
		return redirect('pastebin_app:home')
	
	
def share(request, random_url):
    template = "pastebin_app/share.html"
    b=0
    form_detail = get_object_or_404(AddToDatabase, share_id=random_url)
    paste=form_detail.data_text
    title=form_detail.data_title
    syntax=form_detail.syntax
    a=1
    if form_detail.edit_p=="no":
        a=0
    if syntax=="html":
        b=1
    elif syntax=="css":
        b=2
    elif syntax=="c":
        b=3
    elif syntax=="c#":
        b=4
    elif syntax=="java":
        b=5
    elif syntax=="js":
        b=6
    elif syntax=="python":
        b=7
    elif syntax=="ruby":
        b=8
    elif syntax=="cpp":
        b=9
    else:
        b=0
    username_id=form_detail.username_id
    username=get_object_or_404(user, id=username_id).username
    date=form_detail.created_on
    return render(request, template, {'paste':paste,'title':title,'username':username,'date':date,'b':b,'a':a,'random_url':form_detail.share_id,})
def s_edit(request, random_url):
	template = "pastebin_app/s_edit.html"
	form_detail = get_object_or_404(AddToDatabase, share_id=random_url)
	paste=form_detail.data_text
	title=form_detail.data_title
	syntax=form_detail.syntax
	username_id=form_detail.username_id
	username=get_object_or_404(user, id=username_id).username
	share_id2=form_detail.share_id
	date=form_detail.created_on
	form2= editf()
	if request.POST:
		form2=editf(request.POST)
		if form2.is_valid():
			entry=form2.save()
			return redirect('pastebin_app:share_edited', random_url=entry.share_id)
		else:
			form=editf()
	return render(request, template, {'paste':paste,'title':title,'username':username,'date':date,'share_id2':share_id2,'form':form2,})
def share_edited(request, random_url):
	c=get_object_or_404(editinfo, share_id=random_url)
	a=c.share_id2
	d=get_object_or_404(AddToDatabase, share_id=a)
	username=get_object_or_404(user, id=d.username_id).username
	original_date=d.created_on
	edited_date=c.created
	edited_text=c.edit_text
	title=c.data_title
	syntax=c.syntax
	b=0
	if syntax=="html":
		b=1
	elif syntax=="css":
		b=2
	elif syntax=="c":
		b=3
	elif syntax=="c#":
		b=4
	elif syntax=="java":
		b=5
	elif syntax=="js":
		b=6
	elif syntax=="python":
		b=7
	elif syntax=="ruby":
		b=8
	elif syntax=="cpp":
		b=9
	else:
		b=0
	template="pastebin_app/q.html"
	return render(request, template,{'username':username,'edited_date':edited_date,'original_date':original_date,'b':b,'paste':edited_text,'title':title,'original_id':a,})
@never_cache
def userpage(request, random_id):
	q=get_object_or_404(user, sp_id=random_id)
	if q.signed_in=="yes":
		username=q.username
		username_id=get_object_or_404(user,username=username).id
		randomurl=AddToDatabase.objects.values_list('random_url',flat=True).filter(username_id=username_id)
		for i in randomurl:
			c=get_object_or_404(AddToDatabase,random_url=i)
			c.chk_exp()
		randomurls=AddToDatabase.objects.values_list('random_url',flat=True).order_by('-created_on').filter(username_id=username_id)[:3]
		latest_th=AddToDatabase.objects.values_list('data_title',flat=True).order_by('-created_on').filter(username_id=username_id)[:3]
		
		share1=AddToDatabase.objects.values_list('share_id',flat=True).order_by('-created_on')
		for i in share1:
			c=get_object_or_404(AddToDatabase,share_id=i)
			c.chk_exp()
		share=AddToDatabase.objects.values_list('share_id',flat=True).order_by('-created_on')[:3]
		author=AddToDatabase.objects.values_list('username_id',flat=True).order_by('-created_on')[:3]
		list1=[]
		for i in author:
			v=get_object_or_404(user,id=i).username
			list1.append(v)
		latest_th1=AddToDatabase.objects.values_list('data_title',flat=True).order_by('-created_on')[:3]
		form=paste()
		if request.POST:
			form = paste(request.POST)
			if form.is_valid():
				entry=form.save()
				return redirect('pastebin_app:post', random_url=entry.random_url)
			else:
				form=paste()
		return render(request, 'pastebin_app/userpage.html', {'form':form,'username':username,'username_id':username_id,'latest_th':latest_th,'randomurls':randomurls,'random_id':random_id,'share':share,'latest_th1':latest_th1,'list1':list1,})
	else:
		return redirect('pastebin_app:home')
def signup(request):
    error=''
    form=Signup()
    latest_us=user.objects.values_list('username',flat=True)
    if request.POST:
        form = Signup(request.POST)
        if form.is_valid():
            if form.cleaned_data['username'] in latest_us:
                error="username already exists. pick another"
                return render(request, 'pastebin_app/signup.html', {'form':form,'error':error,})
            else:   
                if form.cleaned_data['password']==form.cleaned_data['npassword']:
                    entry = form.save()
                    return redirect('pastebin_app:confirmation')
                else:
                    error="password and repeat password donot match,check again"
                    return render(request, 'pastebin_app/signup.html', {'form':form,'error':error,})
        else:
            form=Signup()
    return render(request, 'pastebin_app/signup.html', {'form':form,'error':error,})
def confirmation(request):
	return render(request, 'pastebin_app/confirmation.html', {})
def logout(request, random_id):
	q=get_object_or_404(user, sp_id=random_id)
	q.signed_in="no"
	q.save()
	return redirect('pastebin_app:home')
@never_cache
def delete(request, random_url):
	q=get_object_or_404(AddToDatabase, random_url=random_url)
	a=get_object_or_404(user, id=q.username_id)
	delinfo.objects.create(
	random_url=random_url,
	username_id=q.username_id,
	)
	w=a.sp_id
	q.delete()
	return HttpResponseRedirect(reverse('pastebin_app:userpage', args=(w,)))
@never_cache
def edit(request, random_url):
	c=get_object_or_404(AddToDatabase, random_url=random_url)
	q=get_object_or_404(user, id=c.username_id)
	random_id=q.sp_id
	if q.signed_in=="yes":
		username=q.username
		username_id=get_object_or_404(user,username=username).id
		data_text=c.data_text
		data_title=c.data_title
		exp_time=c.exp_time
		edit_p=c.edit_p
		randomurls=AddToDatabase.objects.values_list('random_url',flat=True).order_by('-created_on').filter(username_id=username_id)[:3]
		latest_th=AddToDatabase.objects.values_list('data_title',flat=True).order_by('-created_on').filter(username_id=username_id)[:3]
		form=paste()
		if request.POST:
			form = paste(request.POST)
			if form.is_valid():
				c.data_text=form.cleaned_data['data_text']
				c.exp_time=form.cleaned_data['exp_time']
				c.edit_p=form.cleaned_data['edit_p']
				c.data_title=form.cleaned_data['data_title']
				c.save()
				return redirect('pastebin_app:post', random_url=c.random_url)
			else:
				form=paste()
		return render(request, 'pastebin_app/edit.html', {'form':form,'username':username,'username_id':username_id,'latest_th':latest_th,'randomurls':randomurls,'random_id':random_id,'data_text':data_text,'data_title':data_title,'exp_time':exp_time,'edit_p':edit_p,})
	else:
		return redirect('pastebin_app:home')
@never_cache
def deleted(request, random_id):
	template="pastebin_app/delete.html"
	q=get_object_or_404(user,sp_id=random_id)
	if q.signed_in=="yes":
		return render(request,template, {'random_id':random_id,'username':q.username,})
	else:
		return redirect('pastebin_app:home')

	