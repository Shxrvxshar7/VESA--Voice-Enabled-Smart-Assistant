# 🎙️ VESA – Voice-Enabled Smart Assistant  

A **sophisticated AI-powered voice assistant** combining **RAG (Retrieval-Augmented Generation)**, **Agentic AI**, and **real-time voice interaction** for intelligent, hands-free assistance.  

---

## ✨ Features  

### 🗣️ **Voice Interaction**  
- **Wake Word Detection** → Always-on listening with trigger word `"adam"`  
- **Speech Recognition**:  
  - **Vosk** → Lightweight, offline speech recognition  
  - **Whisper** → High-accuracy transcription model  
- **Text-to-Speech** → Natural-sounding voice responses  

---

### 🧠 **Intelligent Processing**  

#### 📚 **Retrieval-Augmented Generation (RAG)**  
- **FAISS Vector Store** for fast similarity search  
- **Two Dedicated RAG Pipelines**:  
  1. **Query Classification** → (`RAG/data.json`)  
  2. **General Knowledge Base** → (`RAG/general.json`)  
- **Ollama Embeddings** for semantic search and retrieval  

---

#### 🤖 **Agentic AI System**  
- Built using **LangChain** for structured reasoning  
- **Zero-Shot Reaction Agents** for flexible task execution  
- **Modular Tool System**:  
  - Indoor temperature monitoring  
  - Easily expandable with custom tools  

---

## 🏗️ Project Structure  
```plaintext
VESA/
├── RAG/
│   ├── data.json             # Classification training data
│   ├── general.json          # General knowledge base
│   └── rag.py                # RAG implementation
├── voice_2_txt/
│   └── ipex_whisper.py       # Voice transcription
├── text2voice/
│   └── text_to_voice.py      # Speech synthesis
└── models/
    └── vosk-model-small-en-us-0.15/  # Offline speech recognition model
```

## 📸 Screenshots
![Screenshot of VESA](Screenshot%202025-08-02%20193613.png)



## ⚙️Setup

1. Install dependencies:
```sh
pip install -r requirements.txt
```

2. Ensure you have the required models:
   - Vosk model in `models/vosk-model-small-en-us-0.15/`
   - Local Ollama instance with gemmaGpu model

3. Run the assistant:
```sh
python vesa.py
```

## Dependencies

- langchain
- langchain-ollama
- vosk
- sounddevice
- scipy
- FAISS
- whisper
- ollama
