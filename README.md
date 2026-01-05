# Account Balance Tracker

A generic headless Selenium-based automation tool that retrieves account balances from a blockchain explorer and logs results into Google Sheets.

This project is **explorer-agnostic** and can be adapted to any blockchain or web-based account explorer by updating configuration values.

---

## Features
- Fetches balances from a web-based account explorer
- Supports any explorer using `<dt>` / `<dd>` definition lists
- Runs in headless Chrome (server & VPS friendly)
- Logs data to Google Sheets with timestamp
- Simple configuration, no framework overhead

---

## Requirements
- Python 3.9+
- Google Chrome (or Chromium)
- Google Service Account with Sheets access

---

## Installation

```bash
git clone <repository-url>
cd testnet-token-autoclaim
python -m venv .venv
