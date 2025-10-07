from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

#Swagger configuration for JWT Bearer Token
schema_view = get_schema_view(
    openapi.Info(
        title="Movie Booking API",
        default_version='v1',
        description="API documentation for Movie Ticket Booking System",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@moviebooking.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

#Add Bearer authentication description (compatible with all versions)
schema_view.security_definitions = {
    "Bearer": {
        "type": "apiKey",
        "name": "Authorization",
        "in": "header",
        "description": "Enter JWT token in this format: **Bearer <access_token>**"
    }
}

urlpatterns = [
    path('admin/', admin.site.urls),

    #App routes
    path('api/', include('booking_app.urls')),

    #Swagger documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
