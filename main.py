import queue
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from vosk import Model, KaldiRecognizer
import json
import os
import sys

from voice_2_txt.ipex_whisper import voice2text as v2txt

#llm for response generation
from llm import agent
from text2voice.text_to_voice import text_to_voice 
#agent
assistant = agent(model="mistralAgent:latest")
# Load the Vosk model
#t2v
robot = text_to_voice()
model_path = "models/vosk-model-small-en-us-0.15"
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

# load the whisper mode (needs to change)
whisper = v2txt()

# queue to hold audio data
audio_queue = queue.Queue()
# callback function to process audio data
def callback(indata,frames,time,status):
    if status:
        print(status, file=sys.stderr)
    audio_queue.put(bytes(indata))

def listen_for_keyword(keyword = "adam",record_seconds=5):
    print("Listening for keyword...")
    # Start the audio stream
    with sd.RawInputStream(samplerate=16000,blocksize=8000,dtype='int16',channels=1,callback=callback):
        print('Listening')
        while True:
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                print(result)
                if keyword in result.get('text', ''):
                    print("Keyword detected!")
                    print(result)
                    break
    print("Keyword detected, recording...")
    record_wav(record_seconds)

def record_wav(record_seconds):
    robot.speak("Hello!")
    print("Hello! whats up") # need a voice tts
    recording = sd.rec(int(record_seconds * 16000), samplerate=16000, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished  
    print("Recording finished,Saving..")
    wav.write("output.wav", 16000, recording)
    print("Saved to output.wav")
    #invoke whisper
    convert_voice_to_txt()

def convert_voice_to_txt(path='output.wav'):
    r = whisper.transcribe(path)
    print(f"whisper result: {r['text']}")
    if 'temperature' in r['text'] or 'weather' in r['text']:
        robot.speak("Let me check")
    else:
        robot.speak("Hmm hmm")
    #invoke llm agent
    response_data = assistant.get_response(r['text'])  # May be a dict like {"response": "The weather is..."}
    print(f"Assistant response: {response_data}")



    robot.speak(response_data)

while True:
    listen_for_keyword()
