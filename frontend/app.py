import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Logistics Dashboard", layout="wide")

# =====================
# LOGIN CHECK
# =====================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.post("http://127.0.0.1:5000/login", json={
            "username": username,
            "password": password
        }).json()

        if res["status"] == "success":
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error("Invalid credentials")

else:
    st.title("📦 AI Logistics Intelligence Dashboard")

    # =====================
    # INPUTS
    # =====================
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        orders = st.slider("Orders", 50, 500, 200)
    with col2:
        workers = st.slider("Workers", 5, 50, 15)
    with col3:
        safety = st.slider("Safety (0-5)", 0, 5, 3)
    with col4:
        productivity = st.slider("Productivity", 40, 100, 70)

    # =====================
    # KPI CARDS
    # =====================
    k1, k2, k3, k4 = st.columns(4)

    k1.metric("Orders", orders)
    k2.metric("Workers", workers)
    k3.metric("Safety", safety)
    k4.metric("Productivity", productivity)

    # =====================
    # PREDICT
    # =====================
    if st.button("🚀 Run Analysis"):
        res = requests.post("http://127.0.0.1:5000/predict", json={
            "orders": orders,
            "workers": workers,
            "safety": safety,
            "productivity": productivity
        }).json()

        if res["prediction"] == 1:
            st.error("🚨 Delay Risk Detected")

            # SMART INSIGHTS
            if orders / workers > 25:
                st.warning("⚠️ High workload per worker")

            if safety <= 2:
                st.warning("⚠️ Low safety compliance")

            if productivity < 60:
                st.warning("📉 Productivity drop detected")

            st.info("💡 Recommendation: Increase workers or optimize process")

        else:
            st.success("✅ Operations Stable")

    # =====================
    # CHART + DATA
    # =====================
    st.subheader("📊 Historical Data")

    logs = requests.get("http://127.0.0.1:5000/logs").json()
    df = pd.DataFrame(logs)

    if not df.empty:
        st.dataframe(df)

        st.line_chart(df[["orders", "workers", "productivity"]])