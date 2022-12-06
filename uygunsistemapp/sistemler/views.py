from django.shortcuts import render
from .models import Sistem
import pandas as pd



def sistemler(request):

    data = {
        "df":Sistem.objects.all()
    }
    return render(request,"index.html",context=data)