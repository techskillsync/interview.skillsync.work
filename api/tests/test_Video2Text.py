import unittest
import io
from services.Video2Text import process_video_bytes

class TestVideo2Text(unittest.TestCase):

    def test_Video2Text(self):
        str = process_video_bytes("assets/SampleInterview.mp4")
        print(str)

if __name__ == '__main__':
    unittest.main()