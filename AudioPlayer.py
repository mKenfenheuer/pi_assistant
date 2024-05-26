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
    
    def duration(self) -> float:
        return self.player.get_length() / 1000.0
    
    def volume(self) -> float:
        return self.player.audio_get_volume()
    
    def next(self) -> float:
        return self.player.next()
    
    def prev(self) -> float:
        return self.player.previous()
    
    def stop(self) -> float:
        return self.player.stop()
    
    def set_volume(self, volume):
        return self.player.audio_set_volume(volume)
    
    def is_playing(self) -> bool:
        return self.player.is_playing()
    
    def playUrl(self, url):
        self.player.set_mrl(url)
        self.player.set_position(0)
        self.player.play()

    async def wait(self):
        while self.player.get_position() < 0.99 and self.player.get_position() >= 0:
            await asyncio.sleep(0.1)
    
    async def playUrlWait(self, url):
        self.playUrl(url)
        await asyncio.sleep(0.2)
        await self.wait()
        

        
