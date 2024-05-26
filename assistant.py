# Copyright 2022 David Scripka. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Imports
import asyncio
from wakeword import WakewordDetector
from AudioRecorder import AudioRecorder
from AudioPlayer import AudioPlayer
from homeassistant import HomeAssistant
from pixels import pixels


class Assistant:
    def __init__(self, url, token, model= "models/hey_jarvis_v0.1.tflite") -> None:
        self.audioRecorder = AudioRecorder()
        self.audioPlayer = AudioPlayer()
        self.detector = WakewordDetector(models=[model]);
        self.ha = HomeAssistant(url, token)

    async def onDetected(self):
        self.audioPlayer.playUrl("sounds/wake1.mp3")
        #pixels.listen()
        await self.ha.startPipeline()
        complete = False
        while complete is False:
            frame = self.audioRecorder.getRecordedFrame()
            complete = await self.ha.sendAudio(frame)

        self.audioRecorder.stopRecording()
        self.audioPlayer.playUrl("sounds/thinking.mp3")
        #pixels.think()
        data = await self.ha.waitForEvent("tts-end")    
        #pixels.speak()
        await self.audioPlayer.playUrlWait("https://ha.ksol.it" + data["event"]["data"]["tts_output"]["url"])
        data = await self.ha.waitForEvent("run-end")
        #pixels.off()

    async def pipelineStart(self):
        self.audioRecorder.startRecording()
        while True:
            frame = self.audioRecorder.getRecordedFrame()
            if self.detector.detect(frame) == True:
                print ("Detected!")
                self.detector.reset()
                return await self.onDetected()

    async def run(self):
        #pixels.off()
        connect_result = await self.ha.connect()

        if connect_result == False:
            print("Connection to HA failed. Restarting in 5 seconds.")
            asyncio.sleep(5)
            return
        
        print("Connected to HomeAssistant!")
        while True:
            await self.pipelineStart()
        

if __name__ == "__main__":
    while True:
        asyncio.run(Assistant().run())

