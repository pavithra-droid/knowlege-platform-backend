from rest_framework.routers import DefaultRouter
from .views import AIViewset

router = DefaultRouter()
router.register("chat", AIViewset, basename="chat")

urlpatterns = router.urls
