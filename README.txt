# CVE Fetcher

This project is a simple web application that fetches and displays recent Common Vulnerabilities and Exposures (CVEs) based on a keyword search. The application uses the NVD API to retrieve CVEs and presents them in a user-friendly format using Bootstrap.

## Project Structure

cveScript/
├── app.py
├── config.py
├── index.html
└── README.md


- `app.py`: The main server script that handles HTTP requests, interacts with the NVD API, and serves the HTML content.
- `index.html`: The HTML file that serves as the front-end for the application.
- `config.py`: A configuration file that contains the API key for accessing the NVD API: https://nvd.nist.gov/developers/request-an-api-key
- `README.md`: This file, providing information about the project.

## Requirements

- Python 3.x
- `requests` library for Python

## Installation

1. **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd cveScript
    ```

2. **Install the required Python packages**:
    ```bash
    pip3 install requests
    ```

3. **Create the `config.py` file**:
    In the root directory (`cveScript`), create a `config.py` file and add your NVD API key:
    ```python
    # config.py
    NVD_API_KEY = 'your_api_key_here'
    ```

## Running the Application

1. **Run the server**:
    ```bash
    python3 app.py
    ```

2. **Open your web browser** and navigate to `http://127.0.0.1:8000/`.

## Usage

1. **Enter a keyword** (e.g., "Cisco", "Microsoft", or "CVE-2024-1234") in the search bar.
2. **Click the "Fetch CVEs" button**.
3. **View the results**: The CVEs related to the keyword will be displayed on the page in a formatted card layout, results are within last month.

## Troubleshooting

### ModuleNotFoundError: No module named 'config'

If you encounter this error, ensure that:
- The `config.py` file exists in the root directory.
- The `NVD_API_KEY` variable is correctly defined in `config.py`.

### API Key Issues

If the application fails to fetch CVEs due to API key issues:
- Verify that the API key in `config.py` is correct.
- Ensure that your API key has not expired or been invalidated.