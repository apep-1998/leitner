from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime, timedelta
import pytz
from words.models import *
from django.contrib.auth.models import User
from django.shortcuts import redirect

@login_required
def index(request):
    return redirect("index")

