from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from armstrong_nums.armstrong import MAX_END_RANGE, find_armstrong_numbers


def brute_force(start, end):
    result = []
    for number in range(start, end + 1):
        digits = str(number)
        if sum(int(d) ** len(digits) for d in digits) == number:
            result.append(number)
    return result


class EngineTests(TestCase):
    def test_engines_match_brute_force(self):
        for start, end in [(0, 0), (0, 9), (9, 10), (153, 153), (100, 999), (0, 100000), (5000, 600000)]:
            expected = brute_force(start, end)
            self.assertEqual(find_armstrong_numbers(start, end, 'python'), expected)
            self.assertEqual(find_armstrong_numbers(start, end, 'c'), expected)

    def test_engines_match_on_large_range(self):
        python_result = find_armstrong_numbers(0, 10 ** 10, 'python')
        self.assertEqual(len(python_result), 33)
        self.assertEqual(find_armstrong_numbers(0, 10 ** 10, 'c'), python_result)

    def test_c_engine_full_64_bit_range(self):
        result = find_armstrong_numbers(0, MAX_END_RANGE['c'], 'c')
        self.assertEqual(len(result), 51)
        self.assertEqual(result[-1], 4929273885928088826)


class ViewTests(TestCase):
    def test_form_uses_configured_engine(self):
        for engine, label in (('python', 'Python'), ('c', 'C')):
            with patch('armstrong_nums.views.ENGINE', engine):
                response = self.client.post(reverse('index'), {'start_range': 100, 'end_range': 999})
            self.assertEqual(response.context['armstrong_numbers'], [153, 370, 371, 407])
            self.assertContains(response, f'with the {label} engine')

    def test_form_rejects_end_above_engine_limit(self):
        response = self.client.post(reverse('index'), {'start_range': 0, 'end_range': MAX_END_RANGE['python'] + 1})
        self.assertIn('at most', response.context['error_message'])

    def test_api_engines(self):
        for engine in ('python', 'c'):
            response = self.client.post(reverse('armstrong_numbers_api'),
                                        {'start_range': 100, 'end_range': 999, 'engine': engine}, format='json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['armstrong_numbers'], [153, 370, 371, 407])
            self.assertEqual(response.data['engine'], engine)

    def test_api_rejects_unknown_engine(self):
        response = self.client.post(reverse('armstrong_numbers_api'),
                                    {'start_range': 1, 'end_range': 5, 'engine': 'rust'})
        self.assertEqual(response.status_code, 400)
