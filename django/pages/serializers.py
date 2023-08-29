from rest_framework import serializers
from .models import Movie, Actor

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['actor'] = instance.actor.to_dict() if instance.actor else None
        data['director'] = instance.director.to_dict() if instance.director else None
        
        return data


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'
