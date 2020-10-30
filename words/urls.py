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
from words.views import MeanTest, addall, SpellTest, MeanReview, SpellReview, AddWord
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('mean', login_required(MeanTest.as_view())),
    path('meanreview/<int:page>', login_required(MeanReview.as_view())),
    path('meanreview/', login_required(MeanReview.as_view())),
    path('spell', login_required(SpellTest.as_view())),
    path('spellreview', login_required(SpellReview.as_view())),
    path('addword', login_required(AddWord.as_view())),
    path('addall', addall),
]