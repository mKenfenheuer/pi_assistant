import asyncio
from flask import Flask, json, request
import datetime

from AudioPlayer import AudioPlayer

audioPlayer = AudioPlayer()
api = Flask(__name__)


@api.route("/api/command/<command>", methods=["POST"])
def command(command):
    print(request.json)
    return json.dumps({"success": True})

@api.route("/api/command/set_volume", methods=["POST"])
def set_volume():
    audioPlayer.set_volume(int(request.json["volume"] * 100))
    return json.dumps({"success": True})

@api.route("/api/command/media_play", methods=["POST"])
def media_play():
    audioPlayer.resume()
    return json.dumps({"success": True})

@api.route("/api/command/media_next", methods=["POST"])
def media_next():
    audioPlayer.next()
    return json.dumps({"success": True})

@api.route("/api/command/media_prev", methods=["POST"])
def media_prev():
    audioPlayer.prev()
    return json.dumps({"success": True})

@api.route("/api/command/media_pause", methods=["POST"])
def media_pause():
    audioPlayer.pause()
    return json.dumps({"success": True})

@api.route("/api/command/media_stop", methods=["POST"])
def media_stop():
    audioPlayer.stop()
    return json.dumps({"success": True})

@api.route("/api/command/media_seek", methods=["POST"])
def media_seek():
    position = request.json["position"]
    if position > 1:
        position /= audioPlayer.duration()
    audioPlayer.seek(position)
    return json.dumps({"success": True})

@api.route("/api/command/play_media", methods=["POST"])
def play_media():
    audioPlayer.playUrl(request.json["url"])
    return json.dumps({"success": True})


@api.route("/api/state", methods=["GET"])
def get_state():
    return json.dumps(
        {
            "state": "playing" if audioPlayer.is_playing() else ("paused" if audioPlayer.position() >= 1 else "idle"),
            "is_volume_muted": audioPlayer.volume() == 0,
            "media_duration": int(audioPlayer.duration()),
            "media_content_type": "url",
            "media_position": int(audioPlayer.position() * audioPlayer.duration()),
            "media_position_updated_at": datetime.datetime.now(),
            "repeat": False,
            "shuffle": False,
            "source": "Network",
            "volume_level": audioPlayer.volume() / 100.0,
            "volume_step": 0.05,
        }
    )

async def flask_run():
    """Flask run"""
    api.run(host="0.0.0.0", port=5000)


async def main():
    tasks = [
        asyncio.create_task(flask_run()),
    ]
    await asyncio.wait(tasks)

if __name__ == "__main__":
    asyncio.run(main())
