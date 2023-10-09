import os
import csv

def get_connected_devices():
    try:
        # Run the arp-scan command to list devices on the network
        output = os.popen('sudo arp-scan --localnet').read()

        # Parse the output to extract MAC addresses
        lines = output.split('\n')
        mac_addresses = []

        for line in lines:
            if '\t' in line:
                parts = line.split('\t')
                mac_address = parts[0]
                mac_addresses.append(mac_address)

        return mac_addresses

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []

def save_to_csv(mac_addresses, filename):
    try:
        with open(filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['MAC Address'])
            csvwriter.writerows(mac_addresses)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"An error occurred while saving to CSV: {str(e)}")

if __name__ == "__main__":
    connected_devices = get_connected_devices()
    
    if connected_devices:
        print("Connected Devices (MAC addresses):")
        for device in connected_devices:
            print(device)

        # Save the data to a CSV file
        save_to_csv(connected_devices, 'connected_devices.csv')
    else:
        print("No devices found or error occurred.")
