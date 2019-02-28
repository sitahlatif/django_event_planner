from django.shortcuts import render
from rest_framework import serializers
from events.models import Events

class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = [
       		'id',
        	'title',
        	'description',
        	'location',
        	'datetime',
        	'seats',
        	]
