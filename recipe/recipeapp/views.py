from rest_framework import viewsets,mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag,Ingredient
from recipeapp import serializers


'''Making base class of tags and ingredients as they carry so much similarity'''
class RecipeAttr(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin):
    '''Manage the databases'''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        '''Here is the custom filtering should be implemented'''
        '''get objects for the the currently auth user only'''
        return self.queryset.filter(user=self.request.user).order_by('-name')
    
    def perform_create(self,serializer):
        '''Create a new ingridents'''
        serializer.save(user=self.request.user)


class TagViewSet(RecipeAttr):

    '''Thi is the object to be rendered by the api'''
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(RecipeAttr):

    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


    
    

