import sys
import os

# adding path to your directory
base_dir= "/Users/erwien/Documents/myProject/python/flask/quiz-online/app"
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)


from run import app as application

if __name__ == "__main__":
    application.run()