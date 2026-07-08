# 🤖 SafeX FAQ Chatbot

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-TF--IDF-orange?logo=scikitlearn&logoColor=white)
![Status](https://img.shields.io/badge/Status-Prototype-brightgreen)

A retrieval-based FAQ chatbot for **SafeX Solutions**, built as an AI/ML prototype
during my internship at SafeX Solutions.

The chatbot answers common questions about SafeX Solutions — its services,
products, contact details, and internship opportunities — by matching user
questions against a curated FAQ dataset using **TF-IDF + cosine similarity**.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Running the Chatbot](#running-the-chatbot)
- [How It Works](#how-it-works)
- [Dataset](#dataset)
- [Results](#results)
- [Notes & Limitations](#notes--limitations)

---
## 🔗 Live Demo

Try it here: **https://safex-faq-chatbot-bxd7enhyyatghwpg5yedrd.streamlit.app** 

![SafeX Chatbot Screenshot](screenshot/your-image-filename.png)
## Overview

SafeX Solutions' website did not have a dedicated FAQ page at the time of this
project. This chatbot fills that gap — visitors, prospective clients, and
students interested in internships can get instant answers instead of manually
browsing multiple pages across SafeX's main site and subdomains.

## Project Structure

```
safex-faq-chatbot/
├── assets/
│   └── icon.png                # SafeX logo icon
├── chatbot/
│   ├── __init__.py             # Package entry point
│   ├── chatbot.py               # Main SafeXFAQChatbot class
│   ├── model.py                 # TF-IDF matching model (FAQModel)
│   └── preprocess.py            # Text cleaning utilities
├── data/
│   └── SafeX_FAQ_Dataset.xlsx   # FAQ dataset (Question, Answer, Category)
├── ui/
│   └── app.py                   # Streamlit web interface
├── .streamlit/
│   └── config.toml              # Dark theme configuration
├── main.py                      # Command-line entry point
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/safex-faq-chatbot.git
cd safex-faq-chatbot

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt
```

## Running the Chatbot

**Command line:**
```bash
python main.py
```

**Web interface (Streamlit):**
```bash
streamlit run ui/app.py
```

## How It Works

1. The FAQ dataset (`data/SafeX_FAQ_Dataset.xlsx`) contains real questions and
   answers sourced directly from SafeX Solutions' website, organized by category.
2. Each FAQ question is converted into a **TF-IDF vector** (a numeric
   representation of text based on word importance).
3. When a user asks a question, it's converted into a vector the same way, and
   compared against every FAQ question using **cosine similarity**.
4. The closest matching FAQ's answer is returned, along with a confidence score.
5. If no match is confident enough (below a 0.25 threshold), the bot admits it
   isn't sure rather than guessing, and points the user to SafeX's real contact info.

## Dataset

The dataset contains **107 question variations** mapped to **30 unique, verified
answers** across 6 categories:

| Category | Description |
|---|---|
| About | Company background, mission, social impact |
| Services | Web dev, cybersecurity, marketing, creative media, consulting |
| Products | URL2Video.online, Skill Development Centre, SafeX Trust |
| Contact | Emails, phone numbers, business hours |
| Careers | Internships, job placement, application process |
| FAQ | Meta-questions about the site itself |

Multiple phrasings per answer were included deliberately — testing showed a
single phrasing per answer sometimes failed to match reworded user questions
(e.g. *"Do you build websites?"* vs. *"Does SafeX provide web development
services?"*).

## Results

Tested against 13+ sample queries covering exact matches, paraphrased
questions, and out-of-scope questions:

- ✅ Exact and reworded questions matched correctly in the large majority of cases
- ✅ Out-of-scope questions (e.g. "What's the weather today?") were correctly declined instead of guessing
- ⚠️ A few edge cases were found and documented (e.g. single-word brand names like "safexsolutions" without a space), which directly informed the paraphrase-expansion fix in the dataset

Full test results and validation notes are documented in the accompanying
portfolio case study.

## Notes & Limitations

- This is a **retrieval-based system**, not a generative AI model — it selects
  the best pre-written answer rather than generating new text.
- Data was sourced from safexsolutions.com and its subdomains (Skill
  Development Centre, Trust) as of July 2026, and from SafeX's own product,
  URL2Video.online.
- TF-IDF matching relies on shared keywords, so completely novel phrasings
  with no overlapping words may not match — a known trade-off of this
  lightweight approach versus a larger embedding-based model.

---

*Built as part of the SafeX Solutions Skill Development Centre internship program.*
