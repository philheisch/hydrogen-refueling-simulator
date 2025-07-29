
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.set_page_config(page_title="Hydrogen Refueling Simulator", layout="wide")

st.title("🚀 Hydrogen Refueling Station Simulator")

st.markdown(
    '''
    This simulator helps you size and simulate hydrogen refueling stations at either **350 bar** or **700 bar**.
    It supports compression at **500 or 900 bar**, and uses SAE-like fill logic.
    '''
)

# Inputs
col1, col2 = st.columns(2)

with col1:
    fill_pressure = st.selectbox("Target Vehicle Fill Pressure", [350, 700], index=1)
    vehicle_count = st.number_input("Vehicles per hour", min_value=1, value=10)
    avg_tank_liters = st.number_input("Avg. Tank Volume per Vehicle [liters @1 bar]", min_value=1, value=150)
    avg_start_pressure = st.number_input("Avg. Start Pressure [bar]", min_value=0, max_value=fill_pressure-1, value=100)

with col2:
    compressor_pressure = st.selectbox("Compressor Output Pressure", [500, 900], index=1)
    compressor_flow = st.selectbox("Compressor Flow Rate [kg/h]", [25, 50], index=1)
    nozzle_flow = st.number_input("Nozzle Flow Rate [kg/min]", min_value=1, value=5)
    nozzle_count = st.number_input("Number of Nozzles", min_value=1, value=2)

# Calculation logic
st.subheader("📊 Results")

vehicle_h2_needed = (fill_pressure - avg_start_pressure) * avg_tank_liters * 0.0899 / 1000  # in kg
total_h2_per_hour = vehicle_h2_needed * vehicle_count
effective_nozzle_flow = nozzle_flow * nozzle_count * 60  # kg/h

compressor_needed = total_h2_per_hour / compressor_flow
nozzles_needed = total_h2_per_hour / effective_nozzle_flow

st.markdown(f'''
- **Hydrogen needed per vehicle**: {vehicle_h2_needed:.2f} kg  
- **Total hourly hydrogen need**: {total_h2_per_hour:.2f} kg  
- **Estimated compressors needed**: {compressor_needed:.2f} → **{int(np.ceil(compressor_needed))}**  
- **Estimated nozzles needed**: {nozzles_needed:.2f} → **{int(np.ceil(nozzles_needed))}**
''')

# Simulate filling time per vehicle
st.subheader("⏱ Fill Curve Simulation")

fill_times = []
pressures = np.linspace(avg_start_pressure, fill_pressure, 50)
for p in pressures:
    fill_times.append((p - avg_start_pressure) / (fill_pressure - avg_start_pressure) * (vehicle_h2_needed / nozzle_flow) * 60)

fig, ax = plt.subplots()
ax.plot(fill_times, pressures, label="Pressure during filling")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Vehicle Pressure (bar)")
ax.set_title("Hydrogen Fill Curve")
ax.grid(True)
st.pyplot(fig)
