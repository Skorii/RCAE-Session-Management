from django.urls import path
from inscription import views

app_name = 'inscription'
urlpatterns = [
    path('section', views.selection_sport, name='sport_selection'),
    path('session', views.inscription, name='inscription'),
    path('validation', views.validation, name='validation'),
    path('result', views.registration_result, name='result'),
]
