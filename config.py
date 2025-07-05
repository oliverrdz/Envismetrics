import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_DIR = os.path.join(BASE_DIR, 'logs')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')
TMP_FOLDER = '/var/tmp'
ALLOWED_EXTENSIONS = {'csv', 'txt', 'xlsx'}
