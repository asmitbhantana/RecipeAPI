from rest_framework import viewsets,mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag
from recipeapp import serializers

class TagViewSet(viewsets.GenericViewSet,mixins.ListModelMixin):
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