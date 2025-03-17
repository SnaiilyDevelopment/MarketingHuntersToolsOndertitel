import moviepy.editor as mp
import pysrt

def sync_srt(video_path, srt_path, output_path):
    """
    Synchronizes an SRT file with a video file based on a calculated time offset.
    """
    try:
        # Load the video file
        video = mp.VideoFileClip(video_path)
        audio = video.audio

        # Load the SRT file
        subs = pysrt.open(srt_path)

        # --- Basic Offset Calculation (Assumes constant offset) ---
        # 1. Find the start time of the first subtitle.
        first_subtitle_start = (
            subs[0].start.hours * 3600 +
            subs[0].start.minutes * 60 +
            subs[0].start.seconds +
            subs[0].start.milliseconds / 1000.0
        )

        # 2.  Estimate the audio start time (This is a simplification. A more robust
        #     solution would analyze the audio for the first significant sound.)
        audio_start_time = 0.0

        # 3. Calculate the offset.
        offset = first_subtitle_start - audio_start_time

        # --- Apply the offset to all subtitles ---
        for sub in subs:
            sub.start.hours = int(sub.start.hours + (offset / 3600))
            sub.start.minutes = int(sub.start.minutes + ((offset % 3600) / 60))
            sub.start.seconds = int(sub.start.seconds + ((offset % 3600) % 60))
            sub.start.milliseconds = int((sub.start.milliseconds / 1000 + offset - int(offset)) * 1000)

            sub.end.hours = int(sub.end.hours + (offset / 3600))
            sub.end.minutes = int(sub.end.minutes + ((offset % 3600) / 60))
            sub.end.seconds = int(sub.end.seconds + ((offset % 3600) % 60))
            sub.end.milliseconds = int((sub.end.milliseconds / 1000 + offset - int(offset)) * 1000)

        # Save the corrected SRT file
        subs.save(output_path, encoding='utf-8')
        video.close()
        return f"Success! Synced SRT saved as: {output_path}"

    except Exception as e:
        if 'video' in locals():
            video.close()
        return f"Error: {str(e)}"
