import unittest
import io
from services.GetAudio import GetAudio

class TestGetAudio(unittest.TestCase):

    def test_GetAudio(self):
        Audio = GetAudio("Hi")
        self.assertIsInstance(Audio, io.BytesIO)

if __name__ == '__main__':
    unittest.main()