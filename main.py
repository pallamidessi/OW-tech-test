from flask import Flask, jsonify
from dataclasses import dataclass, field, asdict
from typing import Optional

from requests.exceptions import HTTPError
from usage import compute_message_cost
from clients import get_report, get_current_billing_period

app = Flask(__name__)

# data class to model the response and provide some type safety
@dataclass
class MessageUsage:
    message_id: int
    timestamp: str
    credit_used: int
    report_name: Optional[str] = field(default=None)  # This field is optional

    def to_dict(self):
        # Convert to a dictionary, omitting keys with None values
        return {k: v for k, v in asdict(self).items() if v is not None}


@app.route("/")
def hello_world():
    return jsonify({"message": "Hello, Flask!"})


@app.route("/usage")
def usage():
    resp = get_current_billing_period()

    usage_response = {"usage": []}
    for message in resp["messages"]:
        message_id = message["id"]
        message_usage = MessageUsage(
            message_id=message_id, timestamp=message["timestamp"], credit_used=0
        )

        # We check if a report exist AND if it can be found
        # move to the next message: else we compute the message usage cost
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
                    print(f"No report id: {report_id} found for message: {message_id}")

        message_usage.credit_used = compute_message_cost(message["text"])
        usage_response["usage"].append(message_usage.to_dict())
    return jsonify(usage_response)


if __name__ == "__main__":
    app.run(debug=True)
