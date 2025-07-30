import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Hydrogen Refueling Simulator", layout="wide")
st.title("🚀 Hydrogen Refueling Station Simulator")

st.markdown("""
This simulator estimates hydrogen station requirements based on:
- **Vehicle refueling pressure** (350 or 700 bar)
- **Dispenser throughput**
- **Compressor flowrate**
- **Number of vehicles per hour**
""")

refuel_pressure = st.selectbox("Vehicle Refueling Pressure", [350, 700])
vehicle_count = st.number_input("Number of vehicles per hour", min_value=1, value=10, step=1)
avg_vehicle_storage_liters = st.number_input("Avg. Vehicle Hydrogen Storage Capacity [liters at 1 bar]", value=150.0, step=10.0)
avg_starting_pressure = st.number_input("Average Starting Pressure in Vehicle [bar]", value=100.0, step=10.0)
dispenser_flowrate = st.number_input("Hydrogen flow per nozzle [kg/min]", value=1.67, step=0.1)
compressor_flowrate = st.selectbox("Compressor Capacity", [25, 50])  # in kg/h
compressor_pressure = st.selectbox("Compressor Pressure", [500, 900])  # in bar

run = st.button("Run Simulation")

if run:
    H2_density = 0.08988  # kg/Nm³ at 0°C, 1 atm
    vehicle_volume_Nm3 = avg_vehicle_storage_liters / 1000.0  # convert liters to m³
    usable_volume = vehicle_volume_Nm3 * (refuel_pressure - avg_starting_pressure)
    h2_required_kg = usable_volume * H2_density
    total_H2_per_hour = h2_required_kg * vehicle_count
    total_nozzles = int(np.ceil((total_H2_per_hour / 60) / dispenser_flowrate))
    compressors_needed = int(np.ceil(total_H2_per_hour / compressor_flowrate))

    st.subheader("🔍 Results")
    st.markdown(f"- Estimated **hydrogen needed per vehicle**: `{h2_required_kg:.2f} kg`")
    st.markdown(f"- Estimated **hydrogen flow per hour**: `{total_H2_per_hour:.2f} kg/h`")
    st.markdown(f"- Recommended **number of nozzles**: `{total_nozzles}`")
    st.markdown(f"- Required **number of compressors**: `{compressors_needed}` at {compressor_flowrate} kg/h each")

    st.subheader("📊 Flowrate Curve")
    time = np.arange(0, 60, 1)
    flow = np.ones_like(time) * (total_nozzles * dispenser_flowrate)
    plt.plot(time, flow)
    plt.xlabel("Time (min)")
    plt.ylabel("Total Hydrogen Flow (kg/min)")
    plt.title("Hydrogen Flowrate Profile")
    plt.grid(True)
    st.pyplot(plt.gcf())
