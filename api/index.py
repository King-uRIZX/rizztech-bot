import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from webhook import handler

app = handler
