import requests
import socket
import psutil 
import subprocess

def get_ip_and_network():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    # Find the appropriate network interface and its subnet mask
    for name, nic_addrs in psutil.net_if_addrs().items():
        for addr in nic_addrs:
            if addr.family == socket.AF_INET and addr.address == ip_address:
                network = addr.netmask
                return ip_address, network

    return ip_address, "Network not found"

def get_network_name_windows():
    output = subprocess.check_output("netsh wlan show interface").decode()
    for line in output.splitlines():
        if "SSID" in line:
            return line.split(":")[1].strip()
    return "Network name not found"

def send_to_discord(webhook_url, message):
    data = {"content": message}
    response = requests.post(webhook_url, json=data)
    if response.status_code != 204:  # 204 indicates successful message delivery
        print("Error sending to Discord:", response.text)

if __name__ == "__main__":
    webhook_url = "https://discord.com/api/webhooks/1209489160495304764/pSNsnAH07u8mAM3Ra9-oZTqhSZ5ysg_c5wLWAeepqdA-OPTEsxcQYH-Po1IIXHuiXQI2"  # Replace with your actual webhook URL

    ip_address, network = get_ip_and_network()
    network_name = get_network_name_windows()  # Get network name (SSID)
    message = f"Server is open! IP: {ip_address}, Network: {network_name}"
    send_to_discord(webhook_url, message)
