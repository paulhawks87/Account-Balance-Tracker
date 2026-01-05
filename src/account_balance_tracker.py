from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ======================================================
# CONFIGURATION
# ======================================================

# List of account addresses to track
ADDRESSES = [
    # "ACCOUNT_ADDRESS_1",
    # "ACCOUNT_ADDRESS_2",
]

# Explorer URL template
# Replace with the appropriate explorer URL for your project
# Example: "https://example-explorer.com/accounts/{address}"
EXPLORER_ACCOUNT_URL = "https://YOUR-BLOCKCHAIN-EXPLORER/accounts/{address}"

# Label used on the explorer page for balance lookup
# Example values: "Free Balance", "Available Balance", "Balance"
BALANCE_LABEL = "Free Balance"

# Google Sheet name (must already exist)
GOOGLE_SHEET_NAME = "Daily Account Balances"

# Path to Google Service Account credentials (DO NOT COMMIT THIS FILE)
GOOGLE_CREDENTIALS_FILE = "google-credentials.json"

# Page load delay (seconds)
PAGE_LOAD_DELAY = 3

# ======================================================
# DATE & TIME
# ======================================================

now = datetime.now()
current_date = now.strftime("%d-%m-%Y")
current_time = now.strftime("%H-%M")

# ======================================================
# GOOGLE SHEETS AUTH
# ======================================================

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    GOOGLE_CREDENTIALS_FILE,
    scope
)
client = gspread.authorize(credentials)
sheet = client.open(GOOGLE_SHEET_NAME).sheet1

# Add header row if sheet is empty
if not sheet.get_all_values():
    sheet.append_row([
        "Date",
        "Time",
        "Account Address",
        "Balance"
    ])

# ======================================================
# SELENIUM SETUP (HEADLESS)
# ======================================================

options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)

# ======================================================
# MAIN LOOP
# ======================================================

for address in ADDRESSES:
    url = EXPLORER_ACCOUNT_URL.format(address=address)
    driver.get(url)
    time.sleep(PAGE_LOAD_DELAY)

    try:
        dt_elements = driver.find_elements(By.TAG_NAME, "dt")
        dd_elements = driver.find_elements(By.TAG_NAME, "dd")

        balance_value = None

        for dt, dd in zip(dt_elements, dd_elements):
            if dt.text.strip() == BALANCE_LABEL:
                balance_value = dd.text.strip()
                break

        if balance_value:
            print(f"[OK] {address}: {balance_value}")
            sheet.append_row([
                current_date,
                current_time,
                address,
                balance_value
            ])
        else:
            print(f"[NOT FOUND] Balance not found for {address}")
            sheet.append_row([
                current_date,
                current_time,
                address,
                "Not found"
            ])

    except Exception as error:
        print(f"[ERROR] {address}: {error}")
        sheet.append_row([
            current_date,
            current_time,
            address,
            "Error"
        ])

driver.quit()
print("All balances successfully written to Google Sheets.")
