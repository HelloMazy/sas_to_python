# app/ui.py
import streamlit as st
from app.converter import convert_sas_to_python

def run_ui():
    st.set_page_config(page_title="SAS → Python Converter", layout="wide")
    st.title("🧠 SAS → Python Converter")

    sas_code = st.text_area("Colle ici ton code SAS", height=300)

    if st.button("Convertir en Python"):
        result = convert_sas_to_python(sas_code)
        st.subheader("💡 Code Python généré :")
        st.code(result or "# Aucun code reconnu pour l’instant", language="python")
