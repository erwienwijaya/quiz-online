from app import app as application
import os
import sys
from dotenv import load_dotenv

project_home = '/home/erwien/dev/python/flask/quiz-online-flask'
if project_home not in sys.path:
    sys.path.append(project_home)

# MUAT .env DENGAN PATH ABSOLUT
load_dotenv(os.path.join(project_home, '.env'))
