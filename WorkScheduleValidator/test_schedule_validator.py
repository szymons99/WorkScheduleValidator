import unittest
from io import StringIO
from unittest.mock import patch
from schedule_validator import read_schedule_from_file, validate_schedule

class TestScheduleValidator(unittest.TestCase):

    def test_read_schedule_from_file(self):
        file_contents = "1,8\n2,7\n3,9"
        with patch('builtins.open', return_value=StringIO(file_contents)):
            schedule = read_schedule_from_file("test_schedule.txt")
        self.assertEqual(schedule, {1: 8, 2: 7, 3: 9})

    def test_validate_schedule_exceed_work_hours(self):
        schedule = {1: 9, 2: 800, 3: 9}
        with patch('builtins.print') as mock_print:
            validate_schedule(schedule)
            self.assertIn("Validation 1:", mock_print.call_args_list[0][0][0])

    def test_validate_schedule_sunday_work(self):
        schedule = {1: 8, 2: 7, 3: 9, 6: 4}
        with patch('builtins.print') as mock_print:
            validate_schedule(schedule)
            self.assertIn("Validation 2:", mock_print.call_args_list[0][0][0])

    def test_validate_schedule_overtime(self):
        schedule = {1: 8, 2: 10, 3: 6}
        with patch('builtins.print') as mock_print:
            validate_schedule(schedule)
            self.assertIn("Validation 3:", mock_print.call_args_list[0][0][0])

    def test_validate_schedule_short_break(self):
        schedule = {1: 8, 2: 14, 3: 12}
        with patch('builtins.print') as mock_print:
            validate_schedule(schedule)
            self.assertIn("Validation 4:", mock_print.call_args_list[1][0][0])

if __name__ == "__main__":
    unittest.main()
