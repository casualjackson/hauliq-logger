import streamlit as st
from datetime import datetime
import gspread
import json
from google.oauth2.service_account import Credentials

# Google Sheets setup
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from Streamlit Secrets
creds_dict = json.loads(st.secrets["GOOGLE_CREDS"])
creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
client = gspread.authorize(creds)
sheet = client.open_by_key("1d_Yqn0ZANSeGIvtNKXBivFPoj-Av5wcJJW13z8CcHW8").worksheet("Data")

# Streamlit form
st.set_page_config(page_title="HaulIQ Trip Logger", layout="centered")
st.title("🚚 HaulIQ Trip Logger")

with st.form("log_form"):
    truck_id = st.text_input("Truck ID")
    shift_id = st.text_input("Shift ID")
    trip_type = st.text_input("Trip Type")
    from_location = st.text_input("From Location")
    to_location = st.text_input("To Location")
    loader_id = st.text_input("Loading Unit")
    notes = st.text_input("Notes (optional)")

    submitted = st.form_submit_button("✅ Submit Trip")

    if submitted:
        now = datetime.now()
        date_str = now.strftime("%d/%m/%y")
        time_str = now.strftime("%H:%M")

        row = [
            date_str,           # Date
            time_str,           # Timestamp
            shift_id,
            from_location,
            to_location,
            loader_id,
            trip_type,
            "", "", "",         # travel/queue/loading time
            notes
        ]

        sheet.insert_row(row, index=2)  # Insert under headers
        st.success(f"Trip logged at {date_str} {time_str}")
