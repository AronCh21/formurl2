from django.db import models
import datetime


x = datetime.datetime.now()


class Beneficiary(models.Model):
    accNo = models.AutoField(primary_key=True)
    byOrder = models.CharField(max_length=500)
    receiverNo = models.CharField(max_length=200)
    country = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    nationality = models.CharField(max_length=500, blank=True)

class Sender(models.Model):
    #Senders Info
    sender = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    senderNo = models.CharField(max_length=200)
    idNo = models.CharField(max_length=500)
    porpuse = models.CharField(max_length=500)
    

class Receipt(models.Model):
    #--------------------
    receiver = models.CharField(max_length=10000)
    sender = models.CharField(max_length=10000)
    #--------------------
    time = models.CharField(max_length=500)
    valueDate = models.CharField(max_length=500)
    #Payment Info
    payoutAmtUsd = models.CharField(max_length=500)
    rate = models.CharField(max_length=500)
    charge = models.CharField(max_length=500, blank=True)
    #Getting Password
    password = models.CharField(max_length=500, blank=True)