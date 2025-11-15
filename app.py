
import gradio as gr
import numpy as np
import joblib

# Load the scaler and model
scaler = joblib.load("scaler.pkl")
kmeans_final = joblib.load("modelo_clusters.pkl")

def predict_cluster(year, suicide_rate):
    try:
        data = np.array([[float(year), float(suicide_rate)]])
        scaled = scaler.transform(data)
        pred = kmeans_final.predict(scaled)[0]
        return f"Pertenece al cluster: {pred}"
    except Exception as e:
        return f"Error: {e}"

interface = gr.Interface(
    fn=predict_cluster,
    inputs=[
        gr.Number(label="Año"),
        gr.Number(label="Tasa de suicidio (100k)"),
    ],
    outputs="text",
    title="Modelo de Segmentación de Salud Mental"
)

if __name__ == "__main__":
    interface.launch(share=True)
