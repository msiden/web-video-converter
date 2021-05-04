import ffmpeg
from video_converter.pool import VideoFile


class BitRateConverter(object):

    @staticmethod
    def process_item(item: VideoFile, bitrate: str) -> bool:
        passed = True
        output_file = item.output.format(bitrate)
        stream = ffmpeg.input(item.path)
        stream = ffmpeg.output(stream, output_file, video_bitrate=bitrate)
        try:
            ffmpeg.run(stream, quiet=True)
        except ffmpeg.Error:
            passed = False
        return passed
