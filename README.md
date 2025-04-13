# 📰 AI-Powered Personalized Newsletter Generator

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![LLM](https://img.shields.io/badge/Groq-LLaMA3.1-8b-blueviolet?style=flat-square)

> Create personalized, AI-powered newsletters by summarizing RSS news articles using semantic NLP filtering and Groq’s blazing-fast LLaMA 3.1 model.

---

## 🌐 About the Project

This app helps users generate a customized newsletter based on their persona and interests. It:
- Fetches articles from relevant RSS feeds
- Uses spaCy to filter content using NLP similarity
- Extracts full article text
- Summarizes using **Groq's LLaMA 3.1** via LangChain
- Generates Markdown output with highlights + article summaries
- Allows easy download of the final `.md` file

---

## ✨ Features

- 👤 Choose from 5 user personas
- 📰 Auto-fetch articles from top RSS feeds
- 🧠 NLP filtering using spaCy (semantic match)
- 🦙 LLaMA 3.1 summaries via Groq API
- 🔥 Highlight section powered by LLM
- 📄 Download clean Markdown newsletter

---

## 👤 Personas

| Persona | Interests |
|--------|-----------|
| **Alex Parker** (USA) | AI, Cybersecurity, Blockchain, Startups |
| **Priya Sharma** (India) | Global Markets, Fintech, Crypto |
| **Marco Rossi** (Italy) | Football, F1, NBA, Esports |
| **Lisa Thompson** (UK) | Music, TV Shows, Celebs |
| **David Martinez** (Spain) | Space, Biotech, Physics, Renewable Energy |

---

## 🚀 How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/HarshWawa/ai-newsletter.git
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_md
```
### 3. Set Up Environment Variables
```bash
groqPass=your_groq_api_key_here
```
### 4. Launch the App
```bash
streamlit run app.py

