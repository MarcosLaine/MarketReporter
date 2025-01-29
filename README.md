# Market Reporter 📈

A Python script that automatically generates and sends daily market reports via email and pushover. The report includes charts of various market indices and is scheduled to run automatically at market close.

## Features 🌟

- Automatically fetches data for IBOVESPA, DOLAR, S&P500, BTC, EURO, and NASDAQ
- Generates visual charts of market performance
- Sends automated email reports to configured recipients
- Sends automated pushover notifications to configured recipients
- Can be scheduled to run daily using Windows Task Scheduler
- Secure configuration management for sensitive data

## Prerequisites 📋

Before running the script, make sure you have:

- Python 3.x installed
- Anaconda or required Python packages
- A Gmail account with App Password configured
- Pushover account with user key and API token
- Windows OS (for Task Scheduler functionality)

### Required Python Packages

```bash
pip install yfinance pandas matplotlib email
```

## Configuration ⚙️

1. Create a `config.json` file in the `cfg` directory using the following template:

```json
{
    "email": {
        "sender": "your_email@gmail.com",
        "password": "your_app_password",
        "recipients": [
            "recipient1@email.com",
            "recipient2@email.com"
        ],
        "name": "Your Name"
    },
    "smtp": {
        "server": "smtp.gmail.com",
        "port": 587
    },
    "pushover": {
        "user_key": "your_pushover_user_key",
        "api_token": "your_pushover_api_token"
    }
}
```

### Gmail App Password Setup

1. Go to your Google Account settings
2. Navigate to Security
3. Enable 2-Step Verification if not already enabled
4. Generate an App Password:
   - Select 'App Passwords' under 2-Step Verification
   - Choose 'Mail' and your device
   - Use the generated password in your `config.json`

### Pushover Setup

1. Create an account on [Pushover](https://pushover.net/).
2. Create a new application to get your `User Key` and `API Token`.
3. Use these credentials in your `config.json` under the `pushover` section.

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/MarcosLaine/MarketReporter.git
cd MarketReporter
```

2. Create and configure your `config.json` file in the `cfg` directory as shown above

3. Test the script:
```bash
python src/MarketReporter.py
```

## Scheduling Daily Execution ⏰

### Using Windows Task Scheduler

1. Open Task Scheduler
2. Click "Create Basic Task"
3. Set a name (e.g., "Market Reporter")
4. Choose "Daily" trigger
5. Set the start time (recommended: after market close)
6. In "Action", choose "Start a Program"
7. Program/script: `C:\Path\To\Python\python.exe`
8. Add arguments: `"C:\Path\To\Your\src\MarketReporter.py"`
9. Set "Start in": `C:\Path\To\Your\Script\Directory`

### Important Task Scheduler Settings

- Run with highest privileges
- Configure for Windows 10/11
- Set the correct working directory

## Project Structure 📁

```
market-reporter/
│
├── cfg/
│   └── config.json           # Configuration file (not in repo)
│   └── config.example.json    # Example configuration template
│
├── img/                      # Directory for output images
│   ├── btc.png
│   ├── dolar.png
│   ├── euro.png
│   ├── ibovespa.png
│   ├── nasdaq.png
│   └── sp500.png
│
├── src/
│   └── MarketReporter.py     # Main script
│
├── .gitignore                # Git ignore file
└── README.md                 # This file
```

## Troubleshooting 🔧

### Common Issues

1. **Permission Errors**
   - Ensure Task Scheduler is running with appropriate privileges
   - Check file paths and permissions

2. **Email Sending Fails**
   - Verify Gmail App Password is correct
   - Check internet connection
   - Confirm SMTP settings

3. **Script Not Running**
   - Verify Python path in Task Scheduler
   - Check working directory configuration
   - Review Task Scheduler logs


## Security Notes 🔒

- Never commit `config.json` to version control
- Keep your App Password secure
- Regularly update your credentials
- Use the `.gitignore` file to prevent sensitive data from being tracked

## Contributing 🤝

Feel free to fork this project and submit pull requests with improvements. Please ensure you follow the existing code style and add appropriate tests for new features.

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Author ✨

[Marcos Paulo](https://github.com/MarcosLaine)

---

For questions or support, please open an issue in the GitHub repository or contact me at marcospslaine@gmail.com.