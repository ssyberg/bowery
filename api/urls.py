from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

# I think convention would normally be plural routes but the
# given spec had singluar "request"
router.register(r'image', views.ImageViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
