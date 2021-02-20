import re
import datetime
from utils import timecode_to_seconds, seconds_to_timecode


TIMECODE_FORMAT_RE = r"^([\d\:].*?) (.*)$"


def read_timecodes(path):
    with open(path) as file:
        timecode_lines = file.readlines()

    timecodes = []

    for line in timecode_lines:
        matched = re.findall(TIMECODE_FORMAT_RE, line)

        if len(matched) == 0:
            continue

        timecode, title = matched[0]
        secs = timecode_to_seconds(timecode)
        ms = secs * 1000

        timecodes.append([ms, title])

    return timecodes


def write_timecodes(timecodes, path):
    with open(path, "w") as file:
        for timecode in timecodes:
            seconds = timecode[0] / 1000
            formatted_time = seconds_to_timecode(seconds)

            file.write("%s %s\n" % (formatted_time, timecode[1]))
