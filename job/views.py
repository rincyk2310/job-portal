from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from datetime import date
from .models import Job, Recruiter ,Contact
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse


# Create your views here.

def index(request):
    jobs = Job.objects.all()
    titles = Job.objects.values_list('title', flat=True).distinct()
    locations = Job.objects.values_list('location', flat=True).distinct()
    return render(request,'index.html',{'jobs':jobs,'locations':locations,'titles':titles})


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

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    rcount = Recruiter.objects.all().count()
    scount = studentUser.objects.all().count()
    # Recruiter status counts
    pending = Recruiter.objects.filter(status="pending").count()
    accepted = Recruiter.objects.filter(status="Accept").count()
    rejected = Recruiter.objects.filter(status="Reject").count()

    # Total jobs posted
    jobcount = Job.objects.all().count()

    d={'rcount':rcount,
       'scount':scount,
       'pending': pending,
        'accepted': accepted,
        'rejected': rejected,
        'jobcount': jobcount}
    return render(request,'admin_home.html',d)


def user_login(request):
    error=""
    if request.method == "POST":
        u=request.POST['uname']
        p=request.POST['pwd']
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
        u = request.POST['uname']
        p = request.POST['pwd']
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




def user_home(request):
    #  login check
    if not request.user.is_authenticated:
        return redirect('user_login')

    user = request.user

    #  auto-create student profile if not exists
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
    #  login check
    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    user = request.user
    recruiter = Recruiter.objects.filter(user=user).first()

    #  recruiter profile not created yet
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

    if not request.user.is_authenticated:
        return redirect('user_login')

    jobs = Job.objects.all().order_by('-start_date')

    student = studentUser.objects.get(user=request.user)

    #  Applied jobs safely
    applications = Apply.objects.filter(student=student)

    status_dict = {}

    for a in applications:
        if a.job is not None:   # ✅ Prevent NoneType error
            status_dict[a.job.id] = a.status

    #  Saved jobs
    saved_jobs = SavedJob.objects.filter(student=student)
    saved_list = [i.job.id for i in saved_jobs if i.job is not None]

    context = {
        'job': jobs,
        'status_dict': status_dict,
        'saved_list': saved_list
    }

    return render(request, 'user_latestjob.html', context)


def job_detail(request,pid):
    job=Job.objects.get(id=pid)
    d={'job':job,}
    return render(request,'job_detail.html',d)



def applyjob(request, pid):

    if not request.user.is_authenticated:
        return redirect('user_login')

    error = ""

    try:
        user = request.user
        student = studentUser.objects.get(user=user)
        job = Job.objects.get(id=pid)

        today = date.today()

        #  Already applied check
        if Apply.objects.filter(student=student, job=job).exists():
            error = "already"

        #  Job date validation
        elif job.end_date < today:
            error = "close"

        elif job.start_date > today:
            error = "notopen"

        else:

            if request.method == "POST":

                #  Resume check
                if 'resume' not in request.FILES:
                    error = "resume_missing"

                else:
                    resume = request.FILES['resume']

                    #  Save Application
                    Apply.objects.create(
                        student=student,
                        job=job,
                        resume=resume,
                        apply_date=date.today()
                    )

                    #  Email Notification
                    if request.user.email:
                        send_mail(
                            'Job Application Confirmation',
                            f'''Hi {student.user.username},

                        You have successfully applied for {job.title} job.

                        Thank you for using our Job Portal.''',

                            settings.EMAIL_HOST_USER,

                            [student.user.email, 'projectdemo347@gmail.com'],  #  Add demo mail

                            fail_silently=False,
                        )

                    error = "done"

    except Exception as e:
        print("Error:", e)

    return render(request, 'applyjob.html', {'error': error})


def mail_sent(request):

    send_mail(
        'Job Application Confirmation',

        '''Hi User,

You have successfully applied for the job.

Thank you for using our Job Portal.''',

        settings.EMAIL_HOST_USER,

        ['projectdemo347@gmail.com'],

        fail_silently=False,
    )

    return HttpResponse("Mail sent check inbox")



def applied_candidates(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    data=Apply.objects.all()

    d={'data':data}
    return render(request,'applied_candidates.html',d)


def update_status(request, pid, status):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    application = Apply.objects.get(id=pid)

    # Security check (VERY IMPORTANT)
    if application.job.recruiter.user != request.user:
        return redirect('applied_candidates')

    application.status = status
    application.save()

    return redirect('applied_candidates')



def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        Contact.objects.create(
            name=name,
            email=email,
            message=message
        )

    return render(request,'contact.html')


def view_messages(request):
    messages = Contact.objects.all()
    return render(request,'view_messages.html',{'messages':messages})


def search_jobs(request):

    title = request.GET.get('title','')
    location = request.GET.get('location','')

    job = Job.objects.all().order_by('-start_date')

    if title or location:
        job = job.filter(
            title__icontains=title,
            location__icontains=location
        )

    return render(request,"latest_jobs.html",{
        "job":job
    })


def about(request):
    return render(request,'about.html')

def services(request):
    return render(request,'services.html')



def save_job(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')

    student = studentUser.objects.get(user=request.user)
    job = Job.objects.get(id=pid)

    SavedJob.objects.get_or_create(student=student, job=job)

    return redirect('user_latestjob')



def saved_jobs(request):
    student = studentUser.objects.get(user=request.user)
    jobs = SavedJob.objects.filter(student=student)

    return render(request, 'saved_jobs.html', {'jobs': jobs})

def remove_savedjob(request,id):
    job = SavedJob.objects.get(id=id)
    job.delete()
    return redirect('saved_jobs')


def delete_job(request, pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    job = Job.objects.get(id=pid)
    job.delete()

    return redirect('job_list')