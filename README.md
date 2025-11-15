# 🔬 Segmentación por Estado Mental — Análisis y Modelo (Suicide Rates CSV)

**Resumen breve**  
Este repositorio contiene el código y los artefactos para realizar una **segmentación (clustering)** sobre el dataset `crude suicide rates.csv`.  
**Objetivo:** dividir la población en **n clusters** de atención según indicadores de salud (vulnerabilidad / riesgo), calcular las métricas de evaluación (inercia y silhouette) y entregar **un informe por cluster** que permita a un profesional de salud entender por qué cada cluster presenta ese comportamiento. Además incluye una **interfaz web (Gradio)** para consumir el modelo.

> Nota técnica: para evitar *data leakage*, las columnas de **tasas de suicidio** se **excluyeron** como features del clustering y se usan únicamente en el análisis descriptivo por cluster (es decir: las usamos para *interpretar* los grupos, no para crearlos).

---

## 🧾 Dataset (columnas relevantes)
El CSV original contiene, entre otras, las siguientes columnas detectadas:

- `Unnamed: 1` — (Year / etiqueta de año en este CSV)  
- `Probability (%) of dying between age 30 and exact age 70...ular disease, cancer, diabetes, or chronic respiratory disease`  
- `Probability (%) of dying between age 30 and exact age 70...ar disease, cancer, diabetes, or chronic respiratory disease.1`  
- `Probability (%) of dying between age 30 and exact age 70...ar disease, cancer, diabetes, or chronic respiratory disease.2`  
- `Crude suicide rates (per 100 000 population)`  
- `Crude suicide rates (per 100 000 population).1`  
- `Crude suicide rates (per 100 000 population).2`

> En el notebook se usaron las **3 columnas de probabilidad de muerte (las tres columnas "Probability (%) ...")** como features de clustering, y las columnas `Crude suicide rates (...)` se reservaron para análisis por cluster.

---

## 📌 Qué hace el proyecto (pasos reproducibles)
1. **Carga & limpieza** del CSV (conversión a numérico, eliminación de filas/cols inválidas).  
2. **Selección de features**: usamos las 3 columnas `Probability (%) ...` para clustering (evitando las columnas de suicide rate como features).  
3. **Normalización** con `StandardScaler`.  
4. **Búsqueda del mejor k** en un rango (p. ej. 2–10):
   - Calcula **inercia** (KMeans.inertia_) por cada k (Elbow method).  
   - Calcula **Silhouette score** por cada k (scikit-learn).  
   - Opcional: visualización con **Yellowbrick** (`KElbowVisualizer`, `silhouette_visualizer`) si está disponible.  
5. **Selecciona k** (por mayor silhouette o por elbow) y entrena `KMeans(n_clusters=k)`.  
6. **Genera resumen por cluster**:
   - Tamaño (n) y proporción.  
   - Medias de las features (probabilidades de muerte).  
   - Medias de las tasas de suicidio (las columnas `Crude suicide rates...`) dentro de cada cluster — para interpretación clínica.  
   - Top features que más se desvían del promedio global (para justificar por qué un cluster es de riesgo mayor/menor).  
7. **Visualizaciones**: Elbow plot, Silhouette plot, PCA 2D con clusters coloreados, heatmap de medias por cluster.  
8. **Exporta**: `kmeans` + `scaler` serializados (`joblib`) y un `analysis_report.txt` con métricas (inercia, silhouette) y resumen por cluster.  
9. **Interfaz Gradio**: app que acepta un nuevo registro (valores de las columnas de features) y devuelve cluster asignado y texto interpretativo para el médico.

---

## 🩺 Interpretación para el médico (qué incluye el informe por cluster)
Para cada cluster el notebook produce un bloque que contiene:

- **Descripción del cluster** (cantidad de casos, % del dataset).  
- **Por qué el cluster tiene ese comportamiento**: lista de las features (probabilidades de morir) que se desvían más del promedio global y la dirección (mayor/menor).  
- **Estadísticas de tasas de suicidio** dentro del cluster (promedio por las columnas `Crude suicide rates (...)`) — esto permite responder preguntas como:
  - *¿Este cluster muestra mayor probabilidad de suicidio?*  
  - *¿Este cluster muestra mayor probabilidad de morir prematuramente entre 30 y 70 años?*  

---

## 💻 Interfaz y consumo del modelo
- Interfaz Gradio incluida: recibe los **valores de las 3 features** (las 3 columnas `Probability (%) ...`) y devuelve:
  - Cluster asignado (entero).  
  - Texto resumen/interpretación para el médico (generado a partir del `cluster_summaries`).


