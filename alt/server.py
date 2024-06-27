import http.server
import socketserver
import urllib.parse
import requests
from datetime import datetime, timedelta, timezone
import os

# Import the API key from config.py
from config import NVD_API_KEY

PORT = 8000

def fetch_cves_for_keyword(keyword):
    nvd_api_url = 'https://services.nvd.nist.gov/rest/json/cves/2.0'

    # Get the API key from the config file
    api_key = NVD_API_KEY

    # Get the date range for the past month
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=30)

    # Format dates in the required format
    start_date_str = start_date.isoformat().replace('+00:00', 'Z')
    end_date_str = end_date.isoformat().replace('+00:00', 'Z')

    # Parameters for the API request
    params = {
        'pubStartDate': start_date_str,
        'pubEndDate': end_date_str,
        'keywordSearch': keyword,
        'resultsPerPage': 20
    }

    headers = {
        'apiKey': api_key
    }

    try:
        # Send a GET request to the NVD API
        response = requests.get(nvd_api_url, params=params, headers=headers)

        # Log the response content and status for debugging
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        print(f"Response Content: {response.content.decode('utf-8')}")

        # Check for HTTP errors
        response.raise_for_status()

        # Parse the JSON response
        try:
            data = response.json()
            print("API Response Data:", data)  # Additional debugging output
            cves = data.get('vulnerabilities', [])
            return [{'id': cve.get('cve', {}).get('id'),
                     'description': cve.get('cve', {}).get('descriptions', [{}])[0].get('value')}
                    for cve in cves]
        except ValueError:
            print("Failed to decode JSON response")
            return []

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return []

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/fetch_cves':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            keyword = post_data.get('keyword', [''])[0]

            cves = fetch_cves_for_keyword(keyword)
            cve_list = "<ul>"
            for cve in cves:
                cve_list += f"<li><strong>{cve['id']}</strong>: {cve['description']}</li>"
            cve_list += "</ul>" if cves else "<p>No CVEs found for the given keyword.</p>"

            response_content = f"""
            <html>
                <head>
                    <title>Fetch CVEs</title>
                    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
                </head>
                <body>
                    <div class="container">
                        <h1 class="mt-5">Fetch Recent CVEs</h1>
                        <form action="/fetch_cves" method="post" class="mt-3">
                            <div class="form-group">
                                <label for="keyword">Keyword (Vendor, Product, or CVE Name)</label>
                                <input type="text" class="form-control" id="keyword" name="keyword" required>
                            </div>
                            <button type="submit" class="btn btn-primary">Fetch CVEs</button>
                        </form>
                        <hr>
                        <div id="results">
                            {cve_list}
                        </div>
                    </div>
                    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
                    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.2/dist/umd/popper.min.js"></script>
                    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
                </body>
            </html>
            """

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(response_content.encode('utf-8'))

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
