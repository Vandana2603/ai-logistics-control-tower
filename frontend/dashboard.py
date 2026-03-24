import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

def dashboard():
    st.title("🚀 AI Logistics Dashboard")

    st.subheader("📊 Input Data")

    orders = st.slider("Orders", 50, 500, 200)
    workers = st.slider("Workers", 5, 50, 20)
    safety = st.slider("Safety Risk (0-5)", 0, 5, 2)
    productivity = st.slider("Productivity (%)", 60, 100, 80)

    if st.button("Analyze"):
        try:
            res = requests.post(
                "http://127.0.0.1:5000/predict",
                json={
                    "orders": orders,
                    "workers": workers,
                    "safety": safety,
                    "productivity": productivity
                }
            )

            result = res.json()

            st.success(f"Prediction: {result['prediction']}")
            st.warning(f"Alert: {result['alert']}")

        except:
            st.error("Backend not running!")

    st.subheader("📈 Logs")

    try:
        data = requests.get("http://127.0.0.1:5000/logs").json()
        df = pd.DataFrame(data)

        if not df.empty:
            st.dataframe(df)

            fig, ax = plt.subplots()
            ax.plot(df["orders"])
            ax.set_title("Orders Trend")
            st.pyplot(fig)

    except:
        st.error("Cannot load logs")