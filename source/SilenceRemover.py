from pydub import AudioSegment
from pydub.silence import detect_silence


class SilenceRemover:
    def __init__(self, audio, timecodes):
        self._audio = audio
        self._timecodes = timecodes

    @property
    def audio(self):
        return self._audio

    @property
    def timecodes(self):
        return self._timecodes

    def remove(self, silence_length, silence_threshold, progress_viewer=None):
        silence_times = detect_silence(self._audio, min_silence_len=silence_length, silence_thresh=silence_threshold)

        if len(silence_times) == 0:
            return self._audio

        silence_length = len(silence_times)
        removed_count = 0

        for silence in reversed(silence_times):
            start, end = silence
            removed_count += 1
            removed_length = end - start

            if self._timecodes:
                self.__move_timecodes(start, removed_length)

            start_audio = self._audio[0:start]
            end_audio = self._audio[end:]

            self._audio = start_audio + end_audio

            if progress_viewer:
                done_percentage = (removed_count * 100) / silence_length

                progress_viewer(done_percentage)

    def __move_timecodes(self, start, length):
        def move(timecode):
            ms = timecode[0]

            if ms > start:
                timecode[0] = ms - length

            return timecode

        self._timecodes = list(map(move, self._timecodes))
