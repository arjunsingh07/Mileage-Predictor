from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from . import models

# Create your views here.

import joblib

reloadmodel = joblib.load('./models/RFmodel.pkl')


def index(request):

    temp={}
    temp['cylinders']=8
    temp['displacement']=307
    temp['horsepower']=130
    temp['weight']=3504
    temp['acceleration']=12
    temp['model_year']=70
    temp['origin']=1
    context = {'temp' : temp }
    return render(request, 'headerPage.html', context)


def predictions(request):
    print(request)
    if request.method == 'POST':
        temp={}
        temp['cylinders']=request.POST.get('cylinderVal')
        temp['displacement']=request.POST.get('dispVal')
        temp['horsepower']=request.POST.get('hrsPwrVal')
        temp['weight']=request.POST.get('weightVal')
        temp['acceleration']=request.POST.get('accVal')
        temp['model_year']=request.POST.get('modelVal')
        temp['origin']=request.POST.get('originVal')

        models.Mileage.objects.create(cylinders=temp['cylinders'],displacement=temp['displacement'],horsepower=temp['horsepower'],weight=temp['weight'], acceleration=temp['acceleration'],model=temp['model_year'], origin=temp['origin'])


        temp2=temp.copy()
        temp2['model year'] = temp['model_year']
        del temp2['model_year']


    testdata=pd.DataFrame({'x':temp2}).transpose()
    scoreval = reloadmodel.predict(testdata)[0]
    context = {
        'scoreval': scoreval,
        'temp' : temp
        
    }

    return render(request, 'headerPage.html',context)

 