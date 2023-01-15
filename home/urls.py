from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page,name='home_page'),
    path('analytics_page/',views.analytics_page,name="analytics_page"),
    path('survey/', views.survey, name="survey_page"),
    path('results_page/',views.results_page,name="results_page"),
    path('engineering/',views.engineering,name="engineering"),
    path('medical/',views.medical,name="medical"),
    path('management/',views.management,name="management"),
    path('design/',views.design,name="design"),
    path('science/',views.science,name="science"),
    path('law/',views.law,name="law"),
    path('list_all_clgs/',views.list_all_clgs,name="list_all_clgs"),
]



