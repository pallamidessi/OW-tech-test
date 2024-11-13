from flask import Flask, json
from dataclasses import dataclass, field
from typing import Optional

import requests
from requests import RequestException
from requests.exceptions import HTTPError

app = Flask(__name__)

@dataclass
class MessageUsage:
    message_id: int
    timestamp: str
    credit_used: int
    report_name: Optional[str] = field(default=None)  # This field is optional

@app.route("/")
def hello_world():
    response = app.response_class(
        response=json.dumps({"message": "Hello, Flask!"}),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/usage")
def usage():
    resp = get_current_billing_period()

    usage_response = {"usage": []}
    for message in resp["messages"]:
        message_id = message["id"]
        message_usage = MessageUsage(message_id=message_id, timestamp=message["timestamp"], credit_used=0)
        if "report_id" in message:
            report_id = message["report_id"]
            try:
                resp_report = get_report(report_id)
                message_usage.credit_used = resp_report["credit_cost"]
                message_usage.report_name = report_id
                usage_response["usage"].append(message_usage)
                continue
            except HTTPError as http_error:
                if http_error.response.status_code != 404:
                    raise http_error
                else:
                    print(f"No report {report_id} found for {message_id}")

        message_usage.credit_used = compute_message_cost(message["text"])

        usage_response["usage"].append(message_usage)

    response = app.response_class(
        response=json.dumps(usage_response),
        status=200,
        mimetype='application/json'
    )
    return response


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

def compute_message_cost(text: str):
    base_cost = 100
    cost_palindrome_multiplier = 200
    cost = base_cost

    cost += compute_cost_per_characters(text)
    words = text.split()
    cost += compute_cost_per_words(words)
    cost += compute_unique_words(words)
    cost += compute_cost_third_vowels(text)
    cost += compute_length_penalty(text)
    if is_palindrome(text):
        cost *= cost_palindrome_multiplier

    return cost / 100

def compute_cost_per_characters(text: str):
    cost_per_character = 5
    return len(text) * cost_per_character

def compute_length_penalty(text: str):
    return 500 if len(text) > 100 else 0

def compute_unique_words(words):
    cost_all_unique_words = -200
    words_set = {}
    duplicate_found = False
    for word in words:
        if word in words_set:
            duplicate_found = True
            break
        else:
            words_set[word] = True

    if duplicate_found:
        return 0
    else:
        return cost_all_unique_words

def compute_cost_per_words(words):
    total_cost = 0
    for word in words:
        word_length = len(word)
        if word_length <= 3:
            total_cost += 10
            break
        if word_length <= 7:
            total_cost += 20
            break
        total_cost += 30

    return total_cost

def compute_cost_third_vowels(text):
    text = text.lower()
    vowels = {'a', 'e', 'i', 'o', 'u'}
    total_cost = 0
    for i, character in enumerate(text):
        if i % 3 == 0:
            if character in vowels:
                total_cost += 30

    return total_cost

def is_palindrome(text):
    return text[::-1] == text