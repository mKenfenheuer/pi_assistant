import asyncio
from flask import Flask, json, request
import datetime

companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]

api = Flask(__name__)


@api.route("/api/command/<command>", methods=["POST"])
def command(command):
    print(request.json)
    return json.dumps({"success": True})


@api.route("/api/state", methods=["GET"])
def get_state():
    return json.dumps(
        {
            "state": "ON",
            "is_volume_muted": False,
            "media_duration": 300,
            "media_content_type": "url",
            "media_position": 120,
            "media_position_updated_at": datetime.datetime.now(),
            "repeat": False,
            "shuffle": False,
            "source": "Network",
            "volume_level": 0.9,
            "volume_step": 0.5,
        }
    )

async def flask_run():
    """Flask run"""
    api.run(host="0.0.0.0", port=5000)


async def main():
    loop = asyncio.get_event_loop()
    tasks = [
        flask_run(),
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

if __name__ == "__main__":
    asyncio.run(flask_run())
