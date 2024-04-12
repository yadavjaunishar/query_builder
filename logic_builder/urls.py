from django.urls import path
from . import views

urlpatterns = [
    path('',views.logic_builder, name='logic_builder'),
    path('savelogicbuilder',views.savelogicbuilder, name='savelogicbuilder'),
    path('getparameter/',views.getparameter, name='getparameter'),
    path('calculation/',views.calculation, name='calculation'),
]
