from rest_framework import viewsets,mixins,status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag,Ingredient,Recipe
from recipeapp import serializers

from rest_framework.decorators import action
from rest_framework.response import Response

'''Making base class of tags and ingredients as they carry so much similarity'''
class RecipeAttr(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin):
    '''Manage the databases'''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        '''Here is the custom filtering should be implemented'''
        '''get the assigned only if assigned only is true in the path like url/?assigned_onluy=True'''
        assigned_only = bool(self.request.query_params.get('assigned_only'))
        queryset =self.queryset

        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)#reverse class can be accessed form django model using smaller first letter
        
        '''get objects for the the currently auth user only'''
        return queryset.filter(user=self.request.user).order_by('-name')
    
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


class RecipeViewSet(viewsets.ModelViewSet):
    '''Manage the recipe in database'''
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    '''Private function for changing id to tags and ingredient'''
    def _params_to_ints(self,qs):
        #convert a list of strings to a list integers
        '''string = 1,2,3 returns [1,2,3] pythonic way'''
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        '''Retrive The specific filter query set'''
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredient')
        queryset = self.queryset

        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tags_ids)#__ django syntax to filter foregin key
        
        if ingredients:
            ingredient_ids = _params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)
        
        '''Retrive the recipe for the user'''
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        '''Return appropriate serializer class'''
        if self.action=='retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action=='upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self,serializer):
        '''Create a new recipe'''
        serializer.save(user=self.request.user)
    
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self,request,pk=None):
        '''Upload image to the recipe'''
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

