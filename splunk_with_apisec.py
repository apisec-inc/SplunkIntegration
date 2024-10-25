import requests
import json
import os
import logging
from datetime import datetime, timedelta


# Load config
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, "r") as config_file:
    config = json.load(config_file)


# Function to retrieve bearer token by logging in
def get_bearer_token():
    login_url = "https://cloud.apisec.ai/auth/login"
    credentials = {
        "username": config['auth']['username'],
        "password": config['auth']['password']
    }
    
    response = requests.post(login_url, json=credentials)
    
    if response.status_code == 200:
        token = response.json().get('token')
        if token:
            return token
        else:
            logging.error("Bearer token not found in the response.")
            return None
    else:
        logging.error(f"Failed to retrieve bearer token: {response.status_code} - {response.text}")
        return None

# Get the bearer token
BEARER_TOKEN = get_bearer_token()
# API base URL and Authorization from config
API_BASE_URL = "https://cloud.apisec.ai/api/v1"

# Common function to make API requests
def fetch_data(api_endpoint, params=None):
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{API_BASE_URL}/{api_endpoint}", headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Error fetching {api_endpoint}: {response.status_code} - {response.text}")
        return None

# Function to handle paginated requests using totalPages from response
def fetch_paginated_data(api_endpoint, params=None, pageSize=20):
    page = 0
    results = []
    total_pages = None

    while total_pages is None or page < total_pages:
        # Add pagination to the params
        if params is None:
            params = {}
        params['pageSize'] = pageSize
        params['page'] = page

        # Fetch the data for the current page
        data = fetch_data(api_endpoint, params)

        if not data:
            break

        # Add the data to results
        results.append(data)

        # Get totalPages from the first response
        if total_pages is None:
            total_pages = data.get("totalPages", 1)  # Default to 1 page if not available
            total_elements = data.get("totalElements", 0)  # Just for logging or tracking

        logging.info(f"Page {page} fetched {len(data)} records. Total pages: {total_pages}, Total elements: {total_elements}")

        # Increment page number to fetch the next page
        page += 1

    return results

# Function to calculate date range (yesterday as start and end date)
def get_yesterday_date_range():
    yesterday = datetime.now() - timedelta(days=1)
    start_date = yesterday.strftime('%Y-%m-%d')
    end_date = yesterday.strftime('%Y-%m-%d')
    return start_date, end_date

# Function for fetching user activity logs
def fetch_user_activity_logs():
    if config['user_activity_logs']['enabled']:
        # Automatically calculate the startDate and endDate
        start_date, end_date = get_yesterday_date_range()

        # Fetch user activity logs with dynamic date range
        params = {
            "startDate": start_date,
            "endDate": end_date
        }
        paginated_data = fetch_paginated_data("user-activity-logs", params)
        if paginated_data:
            print(json.dumps(paginated_data))  # Indexed as 'user_activity_logs'

# Function for fetching login activity logs
def fetch_login_activity_logs():
    if config['login_activity_logs']['enabled']:
        # Automatically calculate the startDate and endDate
        start_date, end_date = get_yesterday_date_range()

        # Fetch login activity logs with dynamic date range
        params = {
            "startDate": start_date,
            "endDate": end_date
        }
        paginated_data = fetch_paginated_data("login-activity-logs", params)
        if paginated_data:
            print(json.dumps(paginated_data))  # Indexed as 'login_activity_logs'

# Function for fetching system activity logs
def fetch_system_activity_logs():
    if config['system_activity_logs']['enabled']:
        # Automatically calculate the startDate and endDate
        start_date, end_date = get_yesterday_date_range()

        # Fetch system activity logs with dynamic date range
        params = {
            "startDate": start_date,
            "endDate": end_date
        }
        paginated_data = fetch_paginated_data("system-activity-logs", params)
        if paginated_data:
            print(json.dumps(paginated_data))  # Indexed as 'system_activity_logs'

if __name__ == "__main__":
    # Fetch logs based on config
    fetch_user_activity_logs()
    fetch_login_activity_logs()
    fetch_system_activity_logs()
