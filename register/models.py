from __future__ import unicode_literals
import datetime
import django.utils.timezone
from django.db import models

# Create your models here.
class Logintime(models.Model):
	empid = models.CharField(max_length=6)
	rdate = models.DateField(default=django.utils.timezone.now)#(default=datetime.date.today())
	intime = models.TimeField()
	outtime = models.TimeField()
	wtime = models.FloatField(default=0)
	nwtime = models.FloatField(default=0)

	def __unicode__(self):
		return self.empid

	def __str__(self):
		return self.empid 