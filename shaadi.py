import main, pygame, time, threading
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
db=main.db
groups=main.db.get("groups")
next_group=groups[0]
playing=False
pause=False

def play_mp3(file_path):
    global playing, pause
    playing=True
    pygame.init()
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            if pause:
                pygame.mixer.quit()
                pygame.quit()
                pause=False
            playing=True
    except Exception as e:
        print(f"Error: {e}")
    finally:
        pygame.mixer.quit()
        pygame.quit()
    playing=False

@main.app.get("/current_group")
def current_group():
    return main.make_response(next_group)

threading.Thread(target=main.app.run).start()
i=0
while True:
    i+=1
    songs=db.get("group_"+next_group)["songs"]
    if len(songs)!=0:
        option=input("Continue or Forced Index? (1/2)")
        if option=="" or option=="1":
            print("Start Export of Group "+next_group)
            input("...")
            print(songs)
            main.test.process_audio_batch(songs, "group_export"+str(i)+".mp3")
            print("Group export ready")
            input("...")
            playing=True
            threading.Thread(target=play_mp3, args=("songs/group_export"+str(i)+".mp3",)).start()
            while True:
                if playing==False:
                    break
                option=input(">> ")
                if option=="pause":
                    pause=True
                if option=="play":
                    threading.Thread(target=play_mp3, args=("songs/group_export"+str(i)+".mp3",)).start()
                if option=="skip":
                    pause=True
                    time.sleep(1.5)
                    playing=False
                    continue
        else:
            while True:
                try:
                    j=-1
                    for x in db.get("groups"):
                        j+=1
                        print(f"{j} : {x}")
                    next_group=db.get("groups")[int(input())]
                    break
                except:
                    continue
            continue
    try:
        next_group=main.db.get("groups")[main.db.get("groups").index(next_group)+1]
    except:
        break
print("W")