from flask import Flask, jsonify
import scraper

app = Flask(__name__)


@app.route("/")
def scrape():
    scraper.parseFiles()
    return jsonify({"status": "scraping complete"})


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=80)
