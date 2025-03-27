# Scraper for Live Streamers in Gambling Category

## Overview
This project is a web scraper that extracts live streamers from the Gambling category on Kick.com. It gathers details such as language, username, and social media links. The extracted data is saved in an Excel file for further analysis.

## Features
- Scrapes live streamers in the Gambling category.
- Extracts emails and Telegram links from bios.
- Saves the collected data in an Excel file.
- Can be easily modified to scrape different streaming categories by changing the URL.

## Requirements
- Python 3.10
- SeleniumBase
- Pandas

## Installation
1. Clone the repository:
```bash
   git clone https://github.com/your-repo/streamer-scraper.git
   cd streamer-scraper
```

2. Install dependencies:
```bash
   pip install seleniumbase pandas
```

3. Run the scraper:
```bash
   python scraper.py
```

## How It Works
- The script uses `SeleniumBase` to navigate and extract page content.
- Parses JSON data embedded in the webpage.
- Extracts streamers' details, including their social media links.
- Saves the extracted data into an Excel file named `output.xlsx`.

## Customization
To change the scraped category, modify the `BASE_URL` parameter in `scraper.py`. Replace `Gambling` with any other desired category." 

## License
This project is open-source and available under the MIT License.
