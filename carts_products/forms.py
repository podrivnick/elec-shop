from django import forms
from django.contrib.auth import get_user_model

class FormOpinion(forms.Form):
    id_product = forms.IntegerField()
    slug_product = forms.CharField()
    message = forms.Textarea()

    class Meta:
        fields = ['id_product',
                  'slug_product',
                  'message',
                  ]
