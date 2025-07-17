# Example `ex06`: Daily Weather Report (PDF)

This example demonstrates a `Airflow DAG` that:
- Fetches current weather data from a public API: http://api.openweathermap.org/
- Generates a `PDF` report using `reportlab`
- Stores the report in `/tmp/weather_reports` inside the `Airflow worker container`.