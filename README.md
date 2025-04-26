# TPDDL_Internship
Website Monitor

Website Monitor is a lightweight tool designed to automatically check the availability and response status of websites. It helps users ensure that their web services are running smoothly and alerts them if any downtime or performance issues are detected.

Features

✅ Monitor one or multiple websites at regular intervals.

✅ Log website response times and HTTP status codes.

✅ Alert (console/email/other integrations) if a site is down or slow.

✅ Configurable check intervals and thresholds.

✅ Minimal, clean codebase for easy deployment and customization.

Tech Stack

Backend: Python

Logging: Excel

Alert System: Email

How It Works

You list the websites you want to monitor.

The system sends periodic HTTP requests to these websites.

It checks the response time and status.

If a site is unreachable, too slow, or returns an error code, an alert is triggered.

Logs are saved for historical performance tracking.

Use Cases

Monitor your personal or professional websites.

Get early warnings for server downtime.

Track website performance metrics over time.

Future Improvements

Dashboard UI to visualize website status.

Retry logic and smart backoff mechanisms.

More advanced alerting options (push notifications, integrations).

Multi-threaded or async support for faster checks.

License

This project is licensed under the MIT License. See the LICENSE file for more information.
