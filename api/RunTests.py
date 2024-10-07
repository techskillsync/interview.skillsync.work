import os
# Set working directory to this file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()
import unittest

if __name__ == "__main__":
    loader = unittest.TestLoader()

    suite = loader.discover(start_dir='tests')

    runner = unittest.TextTestRunner()
    runner.run(suite)