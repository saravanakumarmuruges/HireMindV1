# 🧠 AI Resume Filter

Upload a resume and job description, provide your OpenAI or Groq API key on the page, and get a match analysis using LLMs.

---

## Setup

```bash
git clone https://github.com/yourusername/ai-resume-filter.git
cd ai-resume-filter

python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows

pip install -r requirements.txt

streamlit run app.py
