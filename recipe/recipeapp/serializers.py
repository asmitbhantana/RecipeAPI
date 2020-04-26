from rest_framework import serializers
from core.models import Tag,Ingredient

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        mode=Tag
        fields = ('id','name')
        read_only_fields = ('id',)


class IngedrientSerializer(serializers.ModelSerializer):

    class Meta:
        mode=Ingredient
        fields = ('id','name')
        read_only_fields = ('id',)