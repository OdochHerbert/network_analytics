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
        # Create a capture object to capture network traffic on all available interfaces
        capture = pyshark.LiveCapture(interface='wlp1s0')

        # Open the output CSV file for writing
        with open(output_file, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Timestamp', 'IP Address', 'Bytes In', 'Bytes Out'])

            # Capture and log network traffic for the specified duration
            start_time = time.time()
            end_time = start_time + duration_seconds

            for packet in capture.sniff_continuously():
                if 'ip' in packet:
                    timestamp = datetime.datetime.now()
                    ip_address = packet.ip.src if 'ip.src' in packet else packet.ip.dst
                    bytes_in = int(packet.length)
                    bytes_out = 0  # You may need to calculate outgoing bytes if needed

                    # Write the data to the CSV file
                    csvwriter.writerow([timestamp, ip_address, bytes_in, bytes_out])
                    print(f"Timestamp: {timestamp}, IP: {ip_address}, Bytes In: {bytes_in}, Bytes Out: {bytes_out}")

                if time.time() >= end_time:
                    break

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    monitoring_duration_seconds = 10  # Adjust the duration in seconds as needed
    output_csv_file = 'network_usage.csv'

    monitor_bandwidth(monitoring_duration_seconds, output_csv_file)

