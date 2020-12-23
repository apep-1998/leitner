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
    path('addbox/', login_required(AddBox.as_view()), name="add_box"),
    path('add2box/<int:box_pk>/', login_required(Add2Box.as_view())),
    path('removebox/<int:box_pk>/', remove_box),
    path('copybox/<int:box_pk>/', copy_box),
    # path('removefrombox/<int:box_pk>/', login_required(RemoveFromBox.as_view())),
    path('boxlist/', login_required(BoxList.as_view()), name="box_list"),
    path('wordmean/<str:word>/', get_means, name="wordmeans"),

    path('meanBoxList/', login_required(MeanBoxList.as_view()), name="mean box list"),
    path('dictationBoxList/', login_required(DictationBoxList.as_view()), name="Dictation box list"),
    path('test/<int:box_pk>/', login_required(TestBox.as_view()), name="test box"),
    path('review/<int:box_pk>/', login_required(ReviewBox.as_view()), name="review box"),
]