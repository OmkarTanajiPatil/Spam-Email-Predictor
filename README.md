# Mail Spam Check (Django)
A small Django site that wraps the TF‑IDF + Logistic Regression pipeline from the original notebook so you can paste an email body and instantly see whether it looks like spam or ham. The UI is intentionally minimal but polished: a single-page form with live results and confidence scores.

## Features
- Reuses the Scikit-Learn pipeline (TF‑IDF n-grams + Logistic Regression) with caching so the model loads once per process.
- Accepts a CSV dataset (`mail_data.csv`) with `Message` and `Category` columns. If you do not provide one, the app falls back to a tiny in-memory sample so everything still runs.
- Crisp, responsive UI with helpful confidence readouts.
- Automated Django tests to ensure the form renders and returns prediction context.

## Quick start
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Open http://127.0.0.1:8000/ and paste an email body.

## Using your own dataset
1. Place `mail_data.csv` in the project root (`Mail_Spam_Check_ML/`). The file must include at least the columns `Message` and `Category` with values `spam`/`ham` (case-insensitive).
2. Optionally set `MAIL_SPAM_DATA=/path/to/your.csv` before running the server if you store it elsewhere.
3. Restart the dev server; the pipeline will retrain on the new data at startup.

## Tests
```bash
python manage.py test
```
The suite keeps the fall-back model path exercised and ensures the prediction context is wired to the template.

## Project layout
```
Mail_Spam_Check_ML/
├── classifier/          # Django app with forms, views, ml helper, static + templates
├── mailspamsite/        # Project settings and URL routing
├── manage.py
├── model.py             # Thin wrapper for quick CLI demos (reuses classifier.ml)
├── requirements.txt
└── README.md
```
