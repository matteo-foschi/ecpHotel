from django.conf import settings
from django.db import models
from django.utils import timezone
from .utils import sendTransaction
import hashlib

class reportData(models.Model):
     produced_energy_in_watt = models.IntegerField(null=True)
     consumed_energy_in_watt = models.IntegerField(null=True)
     report_date = models.DateTimeField(default=timezone.now)
     hash = models.CharField(max_length=32, default=None, null=True, blank=True)
     txId = models.CharField(max_length=66, default=None, null=True, blank=True)

     def publish(self):
         self.save()

     def __str__(self):
          return self.report_date.strftime("%Y-%m-%d")

     def writeOnChain(self):
          self.hash = hashlib.sha256(str(self.produced_energy_in_watt).encode("utf-8")).hexdigest() + hashlib.sha256(
               str(self.consumed_energy_in_watt).encode("utf-8")).hexdigest()
          self.txId = sendTransaction(self.hash)
          self.save()



