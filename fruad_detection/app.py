import streamlit as st
import pandas as pd
import joblib

# Set light theme explicitly
st.set_page_config(
    page_title="Credit Card Fraud Detection",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------- Background image setup --------
def set_bg(url):
    st.markdown(
        f"""
        <style>
        html, body, [class*="stApp"] {{
            background-image: url("{url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: black;
        }}
        .main-container {{
            background-color: rgba(255, 255, 255, 0.94);
            padding: 2rem;
            border-radius: 15px;
            max-width: 750px;
            margin: 3rem auto;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set background image
background_url = "https://images.unsplash.com/photo-1605902711622-cfb43c4437d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80"
set_bg(background_url)

# -------- Load ML models --------
model_dir = "fruad_detection"

try:
    models = {
        "Support Vector Machine": joblib.load(f"{model_dir}/svm.pkl"),
        "Logistic Regression": joblib.load(f"{model_dir}/logistic_model_b.pkl")
    }
except FileNotFoundError as e:
    st.error(f"❌ Missing model files: {e}")
    st.stop()

# -------- UI --------
st.markdown("<div class='main-container'>", unsafe_allow_html=True)
st.title("💳 Credit Card Fraud Detection")
st.markdown("Select a model and input transaction features to detect fraud:")

# Model selection
model_choice = st.selectbox("🔍 Choose a Model", list(models.keys()))

# Input fields
st.subheader("🧾 Transaction Input (30 Features)")
input_features = {}
input_features["Time"] = st.number_input("Time", 0.0, 200000.0, 10000.0)

for i in range(1, 29):
    input_features[f"V{i}"] = st.number_input(f"V{i}", -100.0, 100.0, 0.0)

input_features["Amount"] = st.number_input("Amount ($)", 0.0, 100000.0, 100.0)

# Prediction
if st.button("🧠 Predict"):
    input_df = pd.DataFrame([input_features])
    model = models[model_choice]
    prediction = model.predict(input_df)[0]
    result = "⚠️ Fraudulent Transaction!" if prediction == 1 else "✅ Legitimate Transaction."
    
    st.subheader("📊 Prediction Result")
    st.success(result) if prediction == 0 else st.error(result)

st.markdown("</div>", unsafe_allow_html=True)
