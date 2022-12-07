from django.shortcuts import render
from .models import Sistem
import pandas as pd



def sistemler(request):

    data = {
        "df":Sistem.objects.all(),
        "desc":Sistem.objects.all().order_by('-fiyat'),
        "asc":Sistem.objects.all().order_by('fiyat')
    }
    return render(request,"index.html",context=data)