# OW tech-test

This is a simple implementation for the OW (tech test)[https://orbitalwitness.notion.site/Backend-Engineering-Task-1281572580cc80fc9152f1c3c076cd30].

### Implementation

I went with a tiny Flask app to make this short and readable and not really too much on framework magic. We make use of pytest for test and requests for
calling the 3rd party API. A Makefile and Dockerfile are provided to allow to run and test this project quickly.

We have a flat structure here due to how simple the project is:
* `usage.py` contains the the '/usage' business logic
* `main.py` with the routes and handler
* `client.py` the basic client, with a little bit of error handling
* `tests/` contains the tests

### Design decision

The code is quite basic: this is because I didn't wanted to over-engineered it and because we want to keep the implementation as lean as possible.
With real usage and time, we might decide to change and refactor how thing are done but here we go for simplicity and correctness: this is why we have tests at different level
(unit tests and testing the full endpoint with mocking). We are doing the computation in a way that is not the most efficient but is simple to read, maintains and extend.

This lack better error handling, retries, any observability (logs, metrics, tracing), proper documentation

### Running

If you have docker installed, you should be able to just:
```
make run
```
and then query with

```
curl http://127.0.0.1:5000/usage
```


