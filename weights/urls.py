from django.urls import path
from . import views
from .views import weight_list,weight_entry_view

urlpatterns = [
	
	path('add-entry', weight_entry_view, name='weight-entry'),  # connects view to form
	path('database', weight_list, name='weight_list')
]