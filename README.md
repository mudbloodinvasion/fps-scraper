# **Goa FPS scraper**
## What the project does ?
FPS scraper is an automated website scraping pipeline using selenium that extracts Fair Price Shop sale transactions from the IMDPS portal . The extracted data includes transaction summaries, authentication information, ration-card transactions, and commodity-wise distributed quantities. After extraction of all the required transactions , scraped data is first stored as separate JSON files for each month and district then this pipeline consolidates all the data into one csv format file.
## Website 
https://impds.nic.in/sale/

## Features
1. Automated navigation through the IMPDS website.
2. Supports multiple months and districts using loops.
3. Extracts commodity-wise distributed quantities and tables.
4. The consolidated data is cleaned and normalized and all the nested tables are converted to coloumns
5. All the steps are logged so that any error can be tracked and tackled 
6. Since the site is a dynamic site , which gets slower as number of requests increases , browser gets shut after every 40 shops and restarts  maintaining the extraction speed
7. Every 10 shop is saved after extraction in order to not lose the work done. Hence preventing loss of data and maintaining stability 
8.If a shop fails due to a Selenium/browser/navigation error, the browser is restarted and the scraper resumes from the failed shop not from beginning
9. Detects all newly loaded fps items that were not present earlier
10. To improve synchronization , explicit waits are used for loaders and clickable buttons
11. Fps id authentication used to avoid wrong extraction.

## Limitations

The scraper depends on the current structure of the IMPDS website. Changes to HTML elements, CSS classes, IDs, JavaScript functions, or page navigation may require changes to the Selenium selectors.

If a required table fails to load or contains unexpected data, the corresponding fields may be missing or represented as zero during consolidation.

May require modification if more states and months are needed.

## Structure

```text
FPSscrape/
├── data/
│   ├── raw/
│   │   ├── march_north_goa.json
│   │   ├── march_south_goa.json
│   │   ├── april_north_goa.json
│   │   └── april_south_goa.json
│   └── processed/
│       ├── fps_combined.csv
│       └── final_dataset.csv
├── logs/
│   └── scraper.log
├── get_raw_data.py
├── consolidate_data.py
├── finaldataset.py
├── requirements.txt
└── README.md
```

Has three code files. one for scraping , one for consolidating all json files and one for cleaning the consolidated data 

## Installation 
### 1. Clone the repository

git clone https://github.com/mudbloodinvasion/fps-scraper.git

cd fps-scraper

### 2. Create a virtual environment

python -m venv venv

### 3. Activate the virtual environment

Windows:

venv\Scripts\activate

### 4. Install dependencies

pip install -r requirements.txt
