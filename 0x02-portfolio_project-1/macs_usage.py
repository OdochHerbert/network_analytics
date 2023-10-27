import socket
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

def monitor_bandwidth(duration_seconds):
    try:
        # Create a capture object to capture network traffic on a specific interface
        # Filter to capture traffic only within your local subnet (e.g., 192.168.1.x)
        capture = pyshark.LiveCapture(interface='wlp1s0', display_filter=f'ip.addr==192.168.1.0/24')

        # Dictionary to store byte counts and other information for each MAC address
        mac_info = {}

        # Capture and log network traffic for the specified duration
        start_time = time.time()
        end_time = start_time + duration_seconds

        for packet in capture.sniff_continuously():
            if 'ip' in packet:
                src_mac = packet.eth.src
                dst_mac = packet.eth.dst
                bytes_in = int(packet.length)

                # Update byte count for the source MAC address
                if src_mac in mac_info:
                    mac_info[src_mac]['Bytes In'].append(bytes_in)
                else:
                    mac_info[src_mac] = {'Bytes In': [bytes_in], 'Bytes Out': []}

                # Update byte count for the destination MAC address
                if dst_mac in mac_info:
                    mac_info[dst_mac]['Bytes Out'].append(bytes_in)
                else:
                    mac_info[dst_mac] = {'Bytes In': [], 'Bytes Out': [bytes_in]}

            if time.time() >= end_time:
                break

        return mac_info

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    monitoring_duration_seconds = 10  # Adjust the duration in seconds as needed

    result = monitor_bandwidth(monitoring_duration_seconds)
    if result is not None:
        for mac, info in result.items():
            print(f"MAC Address: {mac}, Bytes In: {info['Bytes In']}, Bytes Out: {info['Bytes Out']}")
