from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.serializers import CustomTokenObtainPairSerializer
from core.model_views.plan_views import PlanListCreateAPIView, PlanRetrieveUpdateDestroyAPIView

TOKEN_OBTAIN_PAIR = 'token-obtain-pair'
TOKEN_REFRESH = 'token-refresh'
PLANS = 'plans'

urlpatterns = [
    path('auth/knock-knock/', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer),
         name=TOKEN_OBTAIN_PAIR),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name=TOKEN_REFRESH),
    path('plans/', PlanListCreateAPIView.as_view(), name=PLANS),
    path('plans/<int:pk>/', PlanRetrieveUpdateDestroyAPIView.as_view(), name=PLANS),
]
