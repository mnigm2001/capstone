from django.shortcuts import render
from rest_framework import status, viewsets, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User, AnonymousUser

# For Uploading Images
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

import time, json

## For Token Gen
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .models import User, Pill, PillIntake, PillReminder, PillScanHistory, UserScanHistory
from .serializers import UserSerializer, PillSerializer, PillIntakeSerializer, PillReminderSerializer, ScrapedPillSerializer
from .permissions import IsOwnerOrAdmin
from .webscraper import MyDrug  # Import your Web_Scrapper class
from .image_recognition import image_recognition
from .shape_detection import shape_detection
from .colour_detection import colour_detection


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


# -------------- Registering Pills -------------- #
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
        print(pill)
    except Pill.DoesNotExist:
        return Response({'error': 'Pill not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Register the pill for the user
    frequency_mapping = {
        'daily': 24,
        'twice a day': 12,
        'every 12 hours': 12,
        'every 8 hours': 8,
        'every 5 minutes': 0.0833,
    }
    frequency_hours = frequency_mapping.get(pill_freq, 24)  # Default to daily if not found
    PillIntake.objects.create(user=request.user, pill=pill, frequency_hours=frequency_hours)
    
    return Response({'message': f'Pill {pill_name} registered successfully.'}, status=status.HTTP_201_CREATED)

# -------------- Creating Pill Reminders -------------- #
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
# @api_view(['POST'])
# def web_scrape(request):
#     # Request will have front_side_imprint, back_side_imprint, color, shape
#     # Get the data from the request, if not found, return an error
#     front_side = request.data.get('front_side')
#     back_side = request.data.get('back_side')
#     color = request.data.get('color')
#     shape = request.data.get('shape')
#     print(request.data)

#     # The back_side, color, and shape can be empty strings
#     if not front_side or not color or not shape:
#         return Response({'error': 'Missing required parameters.'}, status=status.HTTP_400_BAD_REQUEST)

#     # Check PillScanHistory for a matching search
#     matching_histories = PillScanHistory.objects.filter(
#         front_side=front_side,
#         back_side=back_side,
#         color=color,
#         shape=shape
#     )
    
#     # If there's a match and it has associated results, return those pills
#     if matching_histories.exists():
#         print('Matching histories found.')
#         # Assuming many PillScanHistory entries could match, aggregate their pills
#         pills = Pill.objects.filter(search_history__in=matching_histories).distinct()
#         response_serializer = PillSerializer(pills, many=True)
#         return Response(response_serializer.data)

#     # Check if pill is registered for this user
#     try:
#         pill = Pill.objects.get(name=front_side, color=color, shape=shape)  # Adjust query as needed
#         pill_intake = PillIntake.objects.filter(user=request.user, pill=pill).first()

#         if pill_intake:
#             print('Pill already registered for user.')
#             # Pill is already registered for this user, so return its details without scraping
#             response_serializer = PillSerializer(pill)
#             return Response(response_serializer.data)
#     except Pill.DoesNotExist:
#         pass  # If the pill doesn't exist, proceed with the web scraping below


#     # Webscrape
#     search_drug = MyDrug(front_side, back_side, color, shape)
#     pill_data = search_drug.quickSearch2(mode=1)
#     print(pill_data)

#     pills = []  # To store Pill objects for serialization
#     for pill_name, pill_info in pill_data.items():
#         pill_info_with_name = {"name": pill_name, **pill_info}
#         pill_info_with_name = {k.lower(): v for k, v in pill_info_with_name.items()}  # lower-case keys
#         print(pill_info_with_name)
#         serializer = ScrapedPillSerializer(data=pill_info_with_name)
#         if serializer.is_valid():
#             pill = serializer.save()
#             pills.append(pill)
#         else:
#             # validation errors
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     # If the user is authenticated, associate the search with their history
#     if not isinstance(request.user, AnonymousUser):
#         search_history = PillScanHistory.objects.create(
#             user=request.user,
#             front_side=front_side,
#             back_side=back_side,
#             color=color,
#             shape=shape,
#         )
#         # Associate the found/created pills with the user's search history
#         search_history.results.set(pills)

#     # Serialize and return the pills
#     response_serializer = PillSerializer(pills, many=True)
#     return Response(response_serializer.data)
        

################
@api_view(['POST'])
def web_scrape(request):
    front_side = request.data.get('front_side')
    back_side = request.data.get('back_side', '')  # Default to empty string if not provided
    color = request.data.get('color')
    shape = request.data.get('shape')

    if not front_side or not color or not shape:
        return Response({'error': 'Missing required parameters.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check PillScanHistory for a matching search
    matching_history, created = PillScanHistory.objects.get_or_create(
        front_side=front_side,
        back_side=back_side,
        color=color,
        shape=shape
    )

    # If there's a match and it has associated results, and it wasn't just created, return those pills
    if not created:
        pills = Pill.objects.filter(search_history=matching_history).distinct()
        if pills.exists():
            response_serializer = PillSerializer(pills, many=True)
            return Response(response_serializer.data)

    # Proceed with web scraping if no matching history with results was found or it was just created
    search_drug = MyDrug(front_side, back_side, color, shape)
    pill_data = search_drug.quickSearch2(mode=1)

    pills = []  # To store Pill objects for serialization
    for pill_name, pill_info in pill_data.items():
        pill_info_with_name = {"name": pill_name, **pill_info}
        pill_info_with_name = {k.lower(): v for k, v in pill_info_with_name.items()}  # lower-case keys
        serializer = ScrapedPillSerializer(data=pill_info_with_name)
        if serializer.is_valid():
            pill = serializer.save()
            pills.append(pill)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Associate the found/created pills with the PillScanHistory
    matching_history.results.set(pills)

    # If the user is authenticated, link this PillScanHistory to the UserScanHistory
    if not isinstance(request.user, AnonymousUser):
        UserScanHistory.objects.create(
            user=request.user,
            pill_scan=matching_history
        )

    # Serialize and return the pills
    response_serializer = PillSerializer(pills, many=True)
    return Response(response_serializer.data)


class ImageUploadView(APIView):
    parser_classes = [FileUploadParser]
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        print(request.data)
        if 'file' not in request.data:
            return Response("No image file provided", status=status.HTTP_400_BAD_REQUEST)
        
        file = request.data['file']
        # You can now handle the uploaded image file as needed
        # For example, save it to a model or pass it to another function for processing
        # save the image to ./media/images/
        # with open('./media/images/' + file.name, 'wb+') as destination:
        #     for chunk in file.chunks():
        #         destination.write(chunk)
        print(type(file))
        print(dir(file))

        result = {}
        start_time = time.time()
        test = image_recognition(file)
        end_time = time.time()

        result["Pill Detected"] = test.pill_detected
        result["Imprint"] = test.imprint

        print(result)
        print(f"Time taken for pill/imprint detection: {end_time - start_time} seconds")

        print(dir(test))
        # print(type(test.cropped_img))

        start_time = time.time()
        if(result["Pill Detected"]):
            print("Pill Detected")
            shape_test = shape_detection(test.cropped_img) # TODO: THIS WONT WORK
        else:
            print("Pill not detected")
            shape_test = shape_detection(file)
        result["Shape"] = shape_test.shape
        print(result)
        end_time = time.time()
        print(f"Time taken for shape detection: {end_time - start_time} seconds")

        test_colour = colour_detection(shape_test.cropped_img)
        result["Colour"] = test_colour.colour

        result_json = json.dumps(result,indent=2)
        print(result_json)


        return Response("Image processed successfully", status=status.HTTP_200_OK)


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
