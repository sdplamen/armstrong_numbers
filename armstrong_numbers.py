def is_armstrong_number(num):
    num_str = str(num)
    power = len(num_str)
    armstrong_sum = sum(int(digit) ** power for digit in num_str)
    return armstrong_sum == num

def find_armstrong_numbers(start, end):
    armstrong_numbers = []

    for num in range(start, end + 1):
        if is_armstrong_number(num):
            armstrong_numbers.append(num)

    return armstrong_numbers

start_range = int(input('Enter a number to start of range for Armstrong number : '))
end_range = int(input('Enter a number to end of range for Armstrong number : '))

print(f'Armstrong numbers in the range {(start_range, end_range)} are {find_armstrong_numbers(start_range, end_range)}')
