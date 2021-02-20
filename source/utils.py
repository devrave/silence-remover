import argparse
import datetime as dt
import humanize


DEFAULT_MIN_SILENCE_LENGTH = 500
DEFAULT_SILENCE_THRESHOLD = -50


def parse_arguments():
    parser = argparse.ArgumentParser(description="Podcast silence remover")
    parser.add_argument("--audio", type=str, help="audio file path", required=True)
    parser.add_argument("--timecodes", type=str, help="timecodes file path")
    parser.add_argument("--silence-length", type=int, help="silence length", default=DEFAULT_MIN_SILENCE_LENGTH)
    parser.add_argument("--silence-threshold", type=int, help="silence threshold", default=DEFAULT_SILENCE_THRESHOLD)

    return parser.parse_args()


def pretty_milliseconds(ms):
    delta = dt.timedelta(milliseconds=ms)

    return humanize.precisedelta(delta)


def timecode_to_seconds(timecode):
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(timecode.split(":"))))


def seconds_to_timecode(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)

    if hour > 0:
        return "%d:%02d:%02d" % (hour, min, sec)
    else:
        return "%02d:%02d" % (min, sec)


def format_percent(value):
    return "{:.2f}".format(value)
