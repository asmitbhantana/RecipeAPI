from django.contrib.auth import get_user_model,authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    '''Serializer for the user object'''
    class Meta:
        model = get_user_model()
        fields = ('email','password','name')
        '''Setting extra arguments for field variable'''
        extra_kwargs = {'password':{'write_only':True,'min_length':5}}


    def create(self,validated_data):
        '''Create new user with encrypted data and returns it'''
        return get_user_model().objects.create_user(**validated_data)

    def update(self,instance,validated_data):
        '''Update the user credentials
            Steps: `Remove password using pop
                    `call super for using default one along with the one we created
                    `set password of user
                    `sava the user
        '''
        password = validated_data.pop('password',None)
        user = super().update(instance,validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user
        

class AuthTokenSerializer(serializers.Serializer):
    '''Serializer for user auth object'''
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace=False #don't remove the whitespaces
    )

    def validate(self,attrs):
        '''Validate and auth user'''
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username = email,
            password=password
        )
        if not user:
            msg = {'Unable to authenticate with provided credentials'}
            raise serializers.ValidationError(msg,code='authentication')

        attrs['user']=user
        return attrs