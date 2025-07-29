import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Hydrogen Refueling Simulator", layout="centered")

st.title("🚛 Hydrogen Refueling Station Simulator")
st.markdown("Simulate your H2 station sizing and refueling flow ⛽")

st.sidebar.header("📋 Station Configuration")

# Select compressor type
compressor_type = st.sidebar.radio("Compressor Type", ["25 kg/h @ 900 bar", "50 kg/h @ 500 bar"])
compressor_flow = 25 if "25" in compressor_type else 50
compressor_pressure = 900 if "900" in compressor_type else 500

# Select refueling pressure
vehicle_pressure = st.sidebar.selectbox("Vehicle Refueling Pressure", [350, 700])
num_nozzles = st.sidebar.slider("Number of Nozzles", 1, 6, 2)
avg_vehicle_size = st.sidebar.number_input("Vehicle H2 Capacity (kg)", min_value=1.0, value=20.0)
avg_starting_pressure = st.sidebar.number_input("Average Starting Pressure (bar)", min_value=0.0, value=50.0)
vehicles_per_hour = st.sidebar.number_input("Vehicles per hour", min_value=1, value=10)

# Compression time
compressor_startup_time = 15  # min
nozzle_flow_rate = 1.0 * num_nozzles  # kg/min total

st.markdown("---")
st.subheader("🧮 Simulation Results")

# Estimate refueling time per vehicle
delta_pressure = vehicle_pressure - avg_starting_pressure
vehicle_fill_time = avg_vehicle_size / nozzle_flow_rate  # in minutes

# Required hourly flow
required_flow = avg_vehicle_size * vehicles_per_hour  # kg/h

# Number of compressors
effective_compressor_flow = compressor_flow * (45 / 60)  # accounting for 15min startup
compressors_needed = np.ceil(required_flow / effective_compressor_flow)

# Output
st.markdown(f"**Estimated fill time per vehicle**: {vehicle_fill_time:.1f} minutes")
st.markdown(f"**Total H2 required per hour**: {required_flow:.1f} kg")
st.markdown(f"**Effective compressor capacity**: {effective_compressor_flow:.1f} kg/h")
st.markdown(f"**Estimated compressors required**: {int(compressors_needed)} unit(s)")

# Plot
time = np.linspace(0, vehicle_fill_time, 100)
pressure_curve = avg_starting_pressure + (vehicle_pressure - avg_starting_pressure) * (1 - np.exp(-time / 3))

fig, ax = plt.subplots()
ax.plot(time, pressure_curve, label="Vehicle Pressure", color="blue")
ax.axhline(vehicle_pressure, color="green", linestyle="--", label="Target Pressure")
ax.set_xlabel("Time (min)")
ax.set_ylabel("Pressure (bar)")
ax.set_title("Hydrogen Pressure During Refueling")
ax.legend()
st.pyplot(fig)
