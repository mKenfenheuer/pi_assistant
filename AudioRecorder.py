import pyaudio
import numpy as np

class AudioRecorder:
    def __init__(self, format = pyaudio.paInt16, channels = 1, rate = 16000, chunk_size = 1280):
        self.format = format
        self.channels = channels
        self.rate = rate
        self.chunk_size = chunk_size
        self.audio = pyaudio.PyAudio()
        self.stream : pyaudio.Stream = None

    def startRecording(self):
        self.stream = self.audio.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk_size)

    def stopRecording(self):
        self.stream.close()

    def getRecordedFrame(self):
        return np.frombuffer(self.stream.read(self.chunk_size), dtype=np.int16)