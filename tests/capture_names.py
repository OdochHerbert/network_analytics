import subprocess
import re

def capture_device_names():
    try:
        # Run arp-scan to capture device information
        result = subprocess.run(["sudo", "arp-scan", "--localnet"], capture_output=True, text=True)
        output = result.stdout

        # Parse the output to extract device names and MAC addresses
        device_info = []
        lines = output.splitlines()
        for line in lines:
            match = re.match(r"([\d.]+)\s+([\w:]+)\s+(.+)", line)
            if match:
                ip_address = match.group(1)
                mac_address = match.group(2)
                device_name = match.group(3)
                device_info.append((ip_address, mac_address, device_name))

        return device_info

    except Exception as e:
        print(f"An error occurred while capturing device names: {str(e)}")
        return []

if __name__ == "__main__":
    device_info = capture_device_names()
    for ip, mac, name in device_info:
        print(f"IP: {ip}, MAC: {mac}, Device Name: {name}")

