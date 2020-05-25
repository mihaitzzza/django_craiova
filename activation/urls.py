from django.urls import path
from activation.views import activate

app_name = 'activation'

urlpatterns = [
    path('<str:token>/', view=activate, name='activate')
]
