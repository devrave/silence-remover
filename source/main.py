from pydub import AudioSegment
from SilenceRemover import SilenceRemover
from timecode import read_timecodes, write_timecodes
from utils import pretty_milliseconds, parse_arguments, format_percent


if __name__ == "__main__":
    arguments = parse_arguments()

    audio_path = arguments.audio
    timecodes_path = arguments.timecodes
    silence_length = arguments.silence_length
    silence_threshold = arguments.silence_threshold

    timecodes = None

    if timecodes_path:
        timecodes = read_timecodes(timecodes_path)

    print("Loading the file...")
    audio = AudioSegment.from_file(audio_path)
    length_before = len(audio)

    print("Removing silence parts...")
    silence_remover = SilenceRemover(audio, timecodes)
    silence_remover.remove(silence_length, silence_threshold, lambda done_percentage: format_percent(done_percentage))

    print("Saving...")
    silence_remover.audio.export("output.mp3", format="mp3")

    if timecodes_path:
        write_timecodes(silence_remover.timecodes, "output.timecodes")

    length_after = len(silence_remover.audio)
    length_after_percent = 100 - ((length_after * 100) / length_before)

    print("Done.")
    print("Before removing:", pretty_milliseconds(length_before))
    print("After removing:", pretty_milliseconds(length_after))
    print(f"Removed {format_percent(length_after_percent)}%")
