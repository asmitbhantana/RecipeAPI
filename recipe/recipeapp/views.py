from rest_framework import viewsets,mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag,Ingredient
from recipeapp import serializers

class TagViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin):
    '''Manage the databases'''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    '''Thi is the object to be rendered by the api'''
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        '''Here is the custom filtering should be implemented'''
        '''get objects for the the currently auth user only'''
        return self.queryset.filter(user=self.request.user)

    def perform_create(self,serialzier):
        '''Create a new tag'''
        serializer.save(user=self.request.user)
    
class IngedrientViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    '''Manage indegridents in the db'''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngedrientSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')
        