from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from armstrong_nums.serializers import ArmstrongNumberSerializer


# Create your views here.
def is_armstrong_number(number):
    num_str = str(number)
    power = len(num_str)
    armstrong_sum = sum(int(digit) ** power for digit in num_str)
    return armstrong_sum == number

def find_armstrong_numbers(start, end):
    armstrong_numbers = []
    for num in range(start, end + 1):
        if is_armstrong_number(num):
            armstrong_numbers.append(num)
    return armstrong_numbers

def armstrong_numbers_view(request):
    armstrong_numbers = []
    start_range = None
    end_range = None
    error_message = None

    if request.method == 'POST':
        try:
            start_range_str = request.POST.get('start_range', '')
            end_range_str = request.POST.get('end_range', '')
            start_range = int(start_range_str)
            end_range = int(end_range_str)

            if start_range < 0 or end_range < start_range:
                error_message = 'Start range must be non-negative and less than or equal to end range.'
            else:
                armstrong_numbers = find_armstrong_numbers(start_range, end_range)
                if not armstrong_numbers and not error_message:
                    error_message = f'No Armstrong numbers found in the range {start_range} to {end_range}.'
        except ValueError:
            error_message = 'Please enter valid integers for both start and end range.'

    return render(request, 'index.html', {
        'armstrong_numbers': armstrong_numbers,
        'start_range': start_range,
        'end_range': end_range,
        'error_message': error_message
    })


class ArmstrongNumbersAPIView(APIView):
    serializer_class = ArmstrongNumberSerializer
    def post(self, request):
        try :
            start_range = request.data.get('start_range')
            end_range = request.data.get('end_range')

            if start_range is None or end_range is None :
                return Response({'error' :'start_range and end_range are required fields.'}, status=status.HTTP_400_BAD_REQUEST)

            start_range = int(start_range)
            end_range = int(end_range)

            if start_range < 0 or end_range < start_range :
                return Response({'error' :'Start range must be non-negative and less than or equal to end range.'}, status=status.HTTP_400_BAD_REQUEST)

            armstrong_numbers = find_armstrong_numbers(start_range, end_range)

            return Response({'armstrong_numbers' :armstrong_numbers}, status=status.HTTP_200_OK)

        except ValueError :
            return Response({'error' :'Please enter valid integers for both start and end range.'}, status=status.HTTP_400_BAD_REQUEST)