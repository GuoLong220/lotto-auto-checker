# Lotto Auto Checker

A Python-based automation tool for automatically checking Taiwan Lottery results and sending notifications to a designated Line group. The system is deployed on Ubuntu and uses Crontab for scheduling.

## Features
- Automatically fetches Taiwan Lottery results.
- Notifies users of results via Line Bot.
- Supports scheduled tasks using Crontab.
- Customizable settings for lottery numbers and Line group integration.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/lotto-auto-checker.git
   cd lotto-auto-checker
   ```

2.	Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.	Configure environment variables:
Create a .env file in the root directory with the following variables:
    ```env
    line_group_id=<Your Line Group ID>
    line_bot_access_token=<Your Line Bot Access Token>
    os_path=<Path to the project directory>
    my_number=<Your Lottery Numbers>
    ```

---
## Usage
1.	Run the script manually for testing:
    ```bash
    python main.py
    ```

2. Set up Crontab for scheduled execution:
    * Edit your Crontab configuration:
    ```bash
    crontab -e
    ```
    * Add the following line to schedule the script:
    ```bash
    00-55/5 20-23 * * 2,5 python3 main.py  >> crontlog.txt 2>&1
    ```

---

## Project Structure
```bash
lotto-auto-checker/
├── main.py               # Main script
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not included in the repository)
└── README.md             # Project documentation
```

---

## Requirements
* Python 3.7+
* A valid Line Bot token and group ID
* Ubuntu (for Crontab setup)
