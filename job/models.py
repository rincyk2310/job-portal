from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class studentUser(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=15,null=True)
    image = models.ImageField(upload_to='student_images/', null=True, blank=True)
    gender=models.CharField(max_length=10,null=True)
    type=models.CharField(max_length=15,null=True)

    def _str_(self):
        return self.user.username


class Recruiter(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=15,null=True)
    image=models.FileField(null=True)
    gender=models.CharField(max_length=10,null=True)
    company = models.CharField(max_length=100, null=True)
    type=models.CharField(max_length=15,null=True)
    status = models.CharField(max_length=20 ,null=True)

    def _str_(self):
        return self.user.username

class Job(models.Model):
    recruiter=models.ForeignKey(Recruiter,on_delete=models.CASCADE)
    start_date=models.DateField()
    end_date=models.DateField()
    title=models.CharField(max_length=100)
    salary = models.FloatField()
    image=models.FileField()
    description = models.CharField(max_length=300)
    experience = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    skills = models.CharField(max_length=100)
    creationdate = models.DateField()


    def _str_(self):
        return self.title



class Apply(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(studentUser, on_delete=models.CASCADE)
    resume = models.FileField(null=True, blank=True, upload_to='resumes/')
    apply_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.job.title if self.job else 'No Job'}"



