import streamlit as st
from HireMind import HireMind

# ---------------- Configuration ---------------- #
CONFIG = {
    'page_title': "HireMind",
    'page_icon': '🧠',
    'page_layout': 'wide',
    'groq_model': 'llama-3.3-70b-versatile',
    'openai_model': 'gpt-4o-mini',
    'radio_opt': ['GROQ', 'OpenAI']
}

st.set_page_config(page_title=CONFIG['page_title'], page_icon=CONFIG['page_icon'], layout=CONFIG['page_layout'])

# ---------------- Sidebar ---------------- #
st.sidebar.title("🔧 Settings")
selected_opt = st.sidebar.radio("Choose the LLM provider", CONFIG['radio_opt'])
api_key = st.sidebar.text_input(f"Enter your {selected_opt} API Key", type="password")
model_name = CONFIG['openai_model'] if selected_opt == "OpenAI" else CONFIG['groq_model']
st.sidebar.text_input("Model", value=model_name, disabled=True)

uploaded_resume = st.sidebar.file_uploader("Upload Resume (PDF, DOCX)", type=["pdf", "docx"])
jd_text = st.sidebar.text_area("Paste the Job Description here")

# ---------------- Model Caching ---------------- #
@st.cache_resource(show_spinner="⏳ Loading model...")
def get_model(api_key: str, model_name: str, is_openai: bool):
    core = HireMind()
    core.load_model(model_name=model_name, api_key=api_key, openai=is_openai)
    core.test_model()
    return core

# ---------------- Main Logic ---------------- #
if api_key and uploaded_resume and jd_text.strip():
    try:
        core = get_model(api_key, model_name, selected_opt == "OpenAI")

        with st.spinner("🧠 Analyzing resume..."):
            resume_data = core.read_resume(uploaded_resume)
            analysis = core.analyse_resume(resume_data, jd_text)

        # ---------------- Layout Columns ---------------- #
        col1, col2 = st.columns(2)

        # ----- Resume Section ----- #
        with col1:
            st.markdown("## 📄 Extracted Resume")
            st.subheader("🧑‍💼 Summary")
            st.write(resume_data.get('summary', 'Not provided'))

            st.subheader("📊 Experience")
            st.write(f"{resume_data.get('experience', 0)} years")

            st.subheader("🛠️ Skills")
            for category, items in resume_data.get('skills', {}).items():
                st.markdown(f"**{category.replace('_', ' ').title()}**: {', '.join(items)}")

        # ----- AI Analysis Section ----- #
        with col2:
            st.markdown("## 🤖 AI Analysis vs JD")
            st.subheader("💬 Review")
            st.write(analysis.get('review', 'No review provided'))

            st.subheader("📈 Fit Score (out of 10)")
            score = analysis.get('candidate_fit_score', 0)
            st.markdown(
                f"""
                <div style="width: 160px; height: 160px; border-radius: 80px; background: conic-gradient(#4caf50 {score * 36}deg, #ddd {score * 36}deg); display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold;">
                    {score}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.subheader("✅ Final Decision")
            final_decision = analysis.get('final_decision', '')
            if final_decision == 'R':
                st.markdown(
                    "<div style='background-color:#f44336;color:white;padding:10px 20px;border-radius:10px;display:inline-block;font-weight:bold;'>Rejected</div>",
                    unsafe_allow_html=True
                )
            elif final_decision == 'A':
                st.markdown(
                    "<div style='background-color:#4caf50;color:white;padding:10px 20px;border-radius:10px;display:inline-block;font-weight:bold;'>Accepted</div>",
                    unsafe_allow_html=True
                )

    except Exception as e:
        st.error("🚨 Something went wrong during model analysis.")
        with st.expander("Click to view full error"):
            st.exception(e)
