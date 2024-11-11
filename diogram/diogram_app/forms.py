from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['spravki', 'post_cpgu', 'treb_mil', 'vlitiya_kart', 'aktual', 'post_prekr', 'post_objavl', 'istreb']
