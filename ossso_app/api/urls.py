from rest_framework.routers import DefaultRouter
from api import views


router = DefaultRouter()
router.register(r"response", views.SAMLResponseViewSet, basename="sso")
router.register(r"connection", views.SAMLConnectionViewSet, basename="sso")
urlpatterns = router.urls
