import pygame, time
from mutagen.mp3 import MP3

current_playing={"name":"", "current_time": 0}

def play(file_path, fade_in_duration, fade_out_duration, start_time, end_time):
    global current_playing
    current_playing["name"]=file_path
    current_playing["current_time"]=0
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    audio_length = pygame.mixer.Sound(file_path).get_length()
    if end_time==0:
        end_time=audio_length
    pygame.mixer.music.set_volume(0.0)
    portion_duration = end_time - start_time
    total_duration = portion_duration + fade_in_duration + fade_out_duration
    pygame.mixer.music.play(start=int(start_time * 1000))
    for i in range(100):
        volume = i / 100.0
        pygame.mixer.music.set_volume(volume)
        time.sleep(fade_in_duration / 100.0 * portion_duration / total_duration)
    time.sleep(portion_duration)
    for i in range(100, 0, -1):
        volume = i / 100.0
        pygame.mixer.music.set_volume(volume)
        time.sleep(fade_out_duration / 100.0 * portion_duration / total_duration)
    pygame.mixer.music.stop()
    pygame.quit()

def get_mp3_length(file_path):
    try:
        audio = MP3(file_path)
        length_in_seconds = audio.info.length
        return length_in_seconds
    except Exception as e:
        return 0