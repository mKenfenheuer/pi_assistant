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
import pyaudio
import numpy as np
import openwakeword
from openwakeword.model import Model

openwakeword.utils.download_models()

import pyaudio
import wave

class WakewordDetector:
    def __init__(self, models=["models/hey_jarvis_v0.1.tflite"]):
        self.model = Model(wakeword_models=models)
        self.running = True

    def reset(self):
        self.model.reset()

    def detect(self, frame):
        # Feed to openWakeWord model
        prediction = self.model.predict(frame)            

        for mdl in self.model.prediction_buffer.keys():
            # Add scores in formatted table
            scores = list(self.model.prediction_buffer[mdl])
            if scores[-1] >= 0.5:
                return True