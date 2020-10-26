from django.urls import path
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
#router.register(<prefix>, <viewset>, <basename>)

urlpatterns = [
   #path(<route>, <view>),
]
urlpatterns += router.urls

