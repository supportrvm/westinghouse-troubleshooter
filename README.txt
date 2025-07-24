# Westinghouse Troubleshooter Backend

## Instructions

1. Upload this folder into a new Replit Python project.
2. Upload your 3 PDF files into the `pdfs/` folder.
3. Upload your `creds.json` Google Service Account key to the root directory.
4. Click the green "Run" button.
5. Your API will run at: https://<your-repl-name>.<username>.repl.co

## Endpoints

- POST `/search`: { "query": "your search terms" }
- POST `/log_issue`: { "query": "...", "description": "...", "email": "..." }
