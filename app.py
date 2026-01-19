import os
import re
import threading
import webbrowser
import requests
from flask import Flask, request, render_template

# Ensure Flask can find the templates folder even in .exe
base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, "templates")

app = Flask(__name__, template_folder=template_dir)

def is_valid_ip_or_domain(value):
    ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}$"
    domain_pattern = r"^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"
    return re.match(ip_pattern, value) or re.match(domain_pattern, value)

@app.route("/", methods=["GET", "POST"])
def index():
    ip_data = None
    error = None

    if request.method == "POST":
        ip = request.form.get("ip")

        if not ip:
            ip = request.remote_addr

        if not is_valid_ip_or_domain(ip):
            error = "❌ Invalid IP or domain."
        else:
            try:
                response = requests.get(f"http://ip-api.com/json/{ip}")
                data = response.json()

                if data.get("status") == "success":
                    ip_data = data
                else:
                    error = "⚠️ Could not fetch data. Try a different IP."
            except Exception as e:
                error = f"🚫 Error: {str(e)}"

    return render_template("index.html", ip_data=ip_data or {}, error=error)

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(debug=False)


