# Documentation for COVID-19 Testing Data Analysis Program

## Overview
This Python program is designed to fetch and analyze COVID-19 testing data from a public health API. It calculates the total number of PCR tests performed in the United States, the 7-day rolling average of new cases, and identifies the top 10 states with the highest test positivity rates. The program presents these insights in a structured report.

## Assumptions
1. Data Source: The program assumes that the data is available from the API endpoint https://healthdata.gov/resource/j8mb-icvb.json. If this endpoint is modified or becomes unavailable, the program will not function correctly.
  
2. Date Format: Users are expected to input dates in the format YYYY-MM-DD. If the input does not conform to this format, the program will raise an error and terminate.

3. Data Completeness: The program assumes that the data returned from the API is complete and correctly formatted. Any discrepancies in the data may lead to inaccurate calculations.

4. Internet Connectivity: The program requires an active internet connection to fetch data from the API.

5. Data Availability: The program is designed to analyze data available until the specified target date. If there is no data for a particular date or range, the calculations may return zero or default values.

## Features
1. Fetch Testing Data: The program retrieves COVID-19 testing data from the specified API in chunks, processing up to 20,000 records at a time until all relevant data is obtained.

2. Calculate Total PCR Tests: It calculates the total number of PCR tests reported up to a specified date.

3. Calculate 7-Day Rolling Average: The program computes the 7-day rolling average of new COVID-19 cases for the last 30 days leading up to the specified date.

4. Identify Top 10 States by Positivity Rate: It determines the top 10 states with the highest positivity rates based on the available testing data.

5. Generate Report: A comprehensive report is generated summarizing the total PCR tests, rolling averages, and the top states by positivity rate.

## How to Use the Program
1. Run the Program: Execute the program in a Python environment. Ensure that the required libraries (requests, pandas, and datetime) are installed.

2. Input Target Date: When prompted, enter the target date in the format YYYY-MM-DD. This date will be used to filter the testing data.

3. View Results: After the calculations are complete, the program will display a report containing:
   - Total PCR Tests performed up to the target date.
   - 7-Day Rolling Average of New Cases for the last 30 days.
   - Top 10 States with the Highest Positivity Rates.

## Code Structure
The program is structured into several functions, each serving a specific purpose:
- fetch_testing_data(api_url, cutoff_date): Fetches COVID-19 testing data from the API until the specified cutoff date.
- calculate_total_pcr_tests(test_data, cutoff_date): Calculates the total number of PCR tests performed by processing the fetched data.
- calculate_7_day_rolling_average(test_data, cutoff_date): Computes the 7-day rolling average of new COVID-19 cases.
- get_top_positivity_rate_states(test_data, cutoff_date): Identifies the top 10 states with the highest test positivity rates.
- generate_report(test_data, cutoff_date): Compiles the results from the calculations into a report format.
- main(): The main function that orchestrates the execution of the program.

## Example
1. Input: Enter a target date like 2023-10-01.
2. Output: The program will display results similar to:
   Total PCR Tests: 500000
7-Day Rolling Average of New Cases: [50.0, 45.0, 55.0, 60.0]
Top 10 States with Highest Positivity Rate %: [('State A', 15.5), ('State B', 14.2), ...]


## Conclusion
This program is a useful tool for public health officials, researchers, and anyone interested in understanding the trends of COVID-19 testing and positivity rates across different states. It provides valuable insights based on publicly available data, helping to inform decision-making and public health strategies.

---

If you have any additional requests or questions, Feel free to let me know!
