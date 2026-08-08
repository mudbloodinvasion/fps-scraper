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
8. 
