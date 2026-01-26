from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from datetime import date
from .models import Job, Recruiter

# Create your views here.
def index(request):
    return render(request,'index.html')
def admin_login(request):
    error=""
    if request.method == "POST":
        u = request.POST.get('uname')
        p = request.POST.get('pwd')
        user=authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error="yes"
    d={'error':error}
    return render(request,'admin_login.html',d)
def user_login(request):
    error=""
    if request.method == "POST":
        u=request.POST['uname'];
        p=request.POST['pwd'];
        user=authenticate(username=u,password=p)
        if user :
            try:
                user1 = studentUser.objects.get(user=user)
                if user1.type == "student":
                    login(request,user)
                    error="no"
                else:
                    error="yes"
            except:
                error="yes"
        else:
            error="yes"
    d={'error':error}
    return render(request,'user_login.html',d)
def recruiter_login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname'];
        p = request.POST['pwd'];
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = Recruiter.objects.get(user=user)
                if user1.type == "recruiter" and user1.status!="pending":
                    login(request, user)
                    error = "no"
                else:
                    error = "not"
            except:
                error = "yes"
        else:
            error = "yes"
    d = {'error': error}
    return render(request,'recruiter_login.html',d)
def recruiter_signup(request):
    error = ""
    if request.method == "POST":
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        c = request.POST['contact']
        g = request.POST['gender']
        com = request.POST['company']
        try:
            user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
            Recruiter.objects.create(user=user, mobile=c, image=i, gender=g,company=com, type="recruiter",status="pending")
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request,'recruiter_signup.html',d)
def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    rcount = Recruiter.objects.all().count()
    scount = studentUser.objects.all().count()
    d={'rcount':rcount,'scount':scount}
    return render(request,'admin_home.html',d)




def user_home(request):
    # 🔐 login check
    if not request.user.is_authenticated:
        return redirect('user_login')

    user = request.user

    # ✅ auto-create student profile if not exists
    student, created = studentUser.objects.get_or_create(user=user)

    error = None

    if request.method == "POST":
        # form values
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        contact = request.POST.get('mobile')
        gender = request.POST.get('gender')

        # update Django User table
        user.first_name = fname
        user.last_name = lname
        user.save()

        # update studentUser table
        student.mobile = contact
        student.gender = gender
        student.save()

        try:
            student.save()
            error = "no"
        except Exception:
            error = "yes"
        try:
            i = request.FILES['image']
            student.image = i
            student.save()
            error = "no"
        except:
            pass

    context = {
        'student': student,
        'error': error
    }

    return render(request, 'user_home.html', context)



def recruiter_home(request):
    # 🔐 login check
    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    user = request.user
    recruiter = Recruiter.objects.filter(user=user).first()

    # 🚫 recruiter profile not created yet
    if not recruiter:
        return redirect('recruiter_profile')  # or recruiter_signup

    error = None

    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        contact = request.POST.get('contact')
        gender = request.POST.get('gender')

        # update user
        user.first_name = fname
        user.last_name = lname
        user.save()

        # update recruiter
        recruiter.mobile = contact
        recruiter.gender = gender

        # image upload (optional)
        if 'image' in request.FILES:
            recruiter.image = request.FILES['image']

        try:
            recruiter.save()
            error = "no"
        except Exception:
            error = "yes"

    context = {
        'recruiter': recruiter,
        'error': error
    }

    return render(request, 'recruiter_home.html', context)




def Logout(request):
    logout(request)
    return redirect('index')

    return render(request,'user_home.html')
def user_signup(request):
    error=""
    if request.method=="POST":
        f=request.POST['fname']
        l=request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        c = request.POST['contact']
        g = request.POST['gender']
        try:
            user = User.objects.create_user(first_name=f,last_name=l,username=e,password=p)
            studentUser.objects.create(user=user,mobile=c,image=i,gender=g,type="student")
            error="no"
        except:
            error= "yes"
    d={'error':error}
    return render(request,'user_signup.html',d)



def view_users(request):
    # Admin authentication check
    if not request.user.is_authenticated:
        return redirect('admin_login')

    # Fetch all student users
    data = studentUser.objects.all()

    context = {
        'data': data
    }

    return render(request, 'view_users.html', context)


def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    student=User.objects.get(id=pid)
    student.delete()
    return redirect('view_users')

def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.filter(status="pending")
    d={'data':data}
    return render(request,'recruiter_pending.html',d)

def change_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""
    recruiter=Recruiter.objects.get(id=pid)
    if request.method == "POST":
        s=request.POST['status']
        recruiter.status=s
        try:
            recruiter.save()
            error="no"
        except:
            error="yes"

    recruiter={'recruiter':recruiter,'error':error}
    return render(request,'change_status.html',recruiter)

def recruiter_accepted(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status='Accept')
    return render(request, 'recruiter_accepted.html', {'data': data})
def recruiter_rejected(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.filter(status="Reject")
    d={'data':data}
    return render(request,'recruiter_rejected.html',d)
def recruiter_all(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.all()
    d={'data':data}
    return render(request,'recruiter_all.html',d)

def delete_recruiter(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    recruiter=User.objects.get(id=pid)
    recruiter.delete()
    return redirect('recruiter_all')

def change_pwdadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""
    if request.method == "POST":
        o=request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(o):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="no"
        except:
            error="yes"

    d={'error':error}
    return render(request,'change_pwdadmin.html',d)

def change_pwduser(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    if request.method == "POST":
        o=request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(o):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="no"
        except:
            error="yes"

    d={'error':error}
    return render(request,'change_pwduser.html',d)

def change_pwdrecruiter(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""
    if request.method == "POST":
        o=request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(o):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="no"
        except:
            error="yes"

    d={'error':error}
    return render(request,'change_pwdrecruiter.html',d)

def add_job(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""
    if request.method=="POST":
        jt=request.POST['title']
        sd=request.POST['startdate']
        ed = request.POST['enddate']
        sal = request.POST['salary']
        lo = request.FILES['image']
        exp = request.POST['experience']
        loc = request.POST['location']
        skills = request.POST['skills']
        des = request.POST['description']
        user=request.user
        recruiter = Recruiter.objects.get(user=user)
        try:
            Job.objects.create(recruiter=recruiter,start_date=sd,end_date=ed,title=jt,salary=sal,image=lo,description=des,experience=exp,location=loc,skills=skills,creationdate=date.today())
            error="no"
        except:
            error= "yes"
    d={'error':error}
    return render(request,'add_job.html',d)

def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user = request.user
    recruiter = Recruiter.objects.get(user=user)
    job=Job.objects.filter(recruiter=recruiter)
    d={'job':job}
    return render(request,'job_list.html',d)

def edit_job(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""
    job=Job.objects.get(id=pid)
    if request.method=="POST":
        jt=request.POST['title']
        sd=request.POST['startdate']
        ed = request.POST['enddate']
        sal = request.POST['salary']
        # lo = request.FILES['image']
        exp = request.POST['experience']
        loc = request.POST['location']
        skills = request.POST['skills']
        des = request.POST['description']
        job.title=jt
        job.salary = sal
        job.experience = exp
        job.location = loc
        job.skills = skills
        job.description=des

        try:
            job.save()
            error="no"
        except:
            error= "yes"
        if sd:
            try:
               job.start_date=sd
               job.save()
            except:
                pass
        else:
            pass
        if ed:
            try:
               job.end_date=ed
               job.save()
            except:
                pass
        else:
            pass
    d={'error':error,'job':job}
    return render(request,'edit_job.html',d)

def change_companylogo(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""
    job=Job.objects.get(id=pid)
    if request.method=="POST":
        lo = request.FILES['image']
        job.image=lo
        try:
            job.save()
            error="no"
        except:
            error= "yes"

    d={'error':error,'job':job}
    return render(request,'change_companylogo.html',d)

def latest_jobs(request):
    job=Job.objects.all().order_by('start_date')
    d={'job':job}
    return render(request,'latest_jobs.html',d)

def user_latestjob(request):
    job = Job.objects.all().order_by('start_date')
    user = request.user
    student = studentUser.objects.get(user=user)

    # Only get Apply objects with a valid job
    data = Apply.objects.filter(student=student, job__isnull=False)
    li = [i.job.id for i in data]

    context = {'job': job, 'li': li}
    return render(request, 'user_latestjob.html', context)



def job_detail(request,pid):
    job=Job.objects.get(id=pid)
    d={'job':job,}
    return render(request,'job_detail.html',d)


def applyjob(request,pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    user=request.user
    student=studentUser.objects.get(user=user)
    job = Job.objects.get(id=pid)
    date1=date.today()
    if job.end_date < date1:
        error="close"
    elif job.start_date > date1:
        error="notopen"
    else:
        if request.method == "POST":
            resume = request.FILES['resume']
            Apply.objects.create(student=student,job=job,resume=resume,apply_date=date.today())
            error="done"
    d={'error':error}
    return render(request,'applyjob.html',d)

def applied_candidates(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    data=Apply.objects.all()


    d={'data':data}
    return render(request,'applied_candidates.html',d)

def contact(request):
    return render(request,'contact.html')



