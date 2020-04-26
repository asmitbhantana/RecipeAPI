from django.urls import path,include
from rest_framework.routers import DefaultRouter

from recipeapp import views
'''Automatically register default urls'''
router = DefaultRouter()
router.register('tags',views.TagViewSet)
router.register('ingredients',views.IngedrientViewSet)

app_name ='recipe'

urlpatterns=[
    path('',include(router.urls)),
]