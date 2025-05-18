import unittest
from solution import appearance
class AppearanceTestCase(unittest.TestCase):

    def test_original_cases(self):
        self.assertEqual(appearance({
            'lesson': [1594663200, 1594666800],
            'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
            'tutor': [1594663290, 1594663430, 1594663443, 1594666473],
        }), 3117)

        self.assertEqual(appearance({
            'lesson': [1594702800, 1594706400],
            'pupil': [1594702789, 1594704500, 1594702807, 1594704542,
                      1594704512, 1594704513, 1594704564, 1594705150,
                      1594704581, 1594704582, 1594704734, 1594705009,
                      1594705095, 1594705096, 1594705106, 1594706480,
                      1594705158, 1594705773, 1594705849, 1594706480,
                      1594706500, 1594706875, 1594706502, 1594706503,
                      1594706524, 1594706524, 1594706579, 1594706641],
            'tutor': [1594700035, 1594700364, 1594702749, 1594705148,
                      1594705149, 1594706463],
        }), 3577)

        self.assertEqual(appearance({
            'lesson': [1594692000, 1594695600],
            'pupil': [1594692033, 1594696347],
            'tutor': [1594692017, 1594692066, 1594692068, 1594696341],
        }), 3565)

    def test_full_overlap(self):
        self.assertEqual(appearance({
            'lesson': [1000, 2000],
            'pupil': [1000, 2000],
            'tutor': [1000, 2000],
        }), 1000)

    def test_no_overlap(self):
        self.assertEqual(appearance({
            'lesson': [1000, 2000],
            'pupil': [500, 900],
            'tutor': [2100, 2200],
        }), 0)

    def test_one_participant(self):
        self.assertEqual(appearance({
            'lesson': [1000, 2000],
            'pupil': [1100, 1500],
            'tutor': [500, 900],
        }), 0)

    def test_edge_overlap(self):
        self.assertEqual(appearance({
            'lesson': [1000, 2000],
            'pupil': [900, 1500],
            'tutor': [1200, 2100],
        }), 300)

    def test_multiple_small_overlaps(self):
        self.assertEqual(appearance({
            'lesson': [0, 1000],
            'pupil': [100, 200, 300, 400, 500, 600],
            'tutor': [150, 250, 350, 450, 550, 650],
        }), 150)

    def test_zero_length_intervals(self):
        self.assertEqual(appearance({
            'lesson': [1000, 2000],
            'pupil': [1100, 1100, 1200, 1250],
            'tutor': [1230, 1300],
        }), 20)


if __name__ == '__main__':
    unittest.main()
