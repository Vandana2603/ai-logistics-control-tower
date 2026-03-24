import streamlit as st
import requests

def login_page():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.post("http://127.0.0.1:5000/login", json={
            "username": username,
            "password": password
        })

        result = res.json()

        if result["status"] == "success":
            st.session_state["logged_in"] = True
            st.session_state["role"] = result["role"]

            st.success("Login successful ✅")

            # 🔥 THIS LINE FIXES YOUR ISSUE
            st.rerun()

        else:
            st.error("Invalid credentials")