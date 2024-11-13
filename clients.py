import requests
from requests import RequestException, HTTPError

# We do a little bit of error handling here to provide contexts about the error
# Those "client" are kept simple, with little logic other than providing the parsed
# json responses
def get_current_billing_period():
    url = "https://owpublic.blob.core.windows.net/tech-task/messages/current-period"

    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        json_data = response.json()
        return json_data
    except HTTPError as http_error:
        print(f"Failed to get data. Status code: {http_error.response.status_code}")
        raise http_error
    except RequestException as e:
        print(f"Failed to get data. Issue with the request: {e}")
        raise e


def get_report(report_id: str):
    url = f"https://owpublic.blob.core.windows.net/tech-task/reports/{report_id}"

    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        json_data = response.json()
        print("succesfully fetched data")
        return json_data
    except HTTPError as http_error:
        print(f"Failed to get data. Status code: {http_error.response.status_code}")
        raise http_error
    except RequestException as e:
        print(f"Failed to get data. Issue with the request: {e}")
        raise e
