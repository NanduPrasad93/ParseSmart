import requests
from bs4 import BeautifulSoup

def fetch_exam_dates():
    url = "https://www.freejobalert.com/upcoming-exam-dates-of-various-jobs/1835/"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("Failed to fetch data")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the main div containing tables
    main_div = soup.find("div", class_="lssylbts")

    if not main_div:
        print("No div found with class 'lssylbts'")
        return []

    # Find all tables inside the div
    tables = main_div.find_all("table")

    exam_data = []

    for table in tables:
        rows = table.find_all("tr")[1:]  # Skip the header row

        for row in rows:
            columns = row.find_all("td")
            if len(columns) < 3:
                continue

            released_date = columns[0].text.strip()
            exam_name = columns[1].text.strip()
            exam_date = columns[2].text.strip()

            exam_data.append({
                "released_date": released_date,
                "exam_name": exam_name,
                "exam_date": exam_date
            })

    return exam_data







def fetch_defence_exam_dates():
    url = "https://testbook.com/defence"
    headers = {"User-Agent": "Mozilla/5.0"}  # To avoid getting blocked

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    exam_data = []
    
    # Find the table
    table = soup.find("table")
    
    if table:
        rows = table.find_all("tr")[1:]  # Skip the header row
        
        for row in rows:
            columns = row.find_all("td")
            if len(columns) >= 5:
                exam_name = columns[0].text.strip()
                app_start_date = columns[1].text.strip()
                
                # Extract Official Notification link
                official_notification_link = "N/A"
                if columns[2].find("a"):
                    official_notification_link = columns[2].find("a")["href"]
                    if not official_notification_link.startswith("http"):
                        official_notification_link = "https://testbook.com" + official_notification_link  # Handle relative links
                
                last_date_to_apply = columns[3].text.strip()
                exam_date = columns[4].text.strip()

                exam_data.append({
                    "exam_name": exam_name,
                    "app_start_date": app_start_date,
                    "official_notification": official_notification_link,
                    "last_date_to_apply": last_date_to_apply,
                    "exam_date": exam_date,
                })

    return exam_data
