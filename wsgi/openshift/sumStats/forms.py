from django import forms

from sumStats.models import Genotype
from django.db import models

class StatForm(forms.Form):
    allModels = models.get_models(models.get_app('sumStats'))[1:]
    allModelNames=[]
    for model in allModels:
        modName = model._meta.verbose_name_raw.replace(" ","")
        allModelNames.append((modName, modName))
    modelName=forms.ChoiceField(allModelNames, label='')

