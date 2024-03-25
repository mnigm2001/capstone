from django.shortcuts import render
from rest_framework import status, viewsets, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User

from .models import User, Pill, PillIntake, PillReminder
from .serializers import UserSerializer, PillSerializer, PillIntakeSerializer, PillReminderSerializer
from .permissions import IsOwnerOrAdmin
from .webscraper import MyDrug  # Import your Web_Scrapper class

## For Token Gen
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'destroy':
            print("HI")
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_pill(request):
    """
    
    """
    # Extract pill name from the request
    pill_name = request.data.get('pill_name')
    if not pill_name:
        return Response({'error': 'Pill name is required.'}, status=status.HTTP_400_BAD_REQUEST)
    pill_freq = request.data.get('frequency')

    # Find the pill in the database
    try:
        pill = Pill.objects.get(name=pill_name)
    except Pill.DoesNotExist:
        return Response({'error': 'Pill not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Register the pill for the user
    frequency_mapping = {
        'daily': 24,
        'twice a day': 12,
        'every 12 hours': 12,
        'every 8 hours': 8,
    }
    frequency_hours = frequency_mapping.get(pill_freq, 24)  # Default to daily if not found
    PillIntake.objects.create(user=request.user, pill=pill, frequency_hours=frequency_hours)
    
    return Response({'message': f'Pill {pill_name} registered successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_pill_reminder(request):
    pill_name = request.data.get('pill_name')
    reminder_time = request.data.get('reminder_time')  # Assume this is in a valid time format, e.g., '14:00'

    # Convert reminder_time from string to a time object if necessary
    # reminder_time = datetime.strptime(reminder_time, '%H:%M').time()

    # Step 2: Check if the pill is registered
    pill, created = Pill.objects.get_or_create(name=pill_name)
    pill_intake, created = PillIntake.objects.get_or_create(user=request.user, pill=pill)

    # Step 3: Setting the reminder
    reminder, created = PillReminder.objects.update_or_create(
        pill_intake=pill_intake,
        defaults={'reminder_time': reminder_time, 'active': True}
    )

    return Response({'message': 'Reminder set successfully.'}, status=status.HTTP_200_OK)




# -------------- For Web Scraping -------------- #
@api_view(['POST'])
def web_scrape(request):
    # Request will have front_side_imprint, back_side_imprint, color, shape
    # Get the data from the request, if not found, return an error
    front_side = request.data.get('front_side')
    back_side = request.data.get('back_side')
    color = request.data.get('color')
    shape = request.data.get('shape')
    print(request.data)

    # The back_side, color, and shape can be empty strings
    if not front_side or not color or not shape:
        return Response({'error': 'Missing required parameters.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Instantiate your scraper
    search_drug = MyDrug(front_side, back_side, color, shape)
    pill_data = search_drug.quickSearch2(mode=1)
    print(pill_data)


    return Response(pill_data)


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
