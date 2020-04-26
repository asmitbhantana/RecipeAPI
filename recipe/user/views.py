from rest_framework import generics,authentication,permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer

class CreateUserView(generics.CreateAPIView):
    '''Create a new user in the system'''
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    '''Create a new auth token for user'''
    serializer_class = AuthTokenSerializer
    '''Making the browser viewable token getting and setting platform'''
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    '''Manage the authenticated user'''
    serializer_class = UserSerializer
    '''User must just be logged in'''
    authentication_classes = [authentication.TokenAuthentication,]
    '''required permission is just login'''
    permission_classes = [permissions.IsAuthenticated,]
    '''this overrides the features of getting object and 
        makes the retrive for auth user only
    '''
    def get_object(self):
        '''Auth user is retrived with the help of Token of user'''
        return self.request.user
