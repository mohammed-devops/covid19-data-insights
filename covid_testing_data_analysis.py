import requests
import pandas as pd
from datetime import date, datetime, timedelta
import warnings

# Function to fetch COVID-19 testing data from the specified API
def fetch_testing_data(api_url, cutoff_date):  
    print(f"\nFetching data from the API until the date {cutoff_date}. Please wait...")
    page = 1
    all_test_data = []
    
    # Retrieve data in chunks until no more data is available
    while True:
        params = {'$limit': 20000, '$offset': (page - 1) * 20000}  # Adjust limit as needed
        try:
            response = requests.get(api_url, params=params, verify=False)
            response.raise_for_status()  # Raise an error for bad responses
            page_data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            break
        
        if not page_data:
            break
            
        # Filter data for records with date less than or equal to cutoff_date
        filtered_data = [
            record for record in page_data if record.get('date').split('T')[0] <= cutoff_date
        ]
        all_test_data.extend(filtered_data)
        page += 1

    return all_test_data

# Function to calculate the total number of PCR tests performed as of the specified date
def calculate_total_pcr_tests(test_data, cutoff_date):
    # Convert the cutoff_date to a string with the format YYYY-MM-DD
    cutoff_date_str = datetime.strptime(cutoff_date, '%Y-%m-%d').strftime('%Y-%m-%d')
    print("\nCalculating the Total PCR Tests...")
    
    df = pd.DataFrame(test_data)
    total_pcr_tests = 0

    # Sum PCR tests based on available fields
    for _, record in df.iterrows():
        record_date = record.get('date', '')
        if record_date <= cutoff_date_str:
            total_pcr_tests += int(record.get('total_results_reported', 0))

    return total_pcr_tests

# Function to calculate the 7-day rolling average of new cases for the last 30 days
def calculate_7_day_rolling_average(test_data, cutoff_date):
    print("\nCalculating the 7-Day Rolling Average of New Cases...")
    df = pd.DataFrame(test_data)
    rolling_average = []
    
    # Convert the cutoff_date to a date object
    cutoff_date_obj = datetime.strptime(cutoff_date, '%Y-%m-%d').date()
    start_date = cutoff_date_obj - timedelta(days=30)

    for i in range(0, 30, 7):
        if cutoff_date_obj <= start_date:
            break
        
        total_new_cases = 0
        end_date = start_date + timedelta(days=7)
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        # Format date in DataFrame for comparison
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
        # Get new cases in the specified date range
        new_cases = df[(df['date'] >= start_date_str) & (df['date'] <= end_date_str)]['new_results_reported'].values
        total_new_cases = pd.to_numeric(new_cases, errors='coerce').sum()
        
        if new_cases.shape[0] != 0:
            average = total_new_cases / 7
            rounded_average = round(average, 2)
            rolling_average.append(rounded_average)
        else:
            rolling_average.append(0)

        start_date = end_date + timedelta(days=1)

    return rolling_average

# Function to get the top 10 states with the highest test positivity rate
def get_top_positivity_rate_states(test_data, cutoff_date):
    print("\nGetting Top 10 States with the Highest Positivity Rates...")
    df = pd.DataFrame(test_data)
    
    positivity_rates = {}  # Initialize an empty dictionary for positivity rates
    start_date = datetime.strptime(cutoff_date, '%Y-%m-%d') - timedelta(days=30)

    for state in df['state'].unique():
        state_data = df[df['state'] == state]
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = cutoff_date
        
        state_data['date'] = pd.to_datetime(state_data['date']).dt.strftime('%Y-%m-%d')
        state_data = state_data[(state_data['date'] >= start_date_str) & (state_data['date'] <= end_date_str)]
        
        total_tests = pd.to_numeric(state_data['total_results_reported'].sum(), errors='coerce')
        positive_tests = state_data[state_data['overall_outcome'] == 'Positive']['total_results_reported'].values
        positive_tests_sum = pd.to_numeric(positive_tests, errors='coerce').sum()
        
        
        # Calculate positivity rate
        positivity_rate = round((positive_tests_sum) / (total_tests) * 100, 2) if total_tests != 0 else 0
        positivity_rates[state] = positivity_rate

    # Sort and get top 10 states
    sorted_positivity_rates = sorted(positivity_rates.items(), key=lambda x: x[1], reverse=True)
    top_10_states = sorted_positivity_rates[:10]

    return top_10_states

# Function to generate a report with the outputs of the calculations
def generate_report(test_data, cutoff_date):
    report = {}  # Initialize an empty report dictionary
    cutoff_date_str = cutoff_date.strftime('%Y-%m-%d')  # Convert the cutoff_date to a string with the format

    # Add total PCR Tests to the report
    try:
        total_pcr_tests = calculate_total_pcr_tests(test_data, cutoff_date_str)
        report['Total PCR Tests'] = total_pcr_tests
    except Exception as e:
        print(f"Error calculating total PCR tests: {e}")

    # Add rolling average of new cases to the report
    try:
        rolling_average = calculate_7_day_rolling_average(test_data, cutoff_date_str)
        report['7-Day Rolling Average of New Cases'] = rolling_average
    except Exception as e:
        print(f"Error calculating rolling average of new cases: {e}")

    # Add top 10 states with the highest test positivity rate to the report
    try:
        top_10_states = get_top_positivity_rate_states(test_data, cutoff_date_str)
        report['Top 10 States with Highest Positivity Rate %'] = top_10_states
    except Exception as e:
        print(f"Error getting top 10 states by positivity rate: {e}")

    return report

# Main function to run the analysis
def main():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # Ignore warnings
        
        base_url = "https://healthdata.gov/resource/j8mb-icvb.json"
        current_date = datetime.now().strftime('%Y-%m-%d')
        print(f"Today's date is {current_date}")
        
        target_date_str = input("Enter the target date in the format (YYYY-MM-DD): ")
        
        try:
            target_date = datetime.strptime(target_date_str, '%Y-%m-%d')
            target_date = target_date.strftime('%Y-%m-%d')
            print(f"Input Date is {target_date}")
        except ValueError as ve:
            print(f"Invalid date format: {ve}")
            return
        
        # Fetch data from the API
        full_test_data = fetch_testing_data(base_url, target_date)
        
        # Generate the report
        report = generate_report(full_test_data, date.fromisoformat(target_date))
        
        # Print the report
        for key, value in report.items():
            print(f"{key}: {value}")

# Ensure main function runs if this script is executed
if __name__ == "__main__":
    main()
