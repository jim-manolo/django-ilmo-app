from django import forms
import json
import os
from .utils import FieldGenerator

def get_form(form_name):
    with open('./ilmo-app/ilmo/form_templates/' + form_name + '.json','r') as template:
        fields = json.load(template)
        fg = FieldGenerator(fields)
        return type('form',(forms.Form,),fg.formfields)
