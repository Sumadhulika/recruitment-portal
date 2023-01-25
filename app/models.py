from django.db import models



class qualifications(models.Model):

    qualifications=models.CharField(max_length=100,primary_key=True)

    def __str__(self):
         
         return self.qualifications



class skills(models.Model):

    skills=models.CharField(max_length=100,primary_key=True)

    def __str__(self):
         
         return self.skills


class appuser(models.Model):
    userid=models.AutoField(primary_key=True)
    email=models.EmailField(unique=True)
    username=models.CharField(max_length=45)
    password=models.CharField(max_length=8)
    contact=models.CharField(max_length=10)
    role=models.CharField(max_length=45)
    accesslable=models.CharField(max_length=2)


class CandidateDetails(models.Model):
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    email=models.EmailField(unique=True)
    qualifications=models.ForeignKey(qualifications,on_delete=models.CASCADE)
    skills = models.ManyToManyField(skills)    
    experience=models.IntegerField()
    contact=models.CharField(max_length=10)
    address=models.CharField(max_length=100)
    date=models.DateField(null=True)





