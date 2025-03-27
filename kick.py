from seleniumbase import SB
import json
import time
import re
import pandas as pd

def extract_email(text):
    """
    We're looking in the email string
    """
    if text:
        match = re.search(r'[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}', text)
        return match.group(0) if match else ""
    else:
        return ""

def find_telegram_link(text):
    """
    Looking for a telegram link
    """
    if text:
        match = re.search(r'https?://t\.me/\S+', text)
        return match.group(0) if match else ""
    else:
        return ""

def save_to_excel(data, filename="output.xlsx"):
    df = pd.DataFrame(data)
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        worksheet = writer.sheets['Sheet1']
        for col_num, col in enumerate(df.columns):
            worksheet.set_column(col_num, col_num, 20)

def scraping(base_url):
    json_filename = './data.json'
    page = 1
    all_data = []

    with SB(uc=True) as sb:
        while True:
            url = base_url.format(page=page)
            print(f"Loading the page {page}: {url}")
            sb.open(url)
            time.sleep(1)
            
            body_content = sb.get_page_source()
            
            try:
                json_start = body_content.find("<body>") + 6
                json_end = body_content.find("</body>")
                json_text = body_content[json_start:json_end].strip()
                parsed_json = json.loads(json_text)
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error parsing JSON: {e}")
                break
            
            data = parsed_json.get("data", [])
            
            if not data:
                print("We're out of data, let's get out.")
                break
            
            all_data.extend(data)
            page += 1

    with open(json_filename, 'w') as f:
        f.write(json.dumps(all_data, indent=4))
        
    print(f"Collected {len(all_data)} records.")
    
    with open(json_filename, 'r') as f:
        all_data = json.loads(f.read())

    data_users = []
    for item in all_data:
        language = item['language']
        channel = item['channel']['user']
        
        bio = channel['bio']
        email = extract_email(bio)
        telegram = find_telegram_link(bio)
        data_j = {
            "language": language,
            "username": channel['username'],
            "email": email,
            "instagram": channel['instagram'],
            "twitter": channel['twitter'],
            "telegram": telegram,
            "youtube": channel['youtube'],
            "discord": channel['discord'],
            "tiktok": channel['tiktok'],
            "facebook": channel['facebook'],
        }
        
        if not data_j["email"] and not data_j["instagram"] and not data_j["twitter"] and not data_j["twitter"] and not data_j["telegram"] and not data_j["youtube"] and not data_j["discord"] and not data_j["tiktok"] and not data_j["facebook"]:
            continue
        data_users.append(data_j)
    
    save_to_excel(data_users)
    
    # with open('./test.json', 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(data_users, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    # Get all streamers in the Gambling category in all languages
    BASE_URL = "https://kick.com/stream/livestreams/az%2Csq%2Cam%2Cen%2Car%2Cast%2Cbe%2Cbn%2Cbg%2Cbs%2Chu%2Cgl%2Cel%2Cda%2Cid%2Ces%2Cit%2Cca%2Czh%2Cko%2Cla%2Clt%2Cmk%2Cml%2Cmn%2Cde%2Cnl%2Cno%2Cnb%2Cfa%2Cpl%2Cpt%2Cro%2Cru%2Csr%2Csi%2Csk%2Csl%2Csu%2Cth%2Ctr%2Cuk%2Cfil%2Cfi%2Cfr%2Chi%2Chr%2Cckb%2Ccs%2Csv%2Ceo%2Cet%2Cja?page={page}&limit=24&sort=featured&strict=true&tags=Gambling"
    scraping(BASE_URL)