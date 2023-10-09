import subprocess
import re
import csv
import pyshark
import time

def discover_local_ip():
    try:
        # Create a socket object to discover the local IP address
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Connect to a public DNS server (e.g., Google's DNS)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            return local_ip
    except Exception as e:
        print(f"An error occurred while discovering the local IP address: {str(e)}")
        return None

def map_mac_to_device(mac_address):
    # You should implement this function to map MAC addresses to device names
    # For demonstration purposes, we use a simple hardcoded dictionary here
    mac_to_device = {
        '00:11:22:33:44:55': 'Device1',
        'AA:BB:CC:DD:EE:FF': 'Device2',
        # Add more entries as needed
    }
    return mac_to_device.get(mac_address, 'Unknown Device')

def capture_device_info(duration_seconds):
    try:
        # Create a capture object to capture network traffic on a specific interface
        capture = pyshark.LiveCapture(interface='wlp1s0', display_filter=f'ip.addr==192.168.1.0/24')

        # Dictionary to store device information
        device_info = {}

        # Open the CSV file for writing
        with open('device_info.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['IP Address', 'Device Name', 'Bytes In', 'Bytes Out'])

            # Capture and log network traffic for the specified duration
            start_time = time.time()
            end_time = start_time + duration_seconds

            for packet in capture.sniff_continuously():
                if 'ip' in packet:
                    src_mac = packet.eth.src
                    dst_mac = packet.eth.dst
                    bytes_in = int(packet.length)

                    # Map MAC addresses to device names
                    src_device = map_mac_to_device(src_mac)
                    dst_device = map_mac_to_device(dst_mac)

                    # Get IP addresses
                    src_ip = packet.ip.src
                    dst_ip = packet.ip.dst

                    # Update byte count for the source IP
                    if src_ip in device_info:
                        device_info[src_ip]['Bytes In'] += bytes_in
                    else:
                        device_info[src_ip] = {'Device Name': src_device, 'Bytes In': bytes_in, 'Bytes Out': 0}

                    # Update byte count for the destination IP
                    if dst_ip in device_info:
                        device_info[dst_ip]['Bytes Out'] += bytes_in

                if time.time() >= end_time:
                    break

            # Write the aggregated data to the CSV file
            for ip, info in device_info.items():
                csvwriter.writerow([ip, info['Device Name'], info['Bytes In'], info['Bytes Out']])

        print("Device information saved to device_info.csv")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    monitoring_duration_seconds = 10  # Adjust the duration in seconds as needed
    capture_device_info(monitoring_duration_seconds)

