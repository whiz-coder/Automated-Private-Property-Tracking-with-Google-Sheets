# Automated-Private-Property-Tracking-with-Google-Sheets

The goal of the project is to extract information from private property listings and upload the data to a Google Sheets document. The project is deployed on an AWS EC2 machine with cron jobs set up to run the script once every day.

The code performs the following steps:

-Imports the necessary libraries, including requests, BeautifulSoup, gspread, smtplib, and others.
-Defines the URL of the website to scrape for property information.
-Uses the check_page() function to fetch the initial page and extract the URLs of the property listings.
-The check_priv() function filters out the private listings from the extracted URLs.
-For each private listing, the check_sheet() function checks if the listing is already present in the Google Sheets document.
-If the listing is not in the Google Sheets, the update_sheet() function adds the listing details, such as the title, link, and date, to the sheet.
-The send_email() function sends an email notification with the link to the newly found private listing.
-The script executes the check_page(), check_priv(), and email functions.
-The script outputs the start and end times of its execution.

In summary, this project uses web scraping with BeautifulSoup to extract private property listings, stores the data in a Google Sheets document, and sends email notifications for new listings. It provides a basic infrastructure for automating the extraction and tracking of private property information.
