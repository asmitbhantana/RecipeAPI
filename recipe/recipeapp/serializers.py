from rest_framework import serializers
from core.models import Tag,Ingredient,Recipe

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model=Tag
        fields = ('id','name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model=Ingredient
        fields = ('id','name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    '''Serialize a recipe and related keys
        This is the primary key related field 
        that just returns the needed ingredient and tags'''
    ingredients = serializers.PrimaryKeyRelatedField(
            many=True,
            queryset=Ingredient.objects.all(),
        )
    tags = serializers.PrimaryKeyRelatedField(
            many=True,
            queryset=Tag.objects.all(),
        )
    

    class Meta:
        model = Recipe
        fields=(
                'id','title','ingredients',
                'tags','time_minutes',
                'price','link'
            )
        '''This is done to make sure that the user just can't update the id field
            It's good practise to not to change the primary key'''
        read_only_fields=('id',)

    def update(self,instance,validated_data):
        '''Update the recipe credentials
            Steps: `Remove values using pop
                    `call super for using default one along with the one we created
                    `set new recipe
                    `sava the recipe
        '''
        recipe = super().update(instance,validated_data)
        
        if recipe:
            recipe.save()
        return recipe


class RecipeDetailSerializer(RecipeSerializer):
    '''Serialize the recipe details'''
    ingredients = IngredientSerializer(many=True,read_only=True)
    tags = TagSerializer(many=True,read_only=True)
