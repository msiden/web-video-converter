from video_converter.config import *

UPLOADS_DIRECTORY = "uploads/"
COMPLETED_DIRECTORY = "completed/"
FILE_NAME_SUFFIX = "({}bps).mp4"
ZIP_FILE = COMPLETED_DIRECTORY + "converted_files.zip"
HOME_URL = LOCAL_URL if DEV_MODE else PUBLIC_URL
