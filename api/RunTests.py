import os
# Set working directory to this file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()
import unittest, argparse

def run_tests():
	loader = unittest.TestLoader()

	suite = loader.discover(start_dir='tests')

	runner = unittest.TextTestRunner()
	runner.run(suite)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Run tests')
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-a', '--all', action='store_true', help='Run all tests, including expensive ones')
	group.add_argument('-f', '--free', action='store_true', help='Run only free tests')
	args = parser.parse_args()

	if args.all:
		os.environ['RUN_EXPENSIVE_TESTS'] = 'true'
	elif args.free:
		os.environ['RUN_EXPENSIVE_TESTS'] = 'false'

	run_tests()