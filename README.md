# Crypto-WebScraper
Simple Crypto Web Scraper with python beautifulsoup and selenium


# Crypto Wallet Checker

The Crypto Wallet Checker is a Python script designed to check the wallet balances and transaction history of various cryptocurrencies. It utilizes web scraping and automation techniques to retrieve data from cryptocurrency tracking websites.

## Prerequisites

Before running the script, make sure you have the following dependencies installed:

- Python 3.x
- Beautiful Soup 4 (`beautifulsoup4`)
- Requests (`requests`)
- ConfigParser (`configparser`)
- Selenium (`selenium`)
- Webdriver Manager (`webdriver_manager`)
- NumPy (`numpy`)
- Playwright (`playwright`)

You can install these dependencies using pip:

```bash
pip install beautifulsoup4 requests configparser selenium webdriver_manager numpy playwright
```

Additionally, you will need the Chrome browser installed on your system, as the script uses the ChromeDriver for automation.

## Usage

1. Copy the provided code into a Python script file (e.g., `wallet_checker.py`).

2. Open the terminal or command prompt and navigate to the directory where the script is located.

3. Run the script using the following command:

   ```bash
   python wallet_checker.py
   ```

   The script will start executing and display progress and status messages in the console.

4. The script will scrape data from the "Gainers & Losers" page of the Coincarp website (`https://www.coincarp.com/gainers-losers/`). It will retrieve the names of the top gainers' cryptocurrencies.

5. For each cryptocurrency, the script will check if there is a corresponding image with a specified class attribute (defined in the `SCOPE_CHAINS` variable). If the image exists, the script will proceed to check the wallet balances and transaction history.

6. To check wallet balances, the script will open the Coincarp website page for each cryptocurrency and extract the wallet addresses. It will then filter the addresses based on specified conditions (wallet balance percentage), and store the resulting wallet list.

7. Finally, the script will write the resulting wallet list to a configuration file (`config.conf`) under the section `TRACKED_WALLET`.

## Configuration

The script allows for customization through a configuration file (`config.cfg`). However, parts of the code related to the configuration are currently commented out.

To configure the script:

1. Rename `config.cfg.example` to `config.cfg`.

2. Open `config.cfg` in a text editor and modify the values as needed.

   - `SCOPE_CHAINS`: The class attribute value of the image element used to determine whether to check the wallet balances and history.

   - `AMOUNT_CHECKER`: (currently commented out) Set to `1` to enable checking the minimum amount in wallets, or `0` to disable.

   - `AMOUNT_VALUE`: (currently commented out) The minimum wallet balance value (in the respective cryptocurrency) to check if `AMOUNT_CHECKER` is enabled.

   - `TRADE_CHECKER`: (currently commented out) Set to `1` to enable checking the number of trades, or `0` to disable.

   - `TRADE_VALUE`: (currently commented out) The minimum number of trades to check if `TRADE_CHECKER` is enabled.

3. Save the `config.cfg` file.

## Output

The script will write the resulting wallet list to the configuration file `config.conf` under the section `TRACKED_WALLET`.

Make sure to read and parse the `config.conf` file in your other scripts to access the tracked wallets.

Note: The script is provided as a starting point and may require modifications to work with the latest website structure or additional error handling.

## Disclaimer

This script was created for educational purposes and to demonstrate web scraping techniques. Use it responsibly and in accordance with the terms and conditions

 of the websites you are scraping. Be aware that scraping websites without permission may be against their terms of service and could potentially lead to legal issues.
