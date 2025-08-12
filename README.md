# Goodog Streamlit App 🐕

A Streamlit dashboard for payroll and client summaries from monthly activity spreadsheets.

## Local development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Usage
- Upload an `.xlsx` file from the sidebar
- Choose view: Dog walkers or Clients
- Configure amounts (shift compensation, monthly pass, ticket price)
- Download a CSV summary from the summary table

## Deploy (Streamlit Community Cloud)
- Push this repo to GitHub
- Create a new Streamlit app targeting `app.py`
- Streamlit Cloud auto-installs from `requirements.txt`

## Notes
- Excel headers are normalized (Hebrew/English supported)
- Large files are cached to speed up re-runs
