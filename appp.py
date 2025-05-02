"""
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


"""

import streamlit as st
import requests
from streamlit_option_menu import option_menu
from streamlit_extras.metric_cards import style_metric_cards
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

# Page configuration
st.set_page_config(page_title="Mental Health Predictor", page_icon="🧠", layout="centered")

# Sidebar navigation menu
with st.sidebar:
    selected = option_menu(
        menu_title="Menu",
        options=["Home", "Predict", "Clustering", "About", "Research"],
        icons=["house", "activity", "scatter-chart", "info-circle", "book"],
        menu_icon="cast",
        default_index=0,
    )

# Home Page
if selected == "Home":
    st.title("🧠 Mental Health Predictor")
    st.subheader("Track and assess your mental wellness with PHQ-9 & GAD-7.")
    st.markdown("### Features:")
    st.markdown("- ✅ Predict using PHQ-9 and GAD-7")
    st.markdown("- 📊 K-Means Clustering to group user patterns")
    st.markdown("- ⛑️ Validates input completeness")
    st.markdown("- 🚀 Designed for CI/CD deployment")
    st.markdown("- 🧠 Includes research-based explanations")

# Prediction Page
elif selected == "Predict":
    st.header("📊 Mental Health Assessment")

    st.subheader("PHQ-9 (Depression Screening)")
    phq9_questions = [
        "Little interest or pleasure in doing things",
        "Feeling down, depressed, or hopeless",
        "Trouble falling/staying asleep, or sleeping too much",
        "Feeling tired or having little energy",
        "Poor appetite or overeating",
        "Feeling bad about yourself – or that you are a failure",
        "Trouble concentrating on things",
        "Moving or speaking so slowly that others notice",
        "Thoughts of self-harm or suicide"
    ]

    phq9 = []
    for i, question in enumerate(phq9_questions):
        score = st.slider(f"PHQ-9 Q{i+1}: {question}", 0, 3, 1,
                          format="%d (0: Not at all, 3: Nearly every day)")
        phq9.append(score)

    st.subheader("GAD-7 (Anxiety Screening)")
    gad7_questions = [
        "Feeling nervous, anxious, or on edge",
        "Not being able to stop or control worrying",
        "Worrying too much about different things",
        "Trouble relaxing",
        "Being so restless it’s hard to sit still",
        "Becoming easily annoyed or irritable",
        "Feeling afraid as if something awful might happen"
    ]

    gad7 = []
    for i, question in enumerate(gad7_questions):
        score = st.slider(f"GAD-7 Q{i+1}: {question}", 0, 3, 1,
                          format="%d (0: Not at all, 3: Nearly every day)")
        gad7.append(score)

    if st.button("🔍 Predict Mental Health"):
        if len(phq9) < 9 or len(gad7) < 7:
            st.warning("⚠️ Please complete all questions before submitting.")
        else:
            API_URL = "http://127.0.0.1:8000/predict"

            payload = {"phq9": phq9, "gad7": gad7}

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

# Clustering Page
elif selected == "Clustering":
    st.header("📊 User Pattern Clustering (K-Means)")

    # Generate synthetic data or load past user data
    num_users = 200
    data = {
        'phq9_scores': [np.random.randint(0, 4, 9).tolist() for _ in range(num_users)],
        'gad7_scores': [np.random.randint(0, 4, 7).tolist() for _ in range(num_users)],
    }
    df = pd.DataFrame(data)
    df['all_scores'] = df['phq9_scores'] + df['gad7_scores']
    score_matrix = pd.DataFrame(df['all_scores'].tolist())

    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(score_matrix)

    df['Cluster'] = clusters
    st.write("🧩 User groups based on response patterns:")
    st.dataframe(df[['phq9_scores', 'gad7_scores', 'Cluster']].head(10))

# About Page
elif selected == "About":
    st.title("ℹ️ About This App")
    st.write("""
    This app uses machine learning to help assess mental health status via standardized questionnaires:
    
    - **PHQ-9**: Screens for depression
    - **GAD-7**: Screens for anxiety

    🚀 Built using:
    - Streamlit (Frontend)
    - FastAPI (Backend)
    - Scikit-learn (ML models)
    - Joblib (Model persistence)

    _Disclaimer: This is not a diagnostic tool. Always consult a professional._  
    """)

# Research Page
elif selected == "Research":
    st.title("📚 Responsible Mental Health Analysis")
    st.markdown("""
    **Mental health AI tools must follow ethical principles:**
    
    - Data is anonymized and synthetic where possible.
    - Results are intended to raise awareness, not replace clinical advice.
    - PHQ-9 and GAD-7 are evidence-based and widely used.
    - Predictions are paired with actionable suggestions (e.g., “seek counseling”).
    - CI/CD pipelines ensure rapid updates and bug fixes.

    **Sources:**
    - [PHQ-9 Research](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1495268/)
    - [GAD-7 Research](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1854882/)
    """)

# Style
style_metric_cards()
