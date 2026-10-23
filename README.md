# Aqua-Net Redesigned Streamlit Prototype

A redesigned, multi-role product demo inspired by the three UI reference screenshots.

## Experience modes
- Government dashboard: overview, borehole registry, verification queue, repair management, groundwater trends.
- Community app: home, explore boreholes, report an issue, contributions.
- Aqua Fellow: field dashboard, log a reading, reading history.
- Basic phone access: USSD, SMS and voice-flow simulators.

## Run locally
Python 3.10+ recommended.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Important limitations
All records, metrics, locations and readings are illustrative. No live South African government dataset, SMS/USSD/voice service, sensor, or persistent database is connected. Session changes are temporary. National figures shown in the government dashboard are placeholders based on the visual reference and must not be presented as factual statistics.

## Deploy
Push the folder to GitHub and deploy with Streamlit Community Cloud, or another Python host. Do not commit real personal data, API keys or unapproved water-point coordinates.
