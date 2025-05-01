import streamlit as st
import requests
from streamlit_option_menu import option_menu
from streamlit_extras.metric_cards import style_metric_cards

# Page configuration
st.set_page_config(page_title="Mental Health Predictor", page_icon="🧠", layout="centered")

# Sidebar navigation menu
with st.sidebar:
    selected = option_menu(
        menu_title="Menu",
        options=["Home", "Predict", "About"],
        icons=["house", "activity", "info-circle"],
        menu_icon="cast",
        default_index=0,
    )

# Home Page
if selected == "Home":
    st.title("🧠 Mental Health Predictor")
    st.subheader("Track and assess your mental wellness with PHQ-9 & GAD-7.")
    st.markdown("### Features:")
    st.markdown("- ✅ Predict using PHQ-9 and GAD-7")
    st.markdown("- 🎨 Engaging and animated interface")
    st.markdown("- 📈 Real-time score summary")

# Prediction Page
elif selected == "Predict":
    st.header("📊 Answer the following questions:")

    st.subheader("PHQ-9 (Depression)")
    phq9 = []
    for i in range(1, 10):
        score = st.slider(f"Q{i}. In the last 2 weeks, how often were you bothered by: ...", 0, 3, 1,
                          format="%d (0: Not at all, 3: Nearly every day)")
        phq9.append(score)

    st.subheader("GAD-7 (Anxiety)")
    gad7 = []
    for i in range(1, 8):
        score = st.slider(f"Q{i}. In the last 2 weeks, how often did you feel: ...", 0, 3, 1,
                          format="%d (0: Not at all, 3: Nearly every day)")
        gad7.append(score)

    if st.button("🔍 Predict Mental Health"):
        API_URL = "http://127.0.0.1:8000/predict"  # Replace with your deployed API URL if hosted

        payload = {
            "phq9": phq9,
            "gad7": gad7
        }

        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                result = response.json()
                st.success(f"Total Score: `{result['total_score']}`")
                st.info(f"Predicted Level: **{result['level']}**")
                st.warning(f"Recommendation: {result['recommendation']}")
            else:
                st.error("Prediction failed. Please try again.")
        except Exception as e:
            st.error(f"API call error: {e}")

# About Page
elif selected == "About":
    st.title("ℹ️ About This App")
    st.write("""
    This app helps assess mental health levels based on standardized questionnaires: PHQ-9 and GAD-7.

    - **PHQ-9** measures depression severity  
    - **GAD-7** measures anxiety severity  

    Built using:
    - 🧠 Streamlit
    - 💡 Python
    - 🚀 FastAPI backend
    - ✨ Lottie Animations (optional)

    _This is not a clinical diagnostic tool. Please consult a professional if needed._
    """)

# Style metrics
style_metric_cards()

