from .views import ReservationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('reservation', ReservationViewSet, basename="reservation")

urlpatterns = router.urls

