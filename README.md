# LangGraph AI Chatbot

An AI-powered conversational chatbot built with **LangGraph**, **Streamlit**, and **Groq** (`llama-3.1-8b-instant`). It includes stateful memory and persistence across conversational turns using LangGraph's checkpointer.

---

## Features

- **LangGraph State Management:** Uses a graph-based state workflow (`ChatState`) with `add_messages` reducer.
- **Short-term Memory & Persistence:** Stateful chat history powered by `InMemorySaver` checkpointer and unique session thread IDs.
- **Fast Inference:** Accelerated by Groq's LPU inference engine via `langchain-groq`.
- **Interactive UI:** Built with Streamlit's native `st.chat_message` and `st.chat_input` widgets.

---

## Project Structure

```text
├── chat_bot/
│   ├── main_frontend.py       # Streamlit UI application
│   └── langgraph_backend.py   # LangGraph backend workflow
├── requirements.txt           # Project dependencies
├── .env.example               # Template for environment variables
├── .gitignore                 # Files excluded from git tracking
└── README.md                  # Project documentation
```

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/shivampatra2027/Langgraph.git
cd Langgraph
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv myenv
.\myenv\Scripts\activate

# macOS / Linux
python3 -m venv myenv
source myenv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
Copy `.env.example` to `.env` and insert your Groq API key:
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
```

### 5. Run the Application
```bash
streamlit run chat_bot/main_frontend.py
```

---

## Deploying to Streamlit Community Cloud

1. Push this repository to GitHub.
2. Sign in to [share.streamlit.io](https://share.streamlit.io).
3. Click **New app** and select your repository:
   - **Repository:** `shivampatra2027/Langgraph`
   - **Branch:** `main`
   - **Main file path:** `chat_bot/main_frontend.py`
4. Go to **Advanced settings** ➔ **Secrets** and add:
   ```toml
   GROQ_API_KEY = "your_actual_groq_api_key"
   ```
5. Click **Deploy!**
