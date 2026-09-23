from .views import DocumentViewSet, SearchViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("documents", DocumentViewSet)
router.register("search", SearchViewSet, basename="search")

urlpatterns = router.urls
