import plotly.graph_objects as go
import streamlit as st
import json
import google.generativeai as genai
import requests  # Added for Ollama/API fallback
from rapidfuzz import process

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(
    page_title="AI Medicine Safety Advisory",
    page_icon="💊",
    layout="wide"
)

# Custom CSS for better spacing
st.markdown("""
    <style>
    .stAlert { margin-top: -10px; }
    .stSubheader { margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State for History
if "history" not in st.session_state:
    st.session_state.history = []

# ==========================
# DATA LOADING (FAIL-SAFE)
# ==========================
try:
    with open("medicines.json", "r", encoding="utf-8") as file:
        content = file.read().strip()
        if not content:
            st.error("🚨 'medicines.json' is empty!")
            medicines_data = []
        else:
            medicines_data = json.loads(content)
except FileNotFoundError:
    st.error("🚨 'medicines.json' not found in the directory.")
    medicines_data = []
except json.JSONDecodeError as e:
    st.error(f"🚨 JSON Formatting Error: {str(e)}")
    medicines_data = []

# ==========================
# DATABASES
# ==========================
symptom_database = {
    "fever": "Low", "headache": "Low", "cough": "Low", "cold": "Low",
    "dizziness": "Moderate", "vomiting": "Moderate", "fatigue": "Moderate",
    "chest pain": "High", "breathing difficulty": "High", 
    "shortness of breath": "High", "loss of consciousness": "High"
}

condition_map = {
    "fever": ["Viral Infection", "Flu"],
    "headache": ["Migraine", "Stress"],
    "cough": ["Cold", "Respiratory Infection"],
    "dizziness": ["Dehydration", "Blood Pressure Issue"],
    "chest pain": ["Cardiac Concern", "Respiratory Issue"],
    "shortness of breath": ["Asthma", "Respiratory Distress"]
}

medicine_lookup = {med["medicine_name"].lower(): med for med in medicines_data}
medicine_names = list(medicine_lookup.keys())

# ==========================
# GEMINI CONFIG
# ==========================
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        llm_model = genai.GenerativeModel("gemini-2.5-flash")
    except Exception as e:
        st.sidebar.error(f"Gemini Init Error: {e}")
        llm_model = None
else:
    st.sidebar.warning("GEMINI_API_KEY missing in secrets.toml")
    llm_model = None

# ==========================
# HELPER FUNCTIONS
# ==========================

def ollama_fallback(prompt):
    """Attempt to use local Ollama instance (Phi-3) if Gemini fails."""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3:mini",
                "prompt": prompt,
                "stream": False
            },
            timeout=20
        )
        result = response.json()
        return result["response"]
    except:
        return None

def generate_ai_insight(symptoms, meds, score, warnings):
    prompt = f"""
    You are an educational medicine safety assistant. 
    Explain why these symptoms and medicines result in a {score}/100 risk score.
    Symptoms: {symptoms}
    Medicines: {meds}
    Warnings: {warnings}
    Rules: Max 40 words. No diagnosis. Professional tone.
    """
    
    # Logic path if Gemini is not configured
    if not llm_model:
        local = ollama_fallback(prompt)
        if local:
            return local
        return f"Risk Score: {score}/100\nSymptoms and medicines were analyzed via rule engine. Review alerts below."

    # Logic path for Gemini with local fallback for Rate Limits
    try:
        response = llm_model.generate_content(prompt)
        return response.text
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:  # Rate limit hit
            local = ollama_fallback(prompt)
            if local:
                return f"⚠️ Gemini Quota Exceeded. Local Phi3 Insight: {local}"
        return f"AI Insight Error: {error_msg}"

def get_recommendation(score):
    if score >= 80:
        return "🚨 IMMEDIATE ACTION: Seek professional medical attention or emergency services.", "error"
    if score >= 40:
        return "⚠️ CAUTION: Monitor symptoms closely and consult a healthcare provider.", "warning"
    return "✅ LOW CONCERN: Continue monitoring and maintain hydration/rest.", "success"

# ==========================
# SIDEBAR (HISTORY)
# ==========================
with st.sidebar:
    st.header("📋 Analysis History")
    st.markdown("---")
    if not st.session_state.history:
        st.write("No previous analyses.")
    else:
        for item in reversed(st.session_state.history[-5:]):
            st.write(f"**Score:** {item['risk']}/100\n**Meds:** {', '.join(item['medicines'])}")
            st.markdown("---")

# ==========================
# MAIN UI
# ==========================
st.title("💊 AI Medicine Safety Advisory")
st.markdown("Combine hard medical data with AI insights safely.")

col1, col2 = st.columns(2)
with col1:
    sym_input = st.text_area("🩺 Symptoms", placeholder="fever, dizziness, headche")
with col2:
    med_input = st.text_area("💊 Medicines", placeholder="Paracetmol, Aspirin")

if st.button("🔍 Run Safety Analysis", use_container_width=True):
    # 1. CLEAN INPUTS
    raw_s = [s.strip().lower() for s in sym_input.split(",") if s.strip()]
    raw_m = [m.strip().lower() for m in med_input.split(",") if m.strip()]

    recognized_symptoms = []
    corrected_medicines = []
    medicine_corrections = []
    possible_conditions = set()
    interaction_warnings = []
    risk_points = 0

    # 2. PROCESS SYMPTOMS
    for s in raw_s:
        match = process.extractOne(s, symptom_database.keys())
        if match and match[1] >= 75:
            name = match[0]
            recognized_symptoms.append(name.title())
            possible_conditions.update(condition_map.get(name, ["General Malaise"]))
            risk_points += {"Low": 10, "Moderate": 35, "High": 80}.get(symptom_database[name], 0)

    # 3. PROCESS MEDICINES
    for m in raw_m:
        match = process.extractOne(m, medicine_names)
        if match and match[1] >= 85:
            corrected_medicines.append(match[0].title())
            if m != match[0].lower():
                medicine_corrections.append(f"{m} → {match[0].title()}")
        else:
            corrected_medicines.append(m.title())

    # 4. INTERACTION LOGIC
    for i, m1 in enumerate(corrected_medicines):
        for j, m2 in enumerate(corrected_medicines):
            if i >= j: continue
            med_data = medicine_lookup.get(m1.lower())
            if med_data and "interactions" in med_data:
                interact_dict = {k.lower(): v for k, v in med_data["interactions"].items()}
                if m2.lower() in interact_dict:
                    data = interact_dict[m2.lower()]
                    interaction_warnings.append(f"⚠️ {m1} + {m2}: {data['effect']} ({data['risk']} Risk)")
                    risk_points += {"Low": 10, "Moderate": 40, "High": 70, "Critical": 95}.get(data['risk'], 0)

    total_risk_score = min(risk_points, 100)

    # 5. SESSION UPDATE
    st.session_state.history.append({
        "symptoms": recognized_symptoms,
        "medicines": corrected_medicines,
        "risk": total_risk_score
    })

    # 6. OUTPUT DISPLAY
    st.divider()
    
    st.subheader("📊 Safety Risk Meter")
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=total_risk_score,
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "black"},
               'steps': [{'range': [0, 30], 'color': "green"},
                         {'range': [30, 70], 'color': "orange"},
                         {'range': [70, 100], 'color': "red"}]}
    ))
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Recognized Symptoms")
        st.write(", ".join(recognized_symptoms) if recognized_symptoms else "None")
        st.subheader("Possible Conditions")
        st.write(", ".join(possible_conditions) if possible_conditions else "Unknown")

    with c2:
        st.subheader("Corrected Medicines")
        st.write(", ".join(corrected_medicines))
        st.subheader("Interaction Alerts")
        if interaction_warnings:
            for w in interaction_warnings: st.warning(w)
        else:
            st.success("No interactions found.")

    st.subheader("🧠 AI Health Insight")
    with st.spinner("Consulting Safety Engine..."):
        insight = generate_ai_insight(recognized_symptoms, corrected_medicines, total_risk_score, interaction_warnings)
        st.info(insight)

    rec_text, rec_type = get_recommendation(total_risk_score)
    getattr(st, rec_type)(rec_text)

st.markdown("---")
st.caption("⚠️ Educational tool only. Not for medical diagnosis.")