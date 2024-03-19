from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'admin/users', views.UserViewSet)
router.register(r'admin/pills', views.PillViewSet)  # Register the PillViewSet
router.register(r'pill_intakes', views.PillIntakeViewSet)
router.register(r'pill_reminders', views.PillReminderViewSet)

urlpatterns = [
    # path('add_pill/', views.add_pill)
    path('api/add-items/', views.add_items, name='add-items'),
    path('api-token-auth/', views.CustomObtainAuthToken.as_view()),
    # Include the router URL patterns
    path('api/', include(router.urls)),
     path('api/register-pill/', views.register_pill, name='register-pill'),
]