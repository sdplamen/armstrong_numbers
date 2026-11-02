import time

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from armstrong_nums.serializers import ArmstrongNumberSerializer
from armstrong_nums.armstrong import ENGINES, MAX_END_RANGE, find_armstrong_numbers
from armstrong_nums.c_engine import CEngineUnavailable

# Engine used for calculations: 'python' or 'c'.
ENGINE = 'python'


def validate_range(start_range, end_range, engine):
    """Returns an error message, or None if the input is valid."""
    if engine not in ENGINES:
        return f'Engine must be one of: {", ".join(ENGINES)}.'
    if start_range < 0 or end_range < start_range:
        return 'Start range must be non-negative and less than or equal to end range.'
    if end_range > MAX_END_RANGE[engine]:
        return f'End range must be at most {MAX_END_RANGE[engine]} for the {engine.capitalize()} engine.'
    return None


def timed_find(start_range, end_range, engine):
    """Returns (armstrong_numbers, elapsed milliseconds)."""
    started = time.perf_counter()
    armstrong_numbers = find_armstrong_numbers(start_range, end_range, engine)
    return armstrong_numbers, round((time.perf_counter() - started) * 1000, 3)


def armstrong_numbers_view(request):
    armstrong_numbers = []
    start_range = None
    end_range = None
    engine = ENGINE
    elapsed_ms = None
    error_message = None

    if request.method == 'POST':
        try:
            start_range_str = request.POST.get('start_range', '')
            end_range_str = request.POST.get('end_range', '')
            start_range = int(start_range_str)
            end_range = int(end_range_str)

            error_message = validate_range(start_range, end_range, engine)
            if not error_message:
                armstrong_numbers, elapsed_ms = timed_find(start_range, end_range, engine)
                if not armstrong_numbers:
                    error_message = f'No Armstrong numbers found in the range {start_range} to {end_range}.'
        except ValueError:
            error_message = 'Please enter valid integers for both start and end range.'
        except CEngineUnavailable as e:
            error_message = str(e)

    return render(request, 'index.html', {
        'armstrong_numbers': armstrong_numbers,
        'start_range': start_range,
        'end_range': end_range,
        'engine': engine,
        'elapsed_ms': elapsed_ms,
        'error_message': error_message
    })


class ArmstrongNumbersAPIView(APIView):
    serializer_class = ArmstrongNumberSerializer
    def post(self, request):
        try :
            start_range = request.data.get('start_range')
            end_range = request.data.get('end_range')
            engine = request.data.get('engine', ENGINE)

            if start_range is None or end_range is None :
                return Response({'error' :'start_range and end_range are required fields.'}, status=status.HTTP_400_BAD_REQUEST)

            start_range = int(start_range)
            end_range = int(end_range)

            error_message = validate_range(start_range, end_range, engine)
            if error_message :
                return Response({'error' :error_message}, status=status.HTTP_400_BAD_REQUEST)

            armstrong_numbers, elapsed_ms = timed_find(start_range, end_range, engine)

            return Response({'armstrong_numbers' :armstrong_numbers, 'engine' :engine, 'elapsed_ms' :elapsed_ms}, status=status.HTTP_200_OK)

        except (TypeError, ValueError) :
            return Response({'error' :'Please enter valid integers for both start and end range.'}, status=status.HTTP_400_BAD_REQUEST)
        except CEngineUnavailable as e :
            return Response({'error' :str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)