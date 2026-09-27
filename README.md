# Selenium E-Commerce Automation using Python

## Project Overview

This project automates an end-to-end e-commerce purchase flow using Selenium WebDriver with Python and PyTest.

The automation is implemented on the TutorialsNinja demo e-commerce application.

## Business Flow

The automated test performs the following operations:

1. Launch the Chrome browser
2. Open the e-commerce application
3. Register a new customer account
4. Logout
5. Login using the registered credentials
6. Search for a product
7. Open the product
8. Add the product to the shopping cart
9. Navigate to the shopping cart
10. Verify the product
11. Update the quantity
12. Verify the updated quantity
13. Capture screenshots
14. Generate an HTML execution report

## Technologies Used

- Python
- Selenium WebDriver
- PyTest
- pytest-html
- JSON
- Google Chrome
- Git & GitHub

## Project Structure

```text
SeleniumEcommerceAutomation/
│
├── test_data/
│   └── test_data.json
│
├── screenshots/
│   └── Execution screenshots
│
├── reports/
│   └── execution_report.html
│
├── test_ecommerce.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Application Under Test

TutorialsNinja Demo E-Commerce Application

https://tutorialsninja.com/demo/

## Author

Adrija