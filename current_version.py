import player, flask, json, os, downloader

from litedb import Database

from flask import Flask, request

app=Flask(__name__)
app.config["UPLOAD_FOLDER"]="songs"

db=Database("shaadi")

def Song(name, start, stop, fade_in, fade_out):
    return {"name":name, "start":start, "stop":stop, "fade_in":fade_in, "fade_out":fade_out}

def Group(name, songs):
    return {"name":name, "songs":songs}

def reset():
    db.set("groups", [])

def make_response(data):
    if type(data)!=str:
        try:
            data=json.dumps(data)
        except:
            pass
    if type(data)==flask.Response:
        resp=data
        resp.headers["Content-Type"]="audio/mp3"
    else:
        resp=flask.Response(data)
        resp.headers["Content-Type"]="application/json"
    resp.headers["Access-Control-Allow-Origin"]="*"
    return resp

@app.route("/upload")
def upload_file():
    args=dict(request.args)
    if "url" not in args:
        return make_response(False)
    if "name" not in args:
        return make_response(False)
    name=args["name"]
    url=args["url"]
    if "instagram" in url:
        return make_response(downloader.download_instagram_audio(url, name))
    if "youtube" in url:
        return make_response(downloader.download_youtube_audio(url, name))
    return make_response(False)

@app.route("/groups")
def get_groups():
    groups=db.get("groups")
    new_groups=[]
    for x in groups:
        if x!={}:
            new_groups.append(x)
    return make_response(new_groups)

@app.route("/group")
def get_group():
    args=dict(request.args)
    if "group" not in args:
        return make_response(False)
    return make_response(db.get("group_"+args["group"]))

@app.route("/add_group")
def add_group():
    args=dict(request.args)
    if "group" not in args:
        return make_response(False)
    name=args["group"]
    db.set("groups", db.get("groups")+[name])
    db.set("group_"+name, Group(name, []))
    return make_response(True)

@app.route("/add_song_to_group")
def add_song_to_group():
    args=dict(request.args)
    if "group" not in args:
        return make_response(False)
    if "song" not in args:
        return make_response(False)
    name=args["group"]
    song=args["song"]
    group=db.get("group_"+name)
    group["songs"].append(Song(song, 0, player.get_mp3_length("songs/"+song+".mp3"), 0, 0))
    print(group)
    db.set("group_"+name, group)
    return make_response(True)

@app.route("/delete_group")
def delete_group():
    args=dict(request.args)
    if "group" not in args:
        return make_response(False)
    name=args["group"]
    groups=[]
    for x in db.get("groups"):
        if x!=name:
            groups.append(x)
    db.set("groups", groups)
    db.set("group_"+name, {})
    return make_response(True)

@app.route("/set_group")
def set_group():
    args=dict(request.args)
    if "group" not in args:
        return make_response(False)
    if "songs" not in args:
        return make_response(False)
    name=args["group"]
    songs=json.loads(args["songs"])
    db.set("group_"+name, Group(name, songs))
    return make_response(True)

@app.route("/group_action")
def group_action():
    args=dict(request.args)
    if "group" not in args:
        return make_response(False)
    if "action" not in args:
        return make_response(False)
    action=args["action"]
    group=args["group"]
    groups=db.get("groups")
    group_index=groups.index(group)
    print(action, group)
    if action=="minus":
        groups[group_index+1],groups[group_index]=groups[group_index],groups[group_index+1]
    if action=="plus":
        groups[group_index-1],groups[group_index]=groups[group_index],groups[group_index-1]
    db.set("groups", groups)
    return make_response(True)

@app.route("/song_action")
def song_action():
    args=dict(request.args)
    if "group" not in args:
        return make_response(False)
    if "action" not in args:
        return make_response(False)
    if "song" not in args:
        return make_response(False)
    action=args["action"]
    group=db.get("group_"+args["group"])
    song=args["song"]
    song_index=0
    i=-1
    for x in group["songs"]:
        i+=0
        if x["name"]==song:
            song_index=i
            break
    print(action, group, song)
    if action=="minus":
        group["songs"][song_index+1],group["songs"][song_index]=group["songs"][song_index],group["songs"][song_index+1]
    if action=="plus":
        group["songs"][song_index-1],group["songs"][song_index]=group["songs"][song_index],group["songs"][song_index-1]
    db.set("group_"+args["group"], group)
    return make_response(True)

@app.get("/songs")
def get_songs():
    return make_response([x[::-1].split(".", 1)[1][::-1] for x in os.listdir("songs") if ("sothiswasedited" not in x and "_original" not in x)])

@app.get("/song")
def get_song():
    args=dict(request.args)
    if "song" not in args:
        return make_response(False)
    print(player.get_mp3_length("songs/"+args["song"]))
    return make_response(flask.send_from_directory("songs", args["song"]))

@app.get("/set_song")
def set_song():
    args=dict(request.args)
    if "song" not in args:
        return make_response(False)
    song=args["song"]
    if "group" not in args:
        return make_response(False)
    groupname=args["group"]
    if "fadein" not in args:
        return make_response(False)
    fadein=float(args["fadein"])
    if "fadeout" not in args:
        return make_response(False)
    fadeout=float(args["fadeout"])
    if "start" not in args:
        return make_response(False)
    start=float(args["start"])
    if "stop" not in args:
        return make_response(False)
    stop=float(args["stop"])
    if "out" not in args:
        return make_response(False)
    out=args["out"]
    group=db.get("group_"+groupname)
    i=-1
    for x in group["songs"]:
        i+=1
        if x["name"]==song:
            group["songs"][i]=Song(song, start, stop, fadein, fadeout)
            print(group)
    db.set("group_"+groupname, group)
    print(start, stop, fadein, fadeout)
    if start==0:
        start=0.01
    if stop==0:
        exit()
        return remove_song
    if fadein==0:
        fadein=1
    if fadeout==0:
        fadeout=1
    fadein=int(fadein)
    fadeout=int(fadeout)
    print(start, stop, fadein, fadeout)
    downloader.process_audio(song, out, start, stop, fadein, fadeout)
    return make_response(True)

@app.get("/remove_song")
def remove_song():
    args=dict(request.args)
    if "song" not in args:
        return make_response(False)
    song=args["song"]
    if "group" not in args:
        return make_response(False)
    groupname=args["group"]
    group=db.get("group_"+groupname)
    new_songs=[]
    for x in group["songs"]:
        if x["name"]!=song:
            new_songs.append(x)
    group["songs"]=new_songs
    db.set("group_"+groupname, group)
    return make_response(True)

@app.get("/remove_group")
def remove_group():
    args=dict(request.args)
    if "group" not in args:
        return make_response(False)
    groupname=args["group"]
    db.set("groups", [x for x in db.get("groups") if x!=groupname])
    return make_response(True)

app.run()