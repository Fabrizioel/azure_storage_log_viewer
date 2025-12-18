# Azure Log Viewer

Azure Log Viewer is a terminal-based Textual application for browsing Azure File Share
directories and analyzing `.log` files within a user-defined date range.

The tool is designed for internal operational use, providing a fast and interactive way
to inspect log activity without leaving the terminal.

---

## Features

- Interactive TUI built with Textual
- Azure File Share directory navigation
- Date range filtering for log analysis
- Asynchronous log processing (non-blocking UI)
- Aggregated reporting of log activity

---

## Requirements

- Python 3.12 or higher
- Access to the target Azure File Share
- Azure storage account credentials

---

## Installation

### Using [uv](https://docs.astral.sh/uv/getting-started/installation/) (recommended) on MacOS, Linux, and Windows.

```bash
uv tool install git+https://github.com/Fabrizioel/azure_storage_log_viewer.git
```

---

## Usage

### Run the application from any terminal:

```bash
azure-log-viewer
```

The application will prompt for credentials, then present an interactive interface for directory browsing and log analysis.

---

## Development

### Clone the repository and install in editable mode:
```bash
pip install -e .
python -m azure_log_viewer
```