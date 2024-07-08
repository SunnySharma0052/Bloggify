from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_id = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    image = models.ImageField(upload_to='profile_pics', default="defaultprofilepic.jpg")
    password_reset_code = models.CharField(max_length=6,default="")

    def __str__(self):
        return self.first_name
