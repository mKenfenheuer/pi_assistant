import asyncio
import vlc

class AudioPlayer:
    def __init__(self):
        self.player = vlc.MediaPlayer()

    def pause(self):
        self.player.set_pause(True)

    def resume(self):
        self.player.set_pause(False)   

    def seek(self, position):
        self.player.set_position(position)
    
    def position(self) -> float:
        return self.player.get_position()
    
    def is_playing(self) -> bool:
        return self.player.is_playing()
    
    def playUrl(self, url):
        self.player.set_mrl(url)
        self.player.audio_set_volume(100)
        self.player.set_position(0)
        self.player.play()

    async def wait(self):
        while self.player.get_position() < 0.99 and self.player.get_position() >= 0:
            await asyncio.sleep(0.1)
    
    async def playUrlWait(self, url):
        self.playUrl(url)
        await asyncio.sleep(0.2)
        await self.wait()
        

        
