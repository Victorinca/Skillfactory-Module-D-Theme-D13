from django.urls import path
from .views import CabinetView
from .views import upgrade_me, user_profile

app_name = 'accounts'
urlpatterns = [
   path('', CabinetView.as_view(), name='cabinet'),
   path('upgrade/', upgrade_me, name='upgrade')
]
