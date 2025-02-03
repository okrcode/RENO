# RENO
This Python script automates the process of querying and retrieving individual CURP (Clave Única de Registro de Población) data from the RENAPO (Registro Nacional de Población) service in Mexico. The script handles CAPTCHAs, manages cookies, and processes multiple CURPs efficiently.
RENAPO CURP Data Scraper
This Python script automates the process of querying and retrieving individual CURP (Clave Única de Registro de Población) data from the RENAPO (Registro Nacional de Población) service in Mexico. The script handles CAPTCHAs, manages cookies, and processes multiple CURPs efficiently.

# Features:
CAPTCHA Solving: Uses the TwoCaptcha service to solve reCAPTCHA challenges automatically.
Cookie Management: Retrieves and manages session cookies with undetected_chromedriver to avoid bot detection.
API Request Handling: Sends POST requests to RENAPO API with appropriate headers and cookies, and retries on failure.
Data Parsing: Extracts personal information such as name, gender, birth date, and registration details from the RENAPO API response.
Batch Processing: Reads CURP identifiers from a text file, retrieves data for each, and outputs the results to a CSV file.

# Requirements:
Python 3.x
undetected_chromedriver
requests
twocaptcha
csv
# Usage:
Ensure that the necessary Python packages are installed.
Provide a text file with CURP identifiers.
Run the script to fetch and save the CURP data.
