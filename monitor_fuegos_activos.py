import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

# Configuración de la página
st.set_page_config(
    page_title="Monitor de Fuegos Activos - Sentinel",
    page_icon="🔥",
    layout="wide"
)

st.title("🔥 Monitor de Fuegos Activos (Sentinel 3 SLSTR)")
st.markdown("Datos simulados de puntos calientes detectados por satélite Sentinel-3 SLSTR.")

# Simular datos de fuegos activos
np.random.seed(42)
dates = pd.date_range("2024-04-15", periods=10, freq='D')
regions = ["Amazonas", "Cordillera", "Llanura", "Costa", "Selva"]
data = {
    "lat": np.random.uniform(-4, 13, size=50),
    "lon": np.random.uniform(-79, -68, size=50),
    "brightness": np.random.uniform(300, 500, size=50),
    "date": np.random.choice(dates, size=50),
    "region": np.random.choice(regions, size=50)
}
df = pd.DataFrame(data)

# Sidebar para filtros
st.sidebar.header("Filtros")
selected_region = st.sidebar.selectbox("Selecciona región", options=regions + ["Todas"])
start_date = st.sidebar.date_input("Fecha desde", value=dates.min())
end_date = st.sidebar.date_input("Fecha hasta", value=dates.max())

# Filtrar datos
if selected_region != "Todas":
    df = df[df["region"] == selected_region]
df = df[(df["date"] >= pd.to_datetime(start_date)) & (df["date"] <= pd.to_datetime(end_date))]

# Mapa interactivo con Folium
st.subheader("Mapa de Fuegos Activos")

if not df.empty:
    m = folium.Map(location=[df["lat"].mean(), df["lon"].mean()], zoom_start=6)

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=5,
            color="red",
            fill=True,
            fill_color="red",
            tooltip=f"Brillo: {row['brightness']:.2f}",
        ).add_to(m)

    st_folium(m, width=700, height=500)
else:
    st.warning("No hay datos para los filtros seleccionados.")

# Gráfico de fuegos por fecha
st.subheader("Evolución de Fuegos Activos por Fecha")
chart_data = df.groupby("date").size()
st.line_chart(chart_data)

# Tabla de datos
st.subheader("Datos de Fuegos Activos")
st.dataframe(df[["date", "lat", "lon", "brightness", "region"]])

# Pie de página
st.markdown("---")
st.caption("Datos simulados basados en observaciones de Sentinel-3 SLSTR. Actualizados diariamente.")
