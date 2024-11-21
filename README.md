# SUMO-NS3 Based Vehicular Communication Simulation

This repository contains a **SUMO (Simulation of Urban Mobility)** project designed to simulate vehicular communication using **RSU (Roadside Units)** and **V2V (Vehicle-to-Vehicle)** meshed networking. The simulation analyzes communication metrics such as latency, range, and packet delivery ratio (PDR).

## **Features**
1. **RSU-to-Vehicle Communication (RTV)**:  
   Simulates message broadcasting from RSUs to vehicles within a predefined radius.
   
2. **Vehicle-to-Vehicle Communication (VTV)**:  
   Simulates message exchanges between vehicles in proximity.

3. **Logs Communication Events**:  
   Logs time, source, target, type, range, and delay of communication events.

4. **Performance Metrics**:  
   - Maximum communication range.
   - Packet Delivery Ratio (PDR).

## **Requirements**
1. **SUMO (Simulation of Urban Mobility)**  
   Download from [SUMO Official Website](https://sumo.dlr.de/).

2. **Python 3.8+**  
   Required libraries:  
   - `traci` (SUMO Python bindings)  
   - `numpy` (for efficient calculations)

3. **NS-3**  
   Handles communication simulation (packet loss, signal strength, delay).  
   [NS-3 Installation Guide](https://www.nsnam.org/).

4. **Machine Specifications**:  
   A machine with sufficient CPU and RAM to handle SUMO and NS-3 simulations.

## **Setup**
### **Clone the Repository**
```bash
git clone https://github.com/mohammadmehdi-rp/v2x-meshed-network.git
cd v2x-meshed-network
```

### **Install SUMO**
Follow the installation instructions for your operating system:
- [Windows Installation Guide](https://sumo.dlr.de/docs/Installing/Windows.html)  
- [Linux Installation Guide](https://sumo.dlr.de/docs/Installing/Linux_Build.html)  
- [macOS Installation Guide](https://sumo.dlr.de/docs/Installing/MacOS.html)  

Ensure `sumo` and `sumo-gui` are added to your system's PATH.

### **Install Python Dependencies**
Create a virtual environment and install required libraries:
```bash
python -m venv env
source env/bin/activate      # Use env\Scripts\activate on Windows
pip install -r requirements.txt
```

### **Verify Installation**
Run the following commands to verify the setup:
```bash
sumo --version
python -m traci --help
```

## **Run the Simulation**
### **Prepare Configuration Files**
Ensure the following files are present and properly configured:
1. `config.sumocfg`: Main SUMO configuration file.
2. `map.net.xml`: Network file describing the road layout.
3. `routes.rou.xml`: Routes file defining vehicle generation and movement.
4. `additional.xml`: Additional definitions (e.g., induction loops for RSUs).

### **Start the Simulation**
Run the Python script:
```bash
cd ns-3-dev
cd media
python3 simulate_dsrc_meshed.py
python3 simulate_dsrc.py
```

## **Expected Output**
1. **Simulation Visualization**:  
   If running `sumo-gui`, you'll see vehicle and RSU interactions on the map.

2. **Log File**:  
   Communication events are logged in `non_meshed_network_log.txt` and `meshed_network_log.txt`, including:
   - Time of communication.
   - Source and target of communication.
   - Type of communication (RTV or VTV).
   - Distance between entities.
   - Communication delay.

3. **Metrics**:
   - Maximum communication range.
   - Packet Delivery Ratio (PDR).

4. **Meshed Networking Analysis**:  
   The log file `meshed_network_log.txt` can be used to analyze how meshed networking improves **V2X (Vehicle-to-Everything)** communication.  
   By comparing latency, PDR, and range values between RTV and VTV communication, you can understand how VTV meshed networking complements RSU communication, enabling better reliability and coverage.

## **Troubleshooting**
### **Simulation Freezes or Lags**
- Reduce the number of vehicles in `routes.rou.xml`.
- Simplify the map in `map.net.xml`.
- Optimize the Python script (consider running without GUI for large simulations).

### **SUMO Not Found**
- Verify that SUMO binaries (`sumo`, `sumo-gui`) are added to your system's PATH.
