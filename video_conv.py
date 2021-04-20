#!/usr/bin/python3
# -*- coding: utf-8 -*-

import ffmpeg
import os
import argparse
import time
import json
import smtplib
import datetime
import platform


# Functions
def convert(input_file, br):
    """
    Perform bit rate conversion on one video file and return result whether it passed or failed

    - input_file -- (String. Mandatory) The full path to the input video file
    - bitrate -- (String/Integer. Mandatory) The requested output bitrate.

    Returns: Boolean
    """
    suffix = "_(bitrate_{}).mp4".format(br)
    was_processed = True
    output_file = input_file[:input_file.rfind(".")] + suffix

    # Cancel the process if the file has already been converted
    if input_file in get_history() or suffix in input_file or os.path.exists(output_file):
        return False

    stream = ffmpeg.input(input_file)
    stream = ffmpeg.output(stream, output_file, video_bitrate=br)
    try:
        ffmpeg.run(stream, quiet=True)
        update_history(input_file)
    except ffmpeg.Error:
        was_processed = False
    return was_processed


def flush():
    """
    Delete old, unprocessed files

    Returns: None
    """
    deleted_files = 0
    for f in get_history():
        if os.path.exists(f):
            print(f)
            os.remove(f)
            deleted_files += 1
    print("{0} file{1} deleted\n".format(deleted_files, " was" if deleted_files == 1 else "s were"))


def get_email_settings(email_settings_db):
    """
    Check if the file email_settings.json is available and if so return its contents. If not, return None.

    - email_settings_db -- (String. Mandatory) The email settings json-file.

    Returns: None or Dict
    """
    email_settings = None
    if email_settings_db and os.path.exists(email_settings_db):
        with open(email_settings_db, "r") as f:
            email_settings = json.loads(f.read())
    return email_settings


def get_history():
    """
    Open database file containing previously processed files. If not available an empty db will be returned

    Returns: Dict
    """
    db = {}
    if os.path.exists(HISTORY_DB_FILE):
        with open(HISTORY_DB_FILE, "r") as f:
            db = json.loads(f.read())
    return db


def get_timestamp():
    """
    Generate a pretty formatted time stamp as string

    Returns: String
    """
    return time.strftime("%Y-%m-%d @ %H:%M:%S")


def get_video_files(arg):
    """
    Evaluate 'folders' argument passed through argparse and return a list containing all video files in those folders.

    - arg -- (List. Mandatory) A list of data to evaluate. Contains either a reference to a json-file or a series of
        folder paths.

    Returns: List
    """
    db = arg
    result = []

    # Open json-file when applicable
    if len(arg) == 1 and os.path.isfile(arg[0]):
        with open(arg[0], "r") as f:
            db = json.loads(f.read())

    # Verify that all folders are valid
    for fl in db:
        assert os.path.isdir(fl), "{} is not a valid folder".format(fl)

    # Check for sub folders
    if not args.no_subfolders:
        for fl in db:
            fl += SEPARATOR
            for sub in os.listdir(fl):
                sub = fl + sub
                if os.path.isdir(sub):
                    db.append(sub)

    # Compile a list of video files
    for fol in db:
        fol += SEPARATOR if fol[-1] != SEPARATOR else ""
        result += [fol + fil for fil in os.listdir(fol)]
    return [fil for fil in result if os.path.isfile(fil)]


def send_email(message):
    """
    Send an email report

    - message -- (String. Mandatory) The message to send.

    Returns: None
    """
    # Retrieve the email settings and check that all the required info is available
    settings = get_email_settings(args.email)
    if not settings:
        return
    elif not all([x in settings for x in("sender", "password", "recipient", "server", "port")]):
        print("Warning! Email settings file does not contain all the required data. An email report will not be sent.")
        return

    # Set data
    sender = settings["sender"]
    password = settings["password"]
    recipient = settings["recipient"]
    server = smtplib.SMTP_SSL(settings["server"], settings["port"])
    message = "Subject: {}\n\n{}".format("Status report from Video Converter", message)

    # Login and send the email
    server.login(sender, password)
    server.sendmail(sender, recipient, message.encode("utf8"))
    server.quit()


def set_timer(interval_mins):
    """
    Calculate when to check for new files next time

    - interval_mins -- (Integer. Mandatory) The time interval

    returns: Integer
    """
    return (interval_mins * 60) + time.time()


def update_history(file_to_add):
    """
    Add a file to the history db

    - file_to_add -- (String. Mandatory) The file to add to the database. Full path.

    Returns: None
    """
    db = get_history()
    db[file_to_add] = get_timestamp()
    with open(HISTORY_DB_FILE, "w+") as f:
        f.write(json.dumps(db))


# Classes
class Log(object):
    """Print a string to the console and also append it to a variable"""

    def __init__(self):
        self.text = ""

    def clear(self):
        """
        Clear the log

        Returns: None
        """
        self.text = ""

    def print(self, text, end="\n"):
        """
        Print text to the console and append it to the log

        - text -- (String. Mandatory) The text to print and add to the log
        - end -- (String. Optional. Defaults to "\n") Decides whether start end with line break or append the following
            line to this one

        Returns: None
        """
        print(text, end=end)
        self.text += text + end


# Parse arguments
parser = argparse.ArgumentParser(
    description="Convert the bitrate of all video files in given folders and check for new files at a given interval")
parser.add_argument(
    "folders", type=str, nargs="+",
    help="Can be either the path to a json-file containing a list of all folders to process or the list itself "
    "(comma separated)")
parser.add_argument(
    "-i", "--interval", type=int, default=60,
    help="Sets the interval (in minutes) when to check the folders for unprocessed files. Defaults to 60")
parser.add_argument(
    "-b", "--bitrate", type=str, default="8M", help="The requested bitrate. Defaults to '8M' for 8 Mbit/s")
parser.add_argument(
    "-e", "--email", type=str, default="",
    help="The path to a json-file containing the following keys: 'recipient', 'sender', 'password', 'server' and "
    "'port'. If provided an email report will be sent after processing is completed")
parser.add_argument(
    "--flush",
    help="Delete all the original files. Enabling this will skip video conversion. Only deletion will be performed.",
    action="store_true")
parser.add_argument("--no_subfolders", help="Don't look for video files in in sub-folders.", action="store_true")
args = parser.parse_args()

# Constants
HISTORY_DB_FILE = "history.json"
EMAIL_SETTINGS_FILE = "email_settings.json"
OS = platform.system()
OS_IS_WINDOWS = OS == "Windows"
OS_IN_LINUX = OS == "Linux"
OS_IS_MAC = OS == "Darwin"
SEPARATOR = "\\" if OS_IS_WINDOWS else "/"

# Set start values
timer = 0
log = Log()

# Only Linux and Windows supported at this time
if OS_IS_MAC:
    print("Get a real computer!")
    quit()

# Flush processed files if requested
if args.flush:
    flush()
    quit()

# Loop until user cancels execution
while True:

    processing_results = {}
    now = time.time()

    # Check if it's time to look for unprocessed files
    if now >= timer:

        log.print("\n{} - SCANNING FOLDERS FOR NEW VIDEO FILES".format(get_timestamp()))

        # Loop through the list of files and convert each one
        for video_file in get_video_files(args.folders):
            file_size_mb = os.path.getsize(video_file) / (1024*1024)
            log.print("Processing {0} ({1}MB)...".format(video_file, "%.2f" % file_size_mb))
            processing_result = convert(video_file, args.bitrate)
            processing_results[video_file] = processing_result
            log.print("OK" if processing_result else "Skipped")

        # Compile a report
        skipped_files = [x for x in processing_results if not processing_results[x]]
        processed_files = [x for x in processing_results if processing_results[x]]
        number_of_skipped_files = len(skipped_files)
        number_of_processed_files = len(processed_files)
        elapsed_time = int(time.time() - now)
        minutes = elapsed_time >= 60
        timer = set_timer(args.interval)
        log.print("\nRESULTS:")
        log.print("Processed files: {}".format(number_of_processed_files))
        log.print("Skipped files: {}".format(number_of_skipped_files))
        log.print("Elapsed time: {}".format(int(elapsed_time / 60) if minutes else elapsed_time), end=" ")
        log.print("minutes" if minutes else "seconds")
        log.print("Next scan scheduled for: {}".format(datetime.datetime.fromtimestamp(int(timer))))

        # Email the log
        if number_of_processed_files >= 1:
            send_email(log.text)
        log.clear()