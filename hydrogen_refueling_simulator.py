import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Hydrogen Refueling Simulator V2", layout="wide")
st.title("🚛 Hydrogen Refueling Station Simulator – V2 (Full Version)")

# User Inputs
st.sidebar.header("🔧 Configuration")
vehicles_per_hour = st.sidebar.number_input("Vehicles per hour", 1, 200, 10)
vehicle_volume_l = st.sidebar.number_input("Vehicle tank size [liters @ 1 bar]", 100, 2000, 150)
start_pressure = st.sidebar.number_input("Start pressure [bar]", 0, 300, 50)
target_pressure = st.sidebar.selectbox("Target pressure", [350, 700], index=1)
nozzles = st.sidebar.slider("Number of nozzles", 1, 10, 2)
ambient_temp = st.sidebar.slider("Ambient temperature (°C)", -10, 50, 20)

# Constants
flow_per_nozzle_kg_min = 3.6
h2_density = 0.08988
vehicle_volume_nm3 = vehicle_volume_l / 1000
delta_p = target_pressure - start_pressure
h2_per_vehicle = delta_p * vehicle_volume_nm3 * h2_density
h2_total_hour = h2_per_vehicle * vehicles_per_hour
total_flow_kg_min = flow_per_nozzle_kg_min * nozzles

cp_h2 = 14.3
delta_T = ambient_temp + 40
cooling_kw = (total_flow_kg_min / 60) * cp_h2 * delta_T / 1000

comp_start_delay = 15
comp_flow = 800
comp_effective = comp_flow * ((60 - comp_start_delay) / 60)
compressors_needed = int(np.ceil(h2_total_hour / comp_effective))

buffer_total = h2_total_hour * 1.2
lp_vol = buffer_total * 0.5
mp_vol = buffer_total * 0.3
hp_vol = buffer_total * 0.2

# Output Results
st.subheader("📊 Sizing Results")
st.markdown(f"- **Hydrogen per vehicle**: `{h2_per_vehicle:.2f} kg`")
st.markdown(f"- **Total demand**: `{h2_total_hour:.1f} kg/h`")
st.markdown(f"- **Cooling power required**: `{cooling_kw:.1f} kW`")
st.markdown(f"- **Compressors required (800 kg/h each, 15 min delay)**: `{compressors_needed}`")
st.markdown(f"- **Buffer sizing**: LP = `{lp_vol:.1f} kg`, MP = `{mp_vol:.1f} kg`, HP = `{hp_vol:.1f} kg`")

# Animation (simulated fill progress)
st.subheader("🧊 3D-style Buffer Animation (Simplified)")
fill_percent = st.slider("Simulated buffer fill progress", 0, 100, 30)
lp_fill = min(fill_percent, 50) * 2
mp_fill = max(min(fill_percent - 50, 30), 0) * (100/30)
hp_fill = max(fill_percent - 80, 0) * (100/20)

st.progress(int(lp_fill), "Low Pressure Bank (LP)")
st.progress(int(mp_fill), "Mid Pressure Bank (MP)")
st.progress(int(hp_fill), "High Pressure Bank (HP)")

# Pressure curve
st.subheader("📈 Vehicle Pressure Rise During Filling")
t = np.linspace(0, 5, 100)
p = start_pressure + (target_pressure - start_pressure)*(1 - np.exp(-t / 1.5))
fig, ax = plt.subplots()
ax.plot(t, p)
ax.set_xlabel("Time (min)")
ax.set_ylabel("Pressure (bar)")
ax.set_title("Pressure Curve During Filling")
st.pyplot(fig)
