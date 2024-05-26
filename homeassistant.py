import asyncio
import websockets
import json
import numpy as np

class HomeAssistant:
    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.state = "waiting"
        self.stt_binary_handler_id = -1
        self.id = 1
        self.event_receiver: asyncio.Task = None

    async def connect(self) -> bool:
        self.websocket = await websockets.connect(self.url)
        response = await self.websocket.recv()
        if response == None:
            return False
        data = json.loads(response)
        await self.websocket.send(json.dumps({'type': 'auth','access_token': self.token}),)
        response = await self.websocket.recv()
        if response == None:
            return False
        data = json.loads(response)
        return data["type"] == "auth_ok"
    
    async def startPipeline(self) -> bool:
        request = json.dumps({
            "id": self.id,
            "type": "assist_pipeline/run",
            "start_stage": "stt",
            "end_stage": "tts",
            "input": {
                "sample_rate": 16000,
            }
        })
        self.id += 1
        await self.websocket.send(request)
        
        #Receive request result
        frame = await self.websocket.recv()
        if frame is None:
            return False
        data = json.loads(frame)
        if data["success"] == False:
            return False
        
        #Receive run-start event
        frame = await self.websocket.recv()
        if frame is None:
            return False
        data = json.loads(frame)
        if data["event"]["type"] != "run-start":
            return False
        self.stt_binary_handler_id = data["event"]["data"]["runner_data"]["stt_binary_handler_id"]

        #Receive stt-start event
        frame = await self.websocket.recv()
        if frame is None:
            return False
        data = json.loads(frame)
        if data["event"]["type"] != "stt-start":
            return False
                
        return True
    
    async def readEvent(self):
        frame = await self.websocket.recv()
        if frame is None:
            return False
        data = json.loads(frame)
        return data
    
    async def waitForEvent(self, event):
        data = await self.readEvent()
        while data["event"]["type"] != event:
            data = await self.readEvent()
        return data
    
    async def sendAudio(self, frame: np.ndarray):
        data = np.array(self.stt_binary_handler_id, dtype = np.uint8).tobytes() + frame.tobytes()
        await self.websocket.send(data)
        if self.event_receiver is None:
            self.event_receiver = asyncio.create_task(self.websocket.recv(), name="recv")
            return False
        if self.event_receiver.done():
            frame = self.event_receiver.result()
            self.event_receiver = None
            if frame is None:
                return False
            data = json.loads(frame)
            if(data["event"]["type"] == "stt-end"):                
                return True
        return False
            

        
        
