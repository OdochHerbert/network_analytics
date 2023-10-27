from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

# Function to execute shell commands
def run_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return result.stderr

# Example route to get network interfaces
@app.route('/network/interfaces', methods=['GET'])
def get_network_interfaces():
    command = "ip link show"
    network_interfaces = run_command(command)
    return jsonify({'network_interfaces': network_interfaces})

# Example route to get IP addresses
@app.route('/network/ip_addresses', methods=['GET'])
def get_ip_addresses():
    command = "ip addr show"
    ip_addresses = run_command(command)
    return jsonify({'ip_addresses': ip_addresses})

# Example route to get routing tables
@app.route('/network/routing_tables', methods=['GET'])
def get_routing_tables():
    command = "ip route show"
    routing_tables = run_command(command)
    return jsonify({'routing_tables': routing_tables})

# Example route to get network statistics
@app.route('/network/statistics', methods=['GET'])
def get_network_statistics():
    command = "netstat -s"
    network_statistics = run_command(command)
    return jsonify({'network_statistics': network_statistics})
#GEtting info from pyhton code
# Example route to get network interfaces
@app.route('/code', methods=['GET'])
def get_print():
    command = "sudo python macs_usage.py"
    code = run_command(command)
    return jsonify(code)
@app.route('/bandwidth_monitor', methods=['GET'])
def get_band_monitor():
      command = 'sudo iftop -t -s 10'
      bandwidth_usage =  run_command(command)
      return jsonify(bandwidth_usage)
if __name__ == '__main__':
    app.run(debug=True, port=5007)  # Set the port to 5007
