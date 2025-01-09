from django.db import models


#model with email and datetime of getting pixel drawing ability
class time_adress(models.Model):
    email = models.CharField(max_length=300)
    due = models.DateTimeField()
