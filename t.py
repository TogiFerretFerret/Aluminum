import requests



headers = {
    #'accept': '*/*',
    #'accept-language': 'en-US,en;q=0.9',
    'cookie': 't=7cbebf07-4b35-dc01-6ee7-8b7eaf94a2fe',
    #'priority': 'u=1, i',
    #'referer': 'https://hunterschools.myschoolapp.com/app/file/DropBoxFile?aiid=35288409&uTolken=XwtCURZXV30%3d&tolken=h6c0Oj0rh6pbj7z3BS7M0w%3d%3d',
    #'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    #'sec-ch-ua-mobile': '?0',
    #'sec-ch-ua-platform': '"Windows"',
    #'sec-fetch-dest': 'empty',
    #'sec-fetch-mode': 'no-cors',
    #'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

response = requests.get(
    'https://hunterschools.myschoolapp.com/app/file/DropBoxFile?aiid=35288409&uTolken=XwtCURZXV30%3d&tolken=h6c0Oj0rh6pbj7z3BS7M0w%3d%3d',
    #cookies=cookies,
    headers=headers,
)
with open("file.jpeg", "wb") as f:
    f.write(response.content)