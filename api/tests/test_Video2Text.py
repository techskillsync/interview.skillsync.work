import unittest
from services.Video2Text import process_video_bytes

class TestVideo2Text(unittest.TestCase):

    def test_Video2Text(self):
        str1 = process_video_bytes("assets/audio_sample.mp3")
        str2 = process_video_bytes("assets/fake-file.mp4")
        str3 = process_video_bytes("assets/SampleInterview.mp4")
        print(str1)
        print(str2)
        print(str3)

if __name__ == '__main__':
    unittest.main()