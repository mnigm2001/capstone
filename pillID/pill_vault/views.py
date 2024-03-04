from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, PillSerializer

# Create your views here.
def say_hello(request):
    # exists = Product.objects.filter(pk=0).exists()


    return render(request, 'hello.html', {'name': 'Mohamed'})

# # This function will read JSON data from file /home/mnigm2001/capstone/backend/capstone/webscraper/allDrugs.json and add the pill data to the database
# def add_pill(request):
#     # 1 read JSON data from file
#     file_path = "/home/mnigm2001/capstone/backend/capstone/webscraper/allDrugs.json"
#     with open(file_path, "r") as file:

#     # 2 add pill data to the database


# views.py

from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.

    CRUD URLs:
    GET /api/admin/users/ - List users
    POST /api/admin/users/ - Create a new user
    GET /api/admin/users/{id}/ - Retrieve a user
    PUT /api/admin/users/{id}/ - Update a user
    PATCH /api/admin/users/{id}/ - Partially update a user
    DELETE /api/admin/users/{id}/ - Delete a user

    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = [permissions.IsAdminUser]  # This ensures only admins can access this endpoint

    # You can also override any methods if you need custom functionality, for example:
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Custom delete logic here
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework import viewsets, permissions
from .models import Pill
from .serializers import PillSerializer

class PillViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing pill instances.

    GET /api/admin/users/ - List users
    POST /api/admin/users/ - Create a new user
    GET /api/admin/users/{id}/ - Retrieve a user
    PUT /api/admin/users/{id}/ - Update a user
    PATCH /api/admin/users/{id}/ - Partially update a user
    DELETE /api/admin/users/{id}/ - Delete a user

    """
    queryset = Pill.objects.all()
    serializer_class = PillSerializer
    permission_classes = [permissions.IsAdminUser]  # Adjust as needed

from rest_framework import viewsets
from .models import PillIntake, PillReminder
from .serializers import PillIntakeSerializer, PillReminderSerializer
from rest_framework.permissions import IsAuthenticated

class PillIntakeViewSet(viewsets.ModelViewSet):
    queryset = PillIntake.objects.all()
    serializer_class = PillIntakeSerializer
    # TODO: Uncomment this 
    # permission_classes = [IsAuthenticated]  # Ensure the user is logged in

    def get_queryset(self):
        """
        This view should return a list of all the pill intakes
        for the currently authenticated user.
        """
        user = self.request.user
        return PillIntake.objects.filter(user=user)

class PillReminderViewSet(viewsets.ModelViewSet):
    queryset = PillReminder.objects.all()
    serializer_class = PillReminderSerializer
    # TODO: Uncomment this 
    # permission_classes = [IsAuthenticated]  # Ensure the user is logged in
    
    def get_queryset(self):
        """
        This view should return a list of all the pill reminders
        associated with the pill intakes of the currently authenticated user.
        """
        user = self.request.user
        # This assumes your PillIntake model has a 'reminders' related name for PillReminder
        return PillReminder.objects.filter(pill_intake__user=user)


"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer

# Create a User
@api_view(['POST'])
# @permission_classes([IsAdminUser])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# List Users
@api_view(['GET'])
# @permission_classes([IsAdminUser])
def list_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# Get a User Details
@api_view(['GET'])
# @permission_classes([IsAdminUser])
def get_user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data)

# Update a User
@api_view(['PUT'])
# @permission_classes([IsAdminUser])
def update_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Partially Update a User
@api_view(['PATCH'])
# @permission_classes([IsAdminUser])
def partial_update_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete a User
@api_view(['DELETE'])
# @permission_classes([IsAdminUser])
def delete_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

"""

"""
@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def update_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""

# -------------- For Terminal CMD that adds json data to DB -------------- #

@api_view(['POST'])
def add_items(request):
    if isinstance(request.data, list):  # Handles multiple items
        serializer = PillSerializer(data=request.data, many=True)
    else:  # Handles single item
        serializer = PillSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
