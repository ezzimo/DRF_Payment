from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("v1/api/", include("payment.urls", namespace='payment')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
