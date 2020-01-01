from django.urls import path
from spchrcgntn import views as v


app_name = 'spchrcgntn'

urlpatterns = [
	path('',v.feedback,name='feedback'),
	path('select/',v.typeselection,name='typeselection'),
	path('speechinput/',v.speechinput,name='speechinput'),
	path('textinput/',v.textinput,name='textinput'),
	path('success/',v.successpage,name = 'successpage'),
	path('spprocess/',v.spprocess,name = 'spprocess'),
	]