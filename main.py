from flask import Flask, request, jsonify
import os
import fitz  # PyMuPDF
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

PDF_DIR = 'pdfs'
pdf_texts = []

def extract_text_from_pdfs():
    global pdf_texts
    for filename in os.listdir(PDF_DIR):
        if filename.endswith('.pdf'):
            doc = fitz.open(os.path.join(PDF_DIR, filename))
            full_text = "\n".join(page.get_text() for page in doc)
            pdf_texts.append((filename, full_text.lower()))

SCOPES = ['https://spreadsheets.google.com/feeds',
          'https://www.googleapis.com/auth/drive']
CREDS_FILE = 'creds.json'
SHEET_NAME = 'Product Team Westinghouse Issues Log'

def append_to_sheet(data):
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1
    sheet.append_row([data.get("query"), data.get("description"), data.get("email")])

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query', '').lower()
    matches = []
    for filename, text in pdf_texts:
        if query in text:
            snippet_start = text.find(query)
            snippet = text[snippet_start:snippet_start+300]
            matches.append({"source": filename, "snippet": snippet})
    return jsonify({"results": matches})

@app.route('/log_issue', methods=['POST'])
def log_issue():
    data = request.json
    append_to_sheet(data)
    return jsonify({"status": "logged"})

extract_text_from_pdfs()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
