"""qootrade URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from fundvis import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', views.hello),
    path('hw1/', views.hw1),
    path('hw2/', views.hw2),
    path('MASystem/<fundcode>/', views.MASystem),
    path('sectorfunds/', views.sectorFunds),
    path('msg/<name>/<age>/', views.msg),
    path('movieclassification/', views.movieClassification),
    path('moviebar/', views.movieBar),
    path('worldmap/', views.worldmap),
    # path('unemploymentrate/', views.unemploymentRate),
    path('', views.globalData),
    path('vix/', views.vix),
    path('globaldata/', views.globalData),
    path('stockindex/', views.stockIndex),
    path('nsdk/', views.nsdkMethod),
    path('industrymoneyflow/', views.industry)
]
