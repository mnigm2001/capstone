
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

import time, json, os
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import permutations, combinations

## For Token Gen
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .models import User, Pill, PillIntake, PillReminder, PillScanHistory, UserScanHistory
from .serializers import UserSerializer, PillSerializer, PillIntakeSerializer, PillReminderSerializer, ScrapedPillSerializer, PillInfoSerializerVerbose
from .permissions import IsOwnerOrAdmin

from .webscraper import MyDrug
from .imgproc_shape_detection import shape_detection
from .imgproc_colour_detection import colour_detection
from .imgproc_top import process_image

from django.conf import settings
from django.http import Http404

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


class PillDetailView(APIView):
    def get_object(self, name):
        try:
            return Pill.objects.get(name=name)
        except Pill.DoesNotExist:
            return None

    def get(self, request, format=None):
        name = request.query_params.get('name', None)
        if not name:
            return Response({'error': 'The name parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        pill = self.get_object(name)
        if pill is None:
            return Response({'error': f'Pill with name {name} not found.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PillInfoSerializerVerbose(pill)
        return Response(serializer.data)
    
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



# ---------------------------------------------- #
# -------------- For Web Scraping -------------- #
# ---------------------------------------------- #
def perform_web_scrape(front_side, back_side, color, shape, user):    
    # Check PillScanHistory for a matching search
    matching_histories = PillScanHistory.objects.filter(
        front_side=front_side,
        back_side=back_side,
        color=color,
        shape=shape
    ).order_by('-searched_at')  # Order by the most recent first

    created = False
    # If there's a match, use the most recent one
    if matching_histories.exists():
        matching_history = matching_histories.first()
    else:
        created = True
        # If there's no match, create a new one
        matching_history = PillScanHistory.objects.create(
            front_side=front_side,
            back_side=back_side,
            color=color,
            shape=shape
        )

    # If there's a match and it has associated results, and it wasn't just created, return those pills
    # if not created:
    #     pills = Pill.objects.filter(search_history=matching_history).distinct()
    #     if pills.exists():
    #         print("Matching History Found")
    #         response_serializer = PillSerializer(pills, many=True)
    #         return response_serializer.data

    # Search in the Pill database for a pill with matching imprint=front_side and back_side seperated by a space
    print(f"front_side = {front_side}")
    pills = Pill.objects.filter(imprint=front_side)
    if pills.exists():
        print("Matching Pill Found")
        matching_history.results.set(pills)
        response_serializer = PillSerializer(pills, many=True)
        return response_serializer.data

    # Proceed with web scraping if no matching history with pill results was found or it was just created
    print("No Matching History Found: Proceeding with Web Scraping...")
    search_drug = MyDrug(front_side, back_side, color, shape)
    retry_count = 0
    while retry_count < 3:
        pill_data = search_drug.quickSearch2(mode=1)
        if pill_data is not None:
            break
        else:
            retry_count += 1

    if pill_data is None:
        print("No data found.")
        return None

    pills = []  # To store Pill objects for serialization
    for pill_name, pill_info in pill_data.items():
        pill_info_with_name = {"name": pill_name, **pill_info}
        pill_info_with_name = {k.lower(): v for k, v in pill_info_with_name.items()}  # lower-case keys
        # print("pill_info_with_name: ", pill_info_with_name)
        serializer = ScrapedPillSerializer(data=pill_info_with_name)
        if serializer.is_valid():
            pill = serializer.save()
            pills.append(pill)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Associate the found/created pills with the PillScanHistory
    matching_history.results.set(pills)

    # If the user is authenticated, link this PillScanHistory to the UserScanHistory
    if not isinstance(user, AnonymousUser):
        UserScanHistory.objects.create(
            user=user,
            pill_scan=matching_history
        )

    response_serializer = PillSerializer(pills, many=True)
    return response_serializer.data


@api_view(['POST'])
def web_scrape(request):
    front_side = request.data.get('front_side')
    back_side = request.data.get('back_side', '')  # Default to empty string if not provided
    color = request.data.get('color')
    shape = request.data.get('shape')
    print("Params Parsed")

    if not front_side or not color or not shape:
        return Response({'error': 'Missing required parameters.'}, status=status.HTTP_400_BAD_REQUEST)


    # Perform the web scrape using the refactored function
    result = perform_web_scrape(front_side, back_side, color, shape, request.user)

    print("Data found")
    print(result)
    return Response(result, status=status.HTTP_200_OK)

# ---------------------------------------- #
# -------------- Image Scan -------------- #
# ---------------------------------------- #

def perform_shape_color_detection(final_img):
    print("\nPerforming Shape and Colour Detection...")
    
    # Define functions to be executed in parallel
    def detect_custom_shape(shape_obj):
        shape_obj.find_shape()
        return shape_obj.shape

    def detect_gpt_shape(shape_obj):
        shape_obj.detect_shape_gpt()
        return shape_obj.gbt_shape

    def detect_custom_colour(color_obj):
        color_obj.avg_all_pixels()
        return color_obj.colour

    def detect_gpt_colour(color_obj):
        color_obj.detect_colour_gpt()
        return color_obj.gbt_colour

    # Initialize objects
    shape_obj = shape_detection(final_img)
    color_obj = colour_detection(final_img)

    # Use ThreadPoolExecutor to run tasks concurrently
    with ThreadPoolExecutor() as executor:
        # Schedule the custom and GPT-based methods for shape and color detection
        future_custom_shape = executor.submit(detect_custom_shape, shape_obj)
        future_gpt_shape = executor.submit(detect_gpt_shape, shape_obj)
        future_custom_colour = executor.submit(detect_custom_colour, color_obj)
        future_gpt_colour = executor.submit(detect_gpt_colour, color_obj)

        # Wait for all futures to complete
        custom_shape = future_custom_shape.result()
        gpt_shape = future_gpt_shape.result()
        custom_colour = future_custom_colour.result()
        gpt_colour = future_gpt_colour.result()

    print("Custom Shape = ", custom_shape, "\tGPT Shape = ", gpt_shape)
    print("Custom Colour = ", custom_colour, "\tGPT Colour = ", gpt_colour)

    return custom_colour, custom_shape, gpt_colour, gpt_shape

def image_scan(file):
    detected_text, final_img = process_image(image_file=file,
                                image_name=file.name,
                                pre_processed_imgs_path=os.path.join(settings.PILL_VAULT_DIR, 'pre_processed_imgs'), 
                                save_img_prefix=0)
    
    if detected_text is None:
        return detected_text, final_img
    return detected_text, final_img


class ImageUploadView(APIView):
    parser_classes = [FileUploadParser]
    parser_classes = (MultiPartParser,) #https://stackoverflow.com/questions/46806335/fileuploadparser-doesnt-get-the-file-name

    def post(self, request, *args, **kwargs):

        response_data = {}
        response_data["Pill Detected"] = False
        response_data["Pill"] = {}

        if 'image1' not in request.data:
            return Response("Front image file not provided", status=status.HTTP_400_BAD_REQUEST)

        front_img = request.data['image1']
        back_img = request.data.get('image2')  # back_img will be None if not provided

        ##############################################
        ## Concurrently process front and back images
        ##############################################
        print(f"{'-'*20} Processing Images {'-'*20}")
        with ThreadPoolExecutor(max_workers=2) as executor:
            # future_results = [executor.submit(image_scan, front_img)]
            future_to_image = {
                executor.submit(image_scan, front_img): 'front'
            }


            if back_img is not None:
                # future_results.append(executor.submit(image_scan, back_img))
                future_to_image[executor.submit(image_scan, back_img)] = 'back'

            img_proc_results = []
            for future in as_completed(future_to_image):
                image_side = future_to_image[future]
                try:
                    detected_text, final_img = future.result()
                    # Process each result here
                    img_proc_results.append({
                        'side': image_side,
                        'detected_text': detected_text
                    })
                except Exception as exc:
                    print(f"{image_side} generated an exception: {exc}")
        
        #########################
        ## Process Image Results
        #########################
        if all(result['detected_text'] is None for result in img_proc_results):
            # result_json = json.dumps(response_data)
            return Response(response_data, status=status.HTTP_200_OK)
        
        print(f"\n\n{'-'*20} Interpreting Processing Results {'-'*20}")
        all_detected_text = []
        for img_proc_result in img_proc_results:
            if img_proc_result['detected_text'] is not None:
                all_detected_text.extend(img_proc_result['detected_text'])

        # Remove strings with special characters, allow only alphanumeric strings and spaces
        for text in all_detected_text:
            if (not text.strip().isalnum()):
                if ' ' not in text:
                   all_detected_text.remove(text)
                else:
                    for sub_text in text.split():
                        if not sub_text.isalnum():
                            all_detected_text.remove(text)
                            break
            
        # all_detected_text = [text for text in all_detected_text if text.strip.isalnum() or ' ' in text]
        print("all_detected_text = BEFORE", all_detected_text)

        if len(all_detected_text) == 2:                                                     # remove substring
            if all_detected_text[0] in all_detected_text[1]:
                all_detected_text.pop(0)
            elif all_detected_text[1] in all_detected_text[0]:
                all_detected_text.pop(1)
            else:                                                                           # concatenate the two strings
                first_str = all_detected_text[0]
                all_detected_text[0] = first_str + " " + all_detected_text[1]
                all_detected_text[1] = all_detected_text[1] + " " + first_str
        elif len(all_detected_text) >= 3:

            superset_found = False
            for potential_superset in all_detected_text:
                if all(other_str in potential_superset for other_str in all_detected_text if other_str != potential_superset):
                    all_detected_text = [potential_superset]
                    superset_found = True
            
            if not superset_found:
                # all_permutations = permutations(all_detected_text, 2)
                # all_detected_text = [' '.join(permutation) for permutation in all_permutations]

                concatenated_combinations = set()
                # Generate combinations for every size
                for i in range(2, len(all_detected_text) + 1):
                    for combo in combinations(all_detected_text, i):
                        # Add the combination itself
                        concatenated_combinations.add(' '.join(combo))
                        # Generate all permutations for the combination
                        for perm in permutations(combo):
                            concatenated_combinations.add(' '.join(perm))
                all_detected_text = list(concatenated_combinations)


        print("all_detected_text = AFTER", all_detected_text)

        # Perform shape and color detection
        custom_colour, custom_shape, gpt_colour, gpt_shape = perform_shape_color_detection(final_img)
        
        ##########################
        ## Fetch Pill Information
        ##########################
        print(f"\n\n{'-'*20} Fetching Pill Information {'-'*20}")
        for text in all_detected_text:
            pill_results = perform_web_scrape(front_side=text, 
                                        back_side="", 
                                        color=gpt_colour,
                                        shape=gpt_shape, 
                                        user=request.user)
            if pill_results is None:
                continue
            
            print(f"text: {text} -> {pill_results}")
            for pill_result in pill_results:
                print(f"text({type(text)}): {text} -- imp({type(pill_result['imprint'])}): {pill_result['imprint']} -- {str(pill_result['imprint']) == str(text)}")
                if str(pill_result['imprint']) == str(text):
                    print("Matching Pill Found")
                    response_data["Pill Detected"] = True
                    response_data["Pill"] = pill_result
                    # result_json = json.dumps(response_data)
                    return Response(response_data, status=status.HTTP_200_OK)



        # result_json = json.dumps(response_data)
        # print(result_json)
        return Response(response_data, status=status.HTTP_200_OK)
    
        
# {
#     "Pill detected": True/False,
#     "Probable pills": [
#         {
#             "name": "",
#             "imprint": "",
#             "shape": "",
#             "color": ""
#         }
#     ]
# }

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


