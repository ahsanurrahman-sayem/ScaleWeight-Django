from django import forms

class WeightForm(forms.Form):
	weight_id = forms.CharField(label='Weight ID')
	vehicle_no = forms.CharField(label='Vehicle Number')
	client_name = forms.CharField(label='Client Name')
	item_name = forms.CharField(label='Item Name')
	load_weight = forms.DecimalField(label='Load Weight')
	unload_weight = forms.DecimalField(label='Unload Weight')