# Liseo Dashboard Live
Live dashboard for Liseo production data (Excel workbook -> dashboard_data.json -> GitHub Pages).

- `index.html` is the dashboard; it re-checks `dashboard_data.json` every 60 seconds.
- `scripts/refresh_dashboard_data.py` reads the "Production Data" sheet (auto-detects the workbook, or pass its path) and rewrites the JSON.
- `scripts/publish_dashboard_data.py` refreshes the JSON and pushes it when the data changed.
- `scripts/register_local_autopublish.ps1` creates a Windows scheduled task that publishes every minute.
