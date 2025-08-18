import requests
import json
import time
import os

API_KEY = 'b075b2f7683c4c7aab9bc228aced203c'
ENDPOINT = 'https://apieathappygroup.azure-api.net/pos/readV2'

HEADERS = {
    'ocp-apim-subscription-key': API_KEY,
    'User-Agent': 'Mozilla/5.0',
    'Accept': '*/*',
    'Origin': 'https://sushirechner.eathappygroup.com',
    'Referer': 'https://sushirechner.eathappygroup.com/'
}

def fetch_cost_center_data(cost_center):
    params = { 'costcenter': cost_center }

    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and data:
            return data
    except Exception as e:
        print("⚠️ Error for cost center {}: {}".format(cost_center, str(e)))
    return None

def is_valid_json_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            json.load(f)
        return True
    except Exception as e:
        print("❌ Invalid JSON in {}: {}".format(filename, str(e)))
        return False

def main():
    all_data = {}
    for i in range(1, 9999):
        cc = str(i).zfill(4)
        print("🔍 Fetching data for cost center {}...".format(cc))
        data = fetch_cost_center_data(cc)
        if data:
            all_data[cc] = data
            print("✅ Data found for {}".format(cc))
        else:
            print("⛔ No data for {}".format(cc))
        time.sleep(0.3)

    output_dir = 'assets'
    os.makedirs(output_dir, exist_ok=True)
    temp_file = os.path.join(output_dir, 'about_temp.json')
    final_file = os.path.join(output_dir, 'about.json')

    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=4, ensure_ascii=False)

        if is_valid_json_file(temp_file):
            if os.path.exists(final_file):
                os.rename(final_file, final_file + '.backup')
                print("📦 Backup saved as '{}.backup'".format(final_file))

            os.replace(temp_file, final_file)
            print("✅ Saved valid data to '{}'".format(final_file))
        else:
            print("🚫 Temp file is invalid. Original '{}' was not replaced.".format(final_file))
            os.remove(temp_file)

    except Exception as e:
        print("❌ Failed to save data: {}".format(str(e)))
        if os.path.exists(temp_file):
            os.remove(temp_file)

if __name__ == '__main__':
    main()
