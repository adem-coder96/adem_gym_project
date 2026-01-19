from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, CoursViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('cours', CoursViewSet)

urlpatterns = router.urls
