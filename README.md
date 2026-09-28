# EduGenie: Google Gemini Powered Learning Assistant 🧠✨

EduGenie is a lightweight AI-powered educational assistant that simplifies learning through generative AI. Designed for students of all academic levels, EduGenie enables users to:
- **Ask questions and receive smart, concise answers** (`/qa` endpoint)
- **Understand complex concepts through simplified explanations** (`/explain/` endpoint)
- **Generate interactive quizzes from topics or text** (`/quiz` endpoint)
- **Summarize large educational passages** (`/summarize/` endpoint)
- **Receive personalized, structured learning recommendations** (`/learn/recommendations` endpoint)

Built with **FastAPI** for the backend and a modern, responsive **HTML + CSS + JavaScript** frontend, EduGenie leverages both cloud-based AI models (**Google Gemini 1.5 Pro**) and local models (**LaMini-Flan-T5-783M**) for local efficiency and cloud power.

---

## 🏗️ Architecture & Model Selection

```
                         Start (User opens EduGenie)
                                     │
                                     ▼
                            Frontend: User Input
                                     │
                                     ▼
         FastAPI Backend: Route to the respective endpoint based on selection
           │                 │               │               │                │
           ▼                 ▼               ▼               ▼                ▼
   Explanation Module   Q&A Module    Quiz Generation   Summarization   Learning Path Module
    (/explain endpoint) (/qa endpoint) (/quiz endpoint) (/summarize)    (/learn/recommendations)
           │                 │               │               │                │
           └─────────────────┴───────┬───────┴───────────────┴────────────────┘
                                     │
                                     ▼
                          Frontend: Display Results
                                     │
                                     ▼
                       End (User interacts again)
```

### Models Used
- **Google Gemini 1.5 Pro** (Cloud API):
  - Used for: Q&A, Summarization, Quiz Generation, and Learning Path Recommendations.
  - Benefits: Advanced reasoning, structured JSON outputs, fast cloud inference.
- **LaMini-Flan-T5-783M** (Local HuggingFace Seq2Seq LM):
  - Used for: Concept Explanations.
  - Benefits: Instruction-tuned, lightweight, CPU-compatible, simplified educational tone.
  - *Includes seamless automatic fallback to Gemini 1.5 Pro if local weights are not pre-downloaded.*

---

## 📁 Folder Structure

```
EduGenie/
├── static/
│   └── style.css            # Custom CSS styling (responsive, card layouts, quiz styles)
├── templates/
│   └── index.html           # Frontend web interface & interactive JS logic
├── explanation_module.py    # Local LaMini-Flan-T5 model + Gemini fallback logic
├── learning_path.py         # Gemini-driven personalized learning path generator
├── main.py                  # FastAPI server, REST API endpoints, CORS, static routes
├── qna.py                   # Gemini Q&A answering module
├── quiz_module.py           # Gemini 3-question MCQ generator with JSON parser
├── summary_module.py        # Gemini passage summarization logic
├── requirements.txt         # Python project dependencies
├── .env                     # Local environment file for GEMINI_API_KEY
├── .env.example             # Template for environment configuration
└── README.md                # Setup, installation, running, and testing guide
```

---

## ⚙️ Pre-requisites

1. **Python 3.10+** (Tested on Python 3.10, 3.11, and 3.12)
2. **VS Code** (Visual Studio Code)
3. **Google Gemini API Key**:
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Sign in with your Google account.
   - Click **Get API key** -> **Create API key**.
   - Copy your API key.

---

## 🚀 Setup & Installation in VS Code

### Step 1: Open the Project in VS Code
1. Launch **Visual Studio Code**.
2. Go to **File** > **Open Folder...** and select the `Edu gene` folder.
3. Open an integrated terminal in VS Code:
   - Press `` Ctrl + ` `` (backtick) or select **Terminal** > **New Terminal**.

### Step 2: (Recommended) Create and Activate a Virtual Environment
In the VS Code terminal:

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(If you encounter an execution policy prompt, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first)*

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies
Install the required packages using `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Step 4: Configure Your Gemini API Key
1. Open the `.env` file in the root directory.
2. Add your Gemini API key:
   ```env
   GEMINI_API_KEY=AIzaSy...your_actual_api_key_here
   ```
3. Save the file (`Ctrl + S`).

---

## 🏃 Running the Application

### Option A: Using Uvicorn with auto-reload (Recommended)
In the terminal, run:
```bash
uvicorn main:app --reload
```

### Option B: Running directly with Python
```bash
python main.py
```

You should see output similar to:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [...]
INFO:     Started server process [...]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Now open your web browser and navigate to:
👉 **`http://127.0.0.1:8000`**

---

## 🧪 Functional Testing Guide

Once the web page loads at `http://127.0.0.1:8000`, test each feature:

### 1. Ask a Question (Q&A Module)
- **Input:** `Which is the largest ocean?`
- Click: **Get Answer**
- **Expected Result:** A white card appears with `Answer:` stating that the Pacific Ocean is the largest ocean on Earth.

### 2. Need an Explanation? (Explanation Module)
- **Input:** `quantum computing` or `Binary Search Algorithm`
- Click: **Explain**
- **Expected Result:** A simplified explanation suitable for students appears in clean monospace text.

### 3. Summarize a Paragraph (Summarization Module)
- **Input:**
  > The Industrial Revolution, which began in the late 18th century, marked a major turning point in history. It shifted economies from agriculture and manual labor to machine-driven manufacturing. While it boosted economies, it also created social and environmental challenges.
- Click: **Summarize**
- **Expected Result:** A concise, easy-to-understand summary retaining the core concepts.

### 4. Generate a Quiz (Quiz Generation Module)
- **Input:** `Pythagoras theorem` or `Solar System`
- Click: **Generate Quiz**
- **Expected Result:**
  - 3 multiple-choice questions are generated, each with 4 distinct options.
  - Select an answer for a question and click **Check Answer**.
  - If correct, displays `✅ Correct!`.
  - If incorrect, displays `❌ Incorrect. Correct answer: ...`.

### 5. Get Learning Recommendations (Learning Path Module)
- **Input:** `SQL` or `Linear Regression`
- Click: **Get Recommendations**
- **Expected Result:** A structured roadmap divided into Beginner, Intermediate, and Advanced stages with topics, time estimates, and recommended study resources.

---

## 📡 REST API Documentation

EduGenie also exposes interactive Swagger API documentation.
With the server running, visit:
👉 **`http://127.0.0.1:8000/docs`**

| Method | Endpoint | Description | Sample Query / Payload |
|---|---|---|---|
| `GET` | `/` | Web frontend UI | None |
| `GET` | `/qa` | Ask general question | `?question=Why+is+the+sky+blue%3F` |
| `POST` | `/explain/` | Explain a concept | `{"topic": "Photosynthesis"}` |
| `POST` | `/summarize/` | Summarize long text | `{"text": "Long passage..."}` |
| `POST` | `/quiz` | Generate 3 MCQs | `{"text": "Solar System"}` |
| `GET` | `/learn/recommendations` | Learning path recommendations | `?topic=Python` |

---

## 🛠️ Troubleshooting

- **Error: "⚠️ GEMINI_API_KEY is not set"**:
  Make sure your `.env` file has `GEMINI_API_KEY=your_key` without quotes and is located in the same directory where you run `uvicorn`.
- **First-time Explanation Generation**:
  If using the local `MBZUAI/LaMini-Flan-T5-783M` model, it may download model weights on initial run. If memory or internet is constrained, EduGenie automatically falls back to Gemini 1.5 Pro to ensure seamless operation.
- **Port Conflict (Port 8000 already in use)**:
  Run on a different port:
  ```bash
  uvicorn main:app --reload --port 8080
  ```
