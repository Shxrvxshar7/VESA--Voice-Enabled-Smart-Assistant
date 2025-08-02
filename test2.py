from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_ollama import ChatOllama  # Correct import
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import Literal
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import ChatPromptTemplate

from RAG.rag import RAG

from test import vesa_agent

import re

import queue
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from vosk import Model, KaldiRecognizer
import json
import os
import sys

from voice_2_txt.ipex_whisper import voice2text as v2txt
from text2voice.text_to_voice import text_to_voice 

from shared_state import shared_dict


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
    response = classifier_chain.invoke({"input": r['text']})  # May be a dict like {"response": "The weather is..."}
    print("Classification Result:", response)
    
    if response["query_type"] == "tool":
        print("tool call")
        response = vesaAgent.get_response(r['text'])
        print("Tool Response:", response)
        robot.speak(response)

    else:
        print("message call")
        response = general_chain.invoke({"input": r['text']})
        print("General Response:", response)

        cleaned = re.sub(r'^[\s`"\n]*json[\s`"\n]*', '', response, flags=re.IGNORECASE)
        cleaned = cleaned.strip().removeprefix('```json').removesuffix('```').strip()
        cleaned = cleaned.strip('"\n ')

        parsed = json.loads(cleaned)
        print("Parsed JSON:", parsed)
        robot.speak(parsed['response'])

# agent
vesaAgent = vesa_agent()
vesaAgent.tool_init()
# Initialize RAG components
rag_classifier = RAG(".\\RAG\\data.json","label")
retriever = rag_classifier.retrive()

rag_general = RAG(".\\RAG\\general.json","response")
retriever_general = rag_general.retrive()

# Use ChatOllama instead of OllamaLLM
classifier_llm = ChatOllama(model="gemmaGpu", temperature=0.1)

general_llm = ChatOllama(model="gemmaGpu", temperature=0.3)

# agent

class QueryClassification(BaseModel):
    query_type: Literal["tool", "message"]

classification_parser = JsonOutputParser(pydantic_object=QueryClassification)

# Improved prompt template
classifier_template = """You are a home assistant classifier. Analyze the user's query and determine if it requires:
1. A tool to be executed (e.g., turning on lights, checking temperature) or
2. A message to be sent (e.g., asking for help, general conversation).

Respond ONLY with JSON format containing the classification.

Context of available tools: {context}

User query: {input}

Example response for "Turn on the lights": {{"query_type": "tool"}}
Example response for "How are you?": {{"query_type": "message"}}
"""

classifier_prompt = ChatPromptTemplate.from_template(classifier_template)

# Fixed chain structure
classifier_chain = (
    {
        "context": lambda x: retriever.invoke(x["input"]),
        "input": lambda x: x["input"]
    }
    | classifier_prompt
    | classifier_llm
    | classification_parser
)

general_prompt = ChatPromptTemplate.from_template(
    """You are a home assistant Named ADAM. Respond to the user's query in a helpful manner based on the given context,
   Respond ONLY with JSON without code formatting, no markdowns.
    Context of example responses: {context}
    User query: {input}

    """

    
)
# Fixed chain structure
general_chain = (
    {
        "context": lambda x: retriever_general.invoke(x["input"]),
        "input": lambda x: x["input"]
    }
    | general_prompt
    | general_llm
    | StrOutputParser()
)
# Test with proper error handling
try:

    while True:
        listen_for_keyword()
        

        

except Exception as e:
    print(f"Error: {str(e)}")
    print("VESA STOPPED")



 
    