"""
URL configuration for NewsPaper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path # не забываем импортировать include

urlpatterns = [
    path('admin/', admin.site.urls),
# далее добавляем строку с flatpages
    path('pages/', include('django.contrib.flatpages.urls')),
# Подключаем наше приложение и не забываем создать urls.py в приложении/папке news
# делаем так, чтобы все адреса из нашего приложения (news/urls.py) сами автоматически подключались, когда мы их добавим.
    path('', include('news.urls')), # news - должен быть этот адрес из задания
    path('accounts/', include('allauth.urls')),
    path('accounts/cabinet/', include('accounts.urls')),
]
