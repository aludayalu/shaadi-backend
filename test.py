from pydub import AudioSegment
import os

def process_audio_batch(songs, export_path):
    export_path="songs/"+export_path

    # Initialize an empty audio segment for the final result
    final_audio = AudioSegment.silent(duration=0)

    # Process each song in the array
    for song in songs:
        name = song["name"]
        start_time_sec = song["start"]
        end_time_sec = song["stop"]
        fade_in_sec = song["fade_in"]
        fade_out_sec = song["fade_out"]

        # Set the start and end times in milliseconds
        start_time = start_time_sec * 1000
        end_time = end_time_sec * 1000

        # Set fade in and fade out durations in milliseconds
        fade_in_duration = int(fade_in_sec * 1000) + 1
        fade_out_duration = int(fade_out_sec * 1000) + 1

        # Load the audio file
        audio = AudioSegment.from_file("songs/"+name+".mp3", format="mp3")

        # Trim the audio based on start and end times
        trimmed_audio = audio[start_time:end_time]

        # Apply fade in and fade out
        faded_audio = trimmed_audio.fade_in(fade_in_duration).fade_out(fade_out_duration)

        # Append the processed audio to the final result
        final_audio += faded_audio

    # Generate the output file name
    output_file = export_path

    # Export the final merged audio to the specified path
    final_audio.export(output_file, format="mp3")

    print(f"Audio processing complete. Merged file exported to: {output_file}")
