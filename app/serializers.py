from rest_framework import serializers
from app.models import *


class SubjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'subjectCode', 'subjectName',
                  'numberOfClasses', 'created']
