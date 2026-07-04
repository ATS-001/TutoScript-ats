# ⚡ TutoScript

An efficient, modular Retrieval-Augmented Generation (RAG) dashboard designed to parse YouTube video transcripts, index text segments into a local vector storage unit, and generate real-time contextual question-answering streams alongside synchronized video playback.

🚀 **Live Demo:** [Launch App on Streamlit Community Cloud](https://share.streamlit.io)

---

## 📅 Workshop Context

* **Event:** Day 5 of Projectathon conducted by μLearn LBSITW (1st July 2026)
* **Presented by:** Darshana D Devi, AI & ML IG LEAD, µLearn LBSITW
* **Focus:** Deep dive into video data ingestion, transcript fetching pipelines, semantic text splitting chunk optimizations, local vector database processing, and high-performance Groq LLM API architectures.

---

## ✨ Features

* **Synchronized Media Viewport:** Features an integrated side-by-side workspace combining native YouTube media streaming with an interactive conversational chat system.
* **Local Context Indexing:** Utilizes HuggingFace's `all-MiniLM-L6-v2` transformer pipelines to vectorize transcript data and index them inside a local FAISS structural framework.
* **Ultra-Low Latency Inference:** Leverages Llama 3.3 70B through the Groq hardware acceleration cloud to deliver split-second synthesis and accurate educational answer loops.
* **Synchronized State Machine:** Features an explicit, one-click ❌ Clear Conversation callback filter that purges caching variables and text inputs instantly to eliminate stale memory or interface breakage.
* **White-Label Custom UI:** Customized theme injections that completely strip out standard development toolbars and inject a dark terminal-style slate canvas.

---

## 🛠️ Architecture & Tech Stack

* **Frontend Framework:** Streamlit (Python-driven reactive web UI)
* **Vector Database & Indexes:** FAISS (Facebook AI Similarity Search)
* **Embedding Pipelines:** LangChain & HuggingFace Transformers (`all-MiniLM-L6-v2`)
* **LLM Engine Architecture:** Llama 3.3 70B via Groq API
* **Data Processing Toolkit:** Pytube & YouTube Transcript API
* **Repository Architecture:** GitHub Cloud Ecosystem

---

## 🚀 Local Setup & Installation

If you want to run this application locally on your machine, follow these steps:

### 1. Clone the Repository
```bash
git clone [https://github.com/ATS-001/TutoScript-ats.git](https://github.com/ATS-001/TutoScript-ats.git)
cd yt_transcriber
```
### 2. Install System Dependencies
Ensure you have Python installed, then run the pip installation wrapper:
```bash
pip install -r requirements.txt
pip install torchvision --index-url [https://download.pytorch.org/whl/cpu](https://download.pytorch.org/whl/cpu)
```

### 3. Configure Local Environment Secrets
Create a hidden file named .env in the root folder of your project to store local session variables securely:

```
GROQ_API_KEY = "your_actual_groq_api_key_here"
```

### 4. Execute the Application
```bash
streamlit run app.py
```

---

## 🔮 Acknowledgments
Special thanks to Darshana D Devi ([LinkedIn Profile](https://www.linkedin.com/in/darshana-d-devi-1b1094326/)) for providing the foundational dataset structural guidelines and the hands-on workshop instruction regarding Roboflow integration that enabled this end-to-end model training and application deployment.

---

### 👨‍💻 Developer Profile
* **Name:** Aaron Thalakkottor Sooraj
* **Degree:** B.Tech in Computer Science Engineering (CSE)
* **Institution:** Vidya Academy of Science and Technology, Thrissur

---

### 📜 License
```text
COPYRIGHT © Since 2023 ATS-PDZ - ALL RIGHTS RESERVED.
```
