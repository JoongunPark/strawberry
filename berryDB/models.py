from django.db import models

class Reservation(models.Model):
    def __unicode__(self):
        return self.name + '_' + str(self.studentID) + "_" + self.club + "_" + self.date
    reserveID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    studentID = models.IntegerField(max_length=255)
    numRolls = models.IntegerField(max_length=11)
    numBerries = models.IntegerField(max_length=15)
    club = models.CharField(max_length=30)
    phoneNum = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    date = models.CharField(max_length=30,null=True)