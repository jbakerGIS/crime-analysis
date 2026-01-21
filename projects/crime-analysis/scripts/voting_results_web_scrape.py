import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

def parse_row_intelligently(row_data):
    """
    Intelligently parse a row by detecting data types rather than relying on position.
    Returns a standardized 11-column row.
    """
    # Helper function to check if a value is a percentage
    def is_percent(val):
        return '%' in val
    
    # Helper function to check if a value is likely a vote count (large number with commas)
    def is_vote_count(val):
        return ',' in val and val.replace(',', '').isdigit()
    
    # Helper function to check if a value is likely an EV (small integer)
    def is_ev(val):
        return val.isdigit() and int(val) <= 100
    
    if len(row_data) < 7:
        return None  # Not enough data
    
    # Initialize result with 11 columns
    result = [''] * 11
    result[0] = row_data[0]  # STATE
    result[1] = row_data[1]  # TOTAL_VOTES
    
    # Parse the remaining columns (starting from index 2)
    remaining = row_data[2:]
    idx = 0
    
    # Parse Democratic candidate data (positions 2-4)
    if idx < len(remaining):
        # Should be: Votes, %, [EV]
        if is_vote_count(remaining[idx]) or remaining[idx].isdigit():
            result[2] = remaining[idx]  # Democratic_Votes
            idx += 1
        
        if idx < len(remaining) and is_percent(remaining[idx]):
            result[3] = remaining[idx]  # Democratic_Percent
            idx += 1
        
        if idx < len(remaining) and is_ev(remaining[idx]):
            result[4] = remaining[idx]  # Democratic_EV
            idx += 1
    
    # Parse Republican candidate data (positions 5-7)
    if idx < len(remaining):
        if is_vote_count(remaining[idx]) or remaining[idx].isdigit():
            result[5] = remaining[idx]  # Republican_Votes
            idx += 1
        
        if idx < len(remaining) and is_percent(remaining[idx]):
            result[6] = remaining[idx]  # Republican_Percent
            idx += 1
        
        if idx < len(remaining) and is_ev(remaining[idx]):
            result[7] = remaining[idx]  # Republican_EV
            idx += 1
    
    # Parse Others candidate data (positions 8-10) - only in recent elections
    if idx < len(remaining):
        if is_vote_count(remaining[idx]) or remaining[idx].isdigit():
            result[8] = remaining[idx]  # Others_Votes
            idx += 1
        
        if idx < len(remaining) and is_percent(remaining[idx]):
            result[9] = remaining[idx]  # Others_Percent
            idx += 1
        
        if idx < len(remaining) and is_ev(remaining[idx]):
            result[10] = remaining[idx]  # Others_EV
            idx += 1
    
    return result


def scrape_election_table(url):
    """
    Scrape election table from UCSB Presidency website
    
    Args:
        url: URL of the page to scrape
        
    Returns:
        pandas DataFrame containing the table data
    """
    # Send GET request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    # Parse HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table in the field-body div
    table = soup.find('div', class_='field-body').find('table')
    
    if not table:
        raise ValueError("Table not found on the page")
    
    # Extract table rows
    rows = []
    tbody = table.find('tbody')
    
    for tr in tbody.find_all('tr'):
        # Get all td elements
        tds = tr.find_all('td')
        
        # Extract only non-empty cells
        row_data = []
        for td in tds:
            cell_text = td.get_text(strip=True)
            if cell_text:
                row_data.append(cell_text)
        
        # Only process rows with enough data (at least 7 columns for state data)
        if len(row_data) >= 7:
            parsed_row = parse_row_intelligently(row_data)
            if parsed_row:
                rows.append(parsed_row)
    
    # Define the column names
    headers = ['STATE', 'TOTAL_VOTES', 'Democratic_Votes', 'Democratic_Percent', 'Democratic_EV', 
               'Republican_Votes', 'Republican_Percent', 'Republican_EV', 'Others_Votes', 'Others_Percent', 'Others_EV']
    
    # Create DataFrame
    df = pd.DataFrame(rows, columns=headers)
    
    # Filter out the header row if it got included
    df = df[df['STATE'] != 'STATE']
    
    # Filter out rows where STATE column contains long text (like instructions)
    df = df[df['STATE'].str.len() < 50]
    
    return df


# Main execution
if __name__ == "__main__":
    try:
        # Create output directory if it doesn't exist
        from pathlib import Path
        
        # Script is in: crime-analysis/scripts/web_scrape_full.py
        # We need to save to: crime-analysis/data/raw/
        output_dir = Path(__file__).parent.parent / "data" / "raw"
        
        print(f"Saving files to: {output_dir.absolute()}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        election_years = [2012, 2016, 2020, 2024]
        for year in election_years:
            url = f"https://www.presidency.ucsb.edu/statistics/elections/{year}"
            
            # Scrape the table
            df = scrape_election_table(url)
            
            # Display the data
            print(f"\n{year} Presidential Election Results:")
            print("=" * 100)
            print(df.to_string())
            print("\n" + "=" * 100)
            print(f"Total states/rows: {len(df)}")
            
            # Save to CSV
            output_file = f"election_{year}_data.csv"
            output_path = output_dir / output_file
            df.to_csv(output_path, index=False)
            print(f"Data saved to {output_path}\n")
        
        print("All files saved successfully!")
        
    except Exception as e:
        print(f"Error scraping data: {e}")
        import traceback
        traceback.print_exc()