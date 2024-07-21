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

start_range = int(input('Enter a number to start of range for Armstrong number : '))
end_range = int(input('Enter a number to end of range for Armstrong number : '))

result = find_armstrong_numbers(start_range, end_range)
print(f'Armstrong numbers in the range of {start_range} to {end_range} are {", ".join(str(x) for x in result)}')
