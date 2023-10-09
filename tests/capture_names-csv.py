import subprocess
import re
import csv

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

def save_to_csv(device_info, output_file):
    try:
        # Open the CSV file for writing
        with open(output_file, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['IP Address', 'MAC Address', 'Device Name'])

            # Write device information to the CSV file
            for ip, mac, name in device_info:
                csvwriter.writerow([ip, mac, name])

        print(f"Device information saved to {output_file}")

    except Exception as e:
        print(f"An error occurred while saving to CSV: {str(e)}")

if __name__ == "__main__":
    output_csv_file = 'device_info.csv'
    device_info = capture_device_names()
    save_to_csv(device_info, output_csv_file)

