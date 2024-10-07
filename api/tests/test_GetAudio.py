import unittest, io, os
from services.GetAudio import GetAudio

class TestGetAudio(unittest.TestCase):

    @unittest.skipUnless(os.getenv('RUN_EXPENSIVE_TESTS') == 'true', "Skipping GetAudio API test to save tokens")
    def test_GetAudio(self):
        Audio = GetAudio("Hi")
        self.assertIsInstance(Audio, io.BytesIO)

if __name__ == '__main__':
    unittest.main()