from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'user', 'spravki', 'post_cpgu', 'treb_mil', 'vlitiya_kart', 'aktual',
                  'post_prekr', 'post_objavl', 'istreb', 'created_at']
