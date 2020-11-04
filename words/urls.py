"""leitner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from words.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', index_view, name="index"),
    path('addcat/', login_required(AddCat.as_view()), name="add cat"),
    # path('listcat/', login_required(ListCat.as_view()), name="list cat"),
    
    path('addword/', login_required(AddWord.as_view()), name="add word"),
    path('addbox/', login_required(AddBox.as_view()), name="add box"),
    path('add2box/', login_required(Add2Box.as_view()), name="add item box"),
    path('meanboxlist/', login_required(MeanBoxList.as_view()), name="mean box list"),
    path('spellboxlist/', login_required(SpellBoxList.as_view()), name="spell box list"),
    path('test/<int:boxnumber>/', login_required(TestBox.as_view()), name="test box"),
]