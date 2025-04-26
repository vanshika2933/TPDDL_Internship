# Import necessary libraries
import time
import smtplib
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import *
from urllib.parse import urljoin
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import sys

load_dotenv()

# SMTP (email) server settings
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = os.getenv('SMTP_USER')
smtp_password = os.getenv('SMTP_PASSWORD')
recipient_email = os.getenv('RECIPIENT_EMAIL

# Function to send an email alert if a webpage is unresponsive
def send_email(url, error):
    msg = MIMEMultipart()
    msg['Subject'] = 'WEBPAGE UNRESPONSIVE!'
    msg['From'] = smtp_user
    msg['To'] = recipient_email
    body = f"The webpage {url} is unresponsive.\nError: {error}"
    msg.attach(MIMEText(body))
    
    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.ehlo()
        smtp.starttls()  # Secure the connection
        smtp.login(smtp_user, smtp_password)
        smtp.sendmail(smtp_user, recipient_email, msg.as_string)

# Function to extract all internal URLs from a given main website URL
def extract_urls(main_url):
    urls_to_monitor = []
    try:
        response = requests.get(main_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find all <a> tags with href attributes
            for link in soup.find_all('a', href=True):
                full_url = urljoin(main_url, link['href'])
                # Only add URLs that belong to the same domain
                if full_url.startswith(main_url):
                    urls_to_monitor.append(full_url)
        else:
            print("Failed to access the website")
    except Exception as e:
        print("Error: " + str(e))

    return urls_to_monitor

# Function to monitor the list of webpages periodically
def monitor_webpages(urls_to_monitor):
    res_monitor_webpages = []  # List to store results

    while True:
        for url in urls_to_monitor:
            try:
                response = urlopen(url)
                # If the page doesn't return a 200 OK status, treat it as an error
                if response.status != 200:
                    raise HTTPError(url, response.status, "Page not reachable", None, None)
            except (HTTPError, URLError) as e:
                # If any error occurs, send an alert and record the issue
                print(f"Error detected for {url}: {e}")
                send_email(url, str(e))
                res_monitor_webpages.append([url, "Unresponsive", str(e)])
            else:
                # If the site is reachable, log it
                print(f"{url} is reachable.")
                res_monitor_webpages.append([url, "Responsive", "No Error"])
                        
        # Save the monitoring results into an Excel file
        df = pd.DataFrame(res_monitor_webpages, columns=["URL", "Status", "Error"])
        df.to_excel("site_status.xlsx", index=False)
        
        # Log the time and wait before the next monitoring cycle
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\nCurrent time: {current_time}")
        print("Monitoring Complete. Waiting for 2 hours before the next check.")
        countdown(7200)  # Wait for 2 hours (7200 seconds)

# Helper function to create a visible countdown timer between monitoring cycles
def countdown(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timeformat = f"{mins:02d}:{secs:02d}"
        print(f"Next check in: {timeformat}", end='\r')
        time.sleep(1)
        seconds -= 1
    print("\nStarting the next check...\n")
    
# Main execution block
if __name__ == "__main__":
    
    main_url = " "  # Enter the main URL you want to monitor
    
    urls_to_monitor = extract_urls(main_url)
    
    if urls_to_monitor:
        print("Starting monitoring for the following URLs:")
        for url in urls_to_monitor:
            print(url)
        monitor_webpages(urls_to_monitor)
    else:
        print("No URLs found or unable to access the website. Exiting.")
