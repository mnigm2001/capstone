from django.urls import path
from . import views

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PillViewSet, PillIntakeViewSet, PillReminderViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'admin/users', UserViewSet)
router.register(r'admin/pills', PillViewSet)  # Register the PillViewSet
router.register(r'pill_intakes', PillIntakeViewSet)
router.register(r'pill_reminders', PillReminderViewSet)

urlpatterns = [
    path('hello/', views.say_hello),
    # path('add_pill/', views.add_pill)
    path('api/add-items/', views.add_items, name='add-items'),
    # Include the router URL patterns
    path('api/', include(router.urls)),
]


# urlpatterns = [
#     path('hello/', views.say_hello),
#     # path('add_pill/', views.add_pill)
#     path('api/add-items/', views.add_items, name='add-items'),

#     path('api/admin/users/', views.create_user, name='create_user'),
#     path('api/admin/users/', views.list_users, name='list_users'),
#     path('api/admin/users/<int:pk>/', views.get_user_detail, name='get_user_detail'),
#     path('api/admin/users/<int:pk>/', views.update_user, name='update_user'),
#     path('api/admin/users/<int:pk>/', views.partial_update_user, name='partial_update_user'),
#     path('api/admin/users/<int:pk>/', views.delete_user, name='delete_user'),
# ]


# URLConf
""""""
# urlpatterns = [
#     path('hello/', views.say_hello),
#     # path('add_pill/', views.add_pill)
#     path('api/add-items/', views.add_items, name='add-items'),
#     path('users/create/', views.create_user),
#     path('users/delete/<int:user_id>/', views.delete_user),
#     path('users/update/<int:user_id>/', views.update_user),
# ]

# # Admin URLs
# urlpatterns = [
#     path('users/create/', views.create_user),
#     path('users/delete/<int:user_id>/', views.delete_user),
#     path('users/update/<int:user_id>/', views.update_user),
# ]
