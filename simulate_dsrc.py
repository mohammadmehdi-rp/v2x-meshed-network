import traci
import time
import math

# Configuration for RSU and communication ranges
RSU_POS = (50.0, 0.0)  # Example RSU position (adjust based on actual position in the network)
RSU_RADIUS = 50.0  # RSU communication range in meters
VEHICLE_COMM_RADIUS = 30.0  # Vehicle-to-Vehicle communication range
VEHICLE_COMM_SPEED = 1.0  # Example communication speed in m/s (adjust as necessary)

sumo_binary = 'sumo-gui'
# Start SUMO with the config file
traci.start([sumo_binary, "-c", "config.sumocfg"])

# Open a log file for communication events
with open("communication_log.txt", "w") as log:
    log.write("Communication Log\n")
    log.write("Time\tSource\tTarget\tType\tDelay (s)\tRange (m)\tPDR (%)\n")

    # Initialize metrics
    total_sent_packets = 0
    total_received_packets = 0
    max_range = 0

    vehicle_last_comms = {}  # Dictionary to store the last communication times for vehicles

    try:
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()  # Advance simulation step
            current_time = traci.simulation.getTime()

            # Get all active vehicles in the simulation
            vehicles = traci.vehicle.getIDList()

            # RSU-to-Vehicle Communication (Induction Loop RSU1)
            for veh_id in vehicles:
                veh_pos = traci.vehicle.getPosition(veh_id)
                distance_to_rsu = math.sqrt((veh_pos[0] - RSU_POS[0]) ** 2 + (veh_pos[1] - RSU_POS[1]) ** 2)

                # Update max range
                if distance_to_rsu > max_range:
                    max_range = distance_to_rsu

                # Example tweak to log successful RSU-to-Vehicle communication only if within range
                if distance_to_rsu <= RSU_RADIUS:
                    total_sent_packets += 1  # RSU sends message to vehicle
                    comm_time = current_time
                    if veh_id not in vehicle_last_comms or comm_time - vehicle_last_comms[
                        veh_id] > 1:  # Ensure fresh communication
                        delay = comm_time - vehicle_last_comms.get(veh_id, comm_time)
                        log.write(f"{comm_time}\tRSU\t{veh_id}\tRTV\t{delay:.2f}\t{distance_to_rsu:.2f}\n")
                        vehicle_last_comms[veh_id] = comm_time
                    total_received_packets += 1  # Successful communication
                    traci.vehicle.setColor(veh_id, (255, 0, 0, 255))  # Indicate communication success

            # Vehicle-to-Vehicle Communication
            for veh1 in vehicles:
                for veh2 in vehicles:
                    if veh1 != veh2:  # Avoid self-comparison
                        pos1 = traci.vehicle.getPosition(veh1)
                        pos2 = traci.vehicle.getPosition(veh2)

                        distance = math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

                        if distance <= VEHICLE_COMM_RADIUS:
                            total_sent_packets += 1  # Message sent to another vehicle
                            comm_time = current_time
                            if veh1 not in vehicle_last_comms:
                                vehicle_last_comms[veh1] = comm_time
                            else:
                                delay = comm_time - vehicle_last_comms[veh1]  # Calculate latency/delay
                                log.write(f"{comm_time}\t{veh1}\t{veh2}\tVTV\t{delay}\t{distance}\n")
                            if veh2 not in vehicle_last_comms:
                                vehicle_last_comms[veh2] = comm_time
                            else:
                                delay = comm_time - vehicle_last_comms[veh2]  # Calculate latency/delay
                                log.write(f"{comm_time}\t{veh2}\t{veh1}\tVTV\t{delay}\t{distance}\n")

                            # Mark vehicles as communicating
                            traci.vehicle.setColor(veh1, (255, 0, 0, 255))  # Green for veh1
                            traci.vehicle.setColor(veh2, (0, 255, 0, 255))  # Green for veh2

            # Calculate Packet Delivery Ratio (PDR)
            pdr = (total_received_packets / total_sent_packets) * 100 if total_sent_packets > 0 else 0

            # Log final metrics
            log.write(f"End of Simulation:\nMax Range: {max_range} meters\nPDR: {pdr}%\n \n \n")

            # Delay to simulate transmission time
            time.sleep(0.1)  # Adjust as necessary to simulate delay in the communication process

    except Exception as e:
        print(f"Error during simulation: {e}")
    finally:
        traci.close()
