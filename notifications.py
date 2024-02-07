# Made by libalpm 2024 
# This is a GNU LICENSE this free to use for any purpose
# Instructions:
# 1. Download the chrome driver from https://chromedriver.storage.googleapis.com/index.html
# 2. Download the latest chromium for linux (wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb) this may change in the future
# 3. dpkg -i install the package 
# 4. make sure you chmod the web driver
# 5. It's going to ask you to install a million dependcies as chrome is bloated.
# 6. Recommendation install this first: sudo apt-get install libnss3 then run apt-get --fix-broken install (for debian based distros)
# 7. Enter your paths and enter in your credentials.
# 8. Run the notifications.py

import requests, time, subprocess, re, urllib3
from bs4 import BeautifulSoup

# Replicating the cURL request in Python
url = 'https://cp.pathmodule.com/client/ddos'
headers = {
    'authority': 'cp.pathmodule.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.7',
    'cookie': 'XSRF-TOKEN=initial_XSRF_TOKEN_value; pathmodule_session=initial_pathmodule_session_value',
    'referer': 'https://cp.pathmodule.com/client/filters',
    'sec-ch-ua': '"Not A(Brand";v="99", "Brave";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}


def update_cookies(new_cookies):
    headers['cookie'] = f"XSRF-TOKEN={new_cookies['XSRF-TOKEN']}; pathmodule_session={new_cookies['pathmodule_session']}"

def get_new_cookies():
    # Was to lazy to make the process run in the background and capture the output
    result = subprocess.run(['python3', 'chrome-webdriv.py'], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Subprocess failed with return code: {result.returncode}")
        print(f"Error output: {result.stderr}")
        return False

    output = result.stdout
    new_cookies = {}
    # A goofy way to retrieve the object from the tablebase
    xsrf_token_match = re.search(r'XSRF-TOKEN=([^\s]+)', output)
    session_match = re.search(r'pathmodule_session=([^\s]+)', output)

    if xsrf_token_match and session_match:
        new_cookies['XSRF-TOKEN'] = xsrf_token_match.group(1)
        new_cookies['pathmodule_session'] = session_match.group(1)
        return new_cookies
    else:
        print("Failed to retrieve new cookies from the subprocess output.")
        return False

last_seen_attacks = {}
def fetch_and_process_ddos_data():
    global last_seen_attacks
    new_cookies = get_new_cookies()
    if new_cookies:
        update_cookies(new_cookies)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', {'id': 'ddosTable'})
            if table is None:
                print("Unable to fetch table, trying to retrieve new cookies...")
                new_cookies = get_new_cookies()
                if new_cookies:
                    update_cookies(new_cookies)
                    print("Retrieved new cookies. Re-running the data fetch...")
                    fetch_and_process_ddos_data()
                else:
                    print("Unable to retrieve data after cookie refresh.")
                return
            
            rows = table.find_all('tr')[1:]
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) < 6:
                    continue
                
                # Don't flame me for this part right here. It's a mess.
                host = cols[0].text.strip()
                start = cols[1].text.strip()
                end = cols[2].text.strip()
                peak_gbps_str = cols[3].text.strip()
                peak_pps_str = cols[4].text.strip()
                peak_gbps_clean = peak_gbps_str.replace(' Gb/s', '')
                peak_pps_clean = peak_pps_str.replace(' Pp/s', '')
                peak_gbps = round(float(peak_gbps_clean) * 2.5, 2)
                peak_pps = int(round(float(peak_pps_clean) * 2.5, 2))
                attack_key = (host, start)
                new_attack_details = (end, peak_gbps, peak_pps)
                if attack_key not in last_seen_attacks:
                    print(f"DDoS attack detected! Host: {host}, Start: {start}, Peak Gb/s: {peak_gbps}, Peak Pps: {peak_pps}")
                    last_seen_attacks[attack_key] = new_attack_details
                else:
                    last_end, last_peak_gbps, last_peak_pps = last_seen_attacks[attack_key]
                    if end != last_end:
                        if end:
                            print(f"DDoS attack ended! Host: {host}, Start: {start}, End: {end}, Peak Gb/s: {peak_gbps}, Peak Pps: {peak_pps}")
                        else:
                            print(f"DDoS attack size updated! Host: {host}, Start: {start}, New Peak Gb/s: {peak_gbps}, New Peak Pps: {peak_pps}")
                        last_seen_attacks[attack_key] = new_attack_details
                
        else:
            print(f"Failed to retrieve data, status code: {response.status_code}")
    else:
        print("Unable to retrieve new cookies.")

print("Initializing DDoS attack data...")
fetch_and_process_ddos_data()

print("Starting monitoring for new DDoS attacks...")
while True:
    fetch_and_process_ddos_data()
    time.sleep(30)