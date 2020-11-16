from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Employee(models.Model):
    employee_id = models.PositiveIntegerField()
    city = models.CharField(max_length = 200,default= 'New Delhi')
    user_name = models.ForeignKey(User, on_delete = models.DO_NOTHING, null=True, blank=True)


    def __str__(self):
        return f'{self.employee_id}, {self.first_name} {self.last_name}'