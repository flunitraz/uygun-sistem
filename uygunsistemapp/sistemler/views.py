from django.shortcuts import render

import pandas as pd



def sistemler(request):
    df = pd.read_csv("../data/data.csv")
    df.drop("Unnamed: 0", axis=1, inplace=True)
    mydict = {
        "df": df.to_html()
    }
    return render(request,"index.html",context=mydict)