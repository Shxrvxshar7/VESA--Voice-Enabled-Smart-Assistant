import whisper
import intel_extension_for_pytorch as ipex

import warnings
warnings.filterwarnings("ignore") # disable warnings


class voice2text():

    def __init__(self,MODEL="small.en"):
        #load the small.en as default
        self.model = whisper.load_model(MODEL, device = "xpu")

    def transcribe(self, audio_path):
        result = self.model.transcribe(audio_path)
        return result
