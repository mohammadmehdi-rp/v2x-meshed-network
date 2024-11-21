import traci
import math
import time
import random

# Simulation Configuration
VEHICLE_COMM_RADIUS = 50.0  # Communication range in meters
VEHICLE_COMM_SPEED = 1.0    # Example communication speed in messages per second
MESSAGE_LIFETIME = 5.0      # Lifetime of a message in seconds
MESSAGE_DELAY = 0.1        # Communication delay in seconds

# Initialize TRACI
sumo_binary = "sumo-gui"
traci.start([sumo_binary, "-c", "config.sumocfg"])

# Open log file for recording communication events
with open("meshed_network_log.txt", "w") as log:
    log.write("Meshed Network Communication Log\n")
    log.write("Time\tSource\tTarget\tType\tRange (m)\tMessage Lifetime Remaining (s)\tMessage Delay (s)\n")

    # Initialize storage for messages
    active_messages = {}  # Format: {msg_id: {"source": veh_id, "time": timestamp, "range": comm_range}}
    total_messages_sent = 0
    successful_deliveries = 0

    try:
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()  # Advance simulation step
            current_time = traci.simulation.getTime()

            # Get active vehicles
            vehicles = traci.vehicle.getIDList()

            # Iterate through all pairs of vehicles for communication
            for i, veh1 in enumerate(vehicles):
                pos1 = traci.vehicle.getPosition(veh1)

                for j, veh2 in enumerate(vehicles):
                    if i >= j:  # Avoid duplicate pair checks
                        continue

                    pos2 = traci.vehicle.getPosition(veh2)
                    distance = math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

                    # Check if vehicles are within communication range
                    if distance <= VEHICLE_COMM_RADIUS:
                        # Simulate packet delay
                        delay = random.uniform(0, MESSAGE_DELAY)  # Random delay between 0 and MESSAGE_DELAY
                        time.sleep(delay)  # Introduce delay before communication

                        # Create a message if none exists between these vehicles
                        msg_id = f"{veh1}_{veh2}_{current_time}"
                        if msg_id not in active_messages:
                            active_messages[msg_id] = {
                                "source": veh1,
                                "target": veh2,
                                "time": current_time,
                                "range": distance,
                                "lifetime": MESSAGE_LIFETIME,
                            }
                            # Log communication event
                            log.write(
                                f"{current_time:.2f}\t{veh1}\t{veh2}\tVTV\t{distance:.2f}\t{MESSAGE_LIFETIME:.2f}\t{delay:.2f}\n"
                            )
                            total_messages_sent += 1

                        # Mark vehicles visually to indicate communication
                        traci.vehicle.setColor(veh1, (0, 255, 0, 255))  # Green
                        traci.vehicle.setColor(veh2, (0, 255, 0, 255))  # Green

                        # Simulate successful message delivery with a certain probability (PDR)
                        if random.random() < 0.9:  # 90% chance of successful delivery
                            successful_deliveries += 1

            # Update active messages, removing expired ones
            expired_msgs = []
            for msg_id, msg_data in active_messages.items():
                # Reduce the lifetime
                msg_data["lifetime"] -= 1.0 / VEHICLE_COMM_SPEED
                if msg_data["lifetime"] <= 0:
                    expired_msgs.append(msg_id)

            # Remove expired messages
            for msg_id in expired_msgs:
                del active_messages[msg_id]

            # Delay to simulate real-world communication speed
            time.sleep(1.0 / VEHICLE_COMM_SPEED)

        # Calculate and log Packet Delivery Ratio (PDR)
        if total_messages_sent > 0:
            pdr = successful_deliveries / total_messages_sent
            log.write(f"\nPDR: {pdr * 100:.2f}% ({successful_deliveries}/{total_messages_sent} successful deliveries)\n")

    except Exception as e:
        print(f"Error during simulation: {e}")
    finally:
        # Ensure proper closing of TRACI
        traci.close()
