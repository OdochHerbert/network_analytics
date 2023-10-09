import socket
import csv
import datetime
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

def monitor_bandwidth(duration_seconds, output_file):
    try:
        # Create a capture object to capture network traffic on a specific interface
        # Filter to capture traffic only within your local subnet (e.g., 192.168.1.x)
        capture = pyshark.LiveCapture(interface='wlp1s0', display_filter=f'ip.addr==192.168.1.0/24')

        # Dictionary to store byte counts and other information for each IP address
        ip_info = {}

        # Open the output CSV file for writing
        with open(output_file, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['IP Address', 'MAC Address', 'Bytes In', 'Bytes Out'])

            # Capture and log network traffic for the specified duration
            start_time = time.time()
            end_time = start_time + duration_seconds

            for packet in capture.sniff_continuously():
                if 'ip' in packet:
                    src_ip = packet.ip.src
                    dst_ip = packet.ip.dst
                    mac_address = packet.eth.src
                    bytes_in = int(packet.length)

                    # Update byte count for the source IP
                    if src_ip in ip_info:
                        ip_info[src_ip]['Bytes In'] += bytes_in
                        ip_info[src_ip]['Bytes Out'] += 0
                    else:
                        ip_info[src_ip] = {'MAC Address': mac_address, 'Bytes In': bytes_in, 'Bytes Out': 0}

                    # Update byte count for the destination IP
                    if dst_ip in ip_info:
                        ip_info[dst_ip]['Bytes Out'] += bytes_in
                        ip_info[dst_ip]['Bytes In'] += 0
                    else:
                        ip_info[dst_ip] = {'MAC Address': mac_address, 'Bytes In': 0, 'Bytes Out': bytes_in}

                if time.time() >= end_time:
                    break

            # Write the aggregated data to the CSV file
            for ip, info in ip_info.items():
                csvwriter.writerow([ip, info['MAC Address'], info['Bytes In'], info['Bytes Out']])

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    monitoring_duration_seconds = 10  # Adjust the duration in seconds as needed
    output_csv_file = 'network_usage.csv'

    monitor_bandwidth(monitoring_duration_seconds, output_csv_file)

