import time, smtplib, requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import *
from urllib.parse import urljoin
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = ''
smtp_password = ''
recipient_email = ''

def send_email(url, error):
    msg = MIMEMultipart()
    msg['Subject'] = 'WEBPAGE UNRESPONSIVE!'
    msg['From'] = smtp_user
    msg['To'] = recipient_email
    body = f"The webpage {url} is unresponsive.\nError: {error}"
    msg.attach(MIMEText(body))
    
    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(smtp_user, smtp_password)
        smtp.sendmail(smtp_user, recipient_email, msg.as_string)

def extract_urls(main_url):
    urls_to_monitor = []
    try:
        response = requests.get(main_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                full_url = urljoin(main_url, link['href'])
                if full_url.startswith(main_url):
                    urls_to_monitor.append(full_url)
        else:
            print("Failed to access the website")
    except Exception as e:
        print("Error: " + str(e))

    return urls_to_monitor

def monitor_webpages(urls_to_monitor):
    res_monitor_webpages = []
    while True:
        for url in urls_to_monitor:
            try:
                response = urlopen(url)
                if response.status != 200:
                    raise HTTPError(url, response.status, "Page not reachable", None, None)
            except (HTTPError, URLError) as e:
                print(f"Error detected for {url}: {e}")
                send_email(url, str(e))
                res_monitor_webpages.append([url, "Unresponsive", str(e)])
            else:
                print(f"{url} is reachable.")
                res_monitor_webpages.append([url, "Responsive", "No Error"])
                        
        df = pd.DataFrame(res_monitor_webpages, columns=["URL", "Status", "Error"])
        df.to_excel("site_status.xlsx", index=False)
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\nCurrent time: {current_time}")
        print("Monitoring Complete. Waiting for 2 hours before the next check.")
        countdown(7200)
        
def countdown(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timeformat = f"{mins:02d}:{secs:02d}"
        print(f"Next check in: {timeformat}", end='\r')
        time.sleep(1)
        seconds -= 1
    print("\nStarting the next check...\n")
    
if __name__ == "__main__":
    
    main_url = " "
    
    urls_to_monitor = extract_urls(main_url)
    
    if urls_to_monitor:
        print("Starting monitoring for the following URLs:")
        for url in urls_to_monitor:
            print(url)
        monitor_webpages(urls_to_monitor)
    else:
        print("No URLs found or unable to access the website. Exiting.")