from .views import PersonViewSet, PostViewSet, GroupViewSet
from django.conf.urls import url, include
from rest_framework import routers
#from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('people', PersonViewSet)
router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)
#comments_router = routers.NestedDefaultRouter(router, 'posts', lookup='comments')

urlpatterns = [
    url(r'^', include(router.urls)),
#    url(r'^', include(post_router.urls)),
]
