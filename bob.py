import requests

webhook_url = 'https://discord.com/api/webhooks/1209489160495304764/pSNsnAH07u8mAM3Ra9-oZTqhSZ5ysg_c5wLWAeepqdA-OPTEsxcQYH-Po1IIXHuiXQI2'  # Replace with your actual webhook URL

data = {"content": "Server is open"}
response = requests.post(webhook_url, json=data)

if response.status_code == 204:
    print('Message sent successfully.')
else:
    print('An error occurred:', response.status_code)