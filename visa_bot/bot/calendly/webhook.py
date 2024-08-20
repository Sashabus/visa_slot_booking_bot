from flask import Flask, request

app = Flask(__name__)


@app.route('/calendly-webhook', methods=['POST'])
def calendly_webhook():
    event_data = request.json
    # Process the Calendly event data here
    return '', 200


if __name__ == "__main__":
    app.run(port=5000)
