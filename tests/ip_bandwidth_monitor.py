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

if __name__ == "__main__":
    local_ip = discover_local_ip()

    if local_ip:
        print(f"{local_ip}")
    else:
        print("Failed to discover the local IP address.")
  
  

def monitor_bandwidth(ip_address, duration_minutes, output_file):
    try:
        # Create a capture object to capture network traffic on a specific interface
        capture = pyshark.LiveCapture(interface='wlp1s0', display_filter=f'ip.src == {ip_address} or ip.dst == {ip_address}')

        # Open the output CSV file for writing
        with open(output_file, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Timestamp', 'IP Address', 'Bytes In', 'Bytes Out'])

            # Capture and log network traffic for the specified duration
            start_time = datetime.datetime.now()
            end_time = start_time + datetime.timedelta(minutes=duration_minutes)

            for packet in capture.sniff_continuously():
                timestamp = datetime.datetime.now()
                bytes_in = int(packet.length)
                bytes_out = 0  # You may need to calculate outgoing bytes if needed

                # Write the data to the CSV file
                csvwriter.writerow([timestamp, ip_address, bytes_in, bytes_out])
                print(f"Timestamp: {timestamp}, IP: {ip_address}, Bytes In: {bytes_in}, Bytes Out: {bytes_out}")

                if timestamp >= end_time:
                    break

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    ip_to_monitor = discover_local_ip()  # Replace with the IP address you want to monitor
    monitoring_duration_minutes = 0.2  # Adjust the duration as needed
    output_csv_file = 'network_usage.csv'

    monitor_bandwidth(ip_to_monitor, monitoring_duration_minutes, output_csv_file)


