from django.db import models

# Create your models here.
from django.db import models

class WeightEntry(models.Model):
	weight_id = models.CharField(max_length=100)
	scale_id = models.CharField(max_length=10, default='1')
	vehicle_no = models.CharField(max_length=100)
	party_type = models.CharField(max_length=50, default='CLIENT')
	client_name = models.CharField(max_length=100)
	print_date = models.DateField()
	challan_no = models.CharField(max_length=100, blank=True)
	item_name = models.CharField(max_length=100)
	qty = models.CharField(max_length=100, blank=True)
	load_weight = models.DecimalField(max_digits=10, decimal_places=2)
	load_weight_date = models.DateTimeField()
	unload_weight = models.DecimalField(max_digits=10, decimal_places=2)
	unload_weight_date = models.CharField(max_length=100, blank=True)
	deduct = models.CharField(max_length=10, default='0')
	net_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	driver_contact = models.CharField(max_length=100, blank=True)
	
	def __str__(self):
		return f"{self.vehicle_no} - {self.client_name}"