import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def scrape_election_table(url):
    """
    Scrape the 2024 election table from UCSB Presidency website
    
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
        # Get all td elements (including empty ones)
        tds = tr.find_all('td')
        
        # Extract only non-empty cells
        row_data = []
        for td in tds:
            cell_text = td.get_text(strip=True)
            # Only append non-empty cells
            if cell_text:
                row_data.append(cell_text)
        
        # State data rows can have 7, 8, 9, or 11 non-empty columns
        # 7 columns: 2012 format with one missing EV (most common)
        # 8 columns: 2012 format with all EVs present
        # 9 columns: 2016-2024 format with missing EV values
        # 11 columns: complete data with all EV values (header/totals)
        if len(row_data) in [7, 8, 9, 11]:
            rows.append(row_data)
    
    # Process rows to ensure all have 11 columns
    processed_rows = []
    for row in rows:
        if len(row) == 7:
            # 2012 format: STATE, TOTAL, Dem_Votes, Dem_%, Rep_Votes, Rep_%, Rep_EV
            # Missing Democratic EV (empty)
            new_row = [
                row[0],  # STATE
                row[1],  # TOTAL_VOTES
                row[2],  # Democratic_Votes
                row[3],  # Democratic_Percent
                '',      # Democratic_EV (empty)
                row[4],  # Republican_Votes
                row[5],  # Republican_Percent
                row[6],  # Republican_EV
                '',      # Others_Votes (empty for 2012)
                '',      # Others_Percent (empty for 2012)
                ''       # Others_EV (empty for 2012)
            ]
            processed_rows.append(new_row)
        elif len(row) == 8:
            # 2012 format with all EVs: STATE, TOTAL, Dem_Votes, Dem_%, Dem_EV, Rep_Votes, Rep_%, Rep_EV
            new_row = [
                row[0],  # STATE
                row[1],  # TOTAL_VOTES
                row[2],  # Democratic_Votes
                row[3],  # Democratic_Percent
                row[4],  # Democratic_EV
                row[5],  # Republican_Votes
                row[6],  # Republican_Percent
                row[7],  # Republican_EV
                '',      # Others_Votes (empty for 2012)
                '',      # Others_Percent (empty for 2012)
                ''       # Others_EV (empty for 2012)
            ]
            processed_rows.append(new_row)
        elif len(row) == 9:
            # 2016-2024 format with missing EVs
            new_row = [
                row[0],  # STATE
                row[1],  # TOTAL_VOTES
                row[2],  # Democratic_Votes
                row[3],  # Democratic_Percent
                '',      # Democratic_EV (empty)
                row[4],  # Republican_Votes
                row[5],  # Republican_Percent
                row[6],  # Republican_EV
                row[7],  # Others_Votes
                row[8],  # Others_Percent
                ''       # Others_EV (empty)
            ]
            processed_rows.append(new_row)
        else:
            # 11 columns - complete data
            processed_rows.append(row)
    
    # Define the column names (Democratic candidate first, Republican second)
    headers = ['STATE', 'TOTAL_VOTES', 'Democratic_Votes', 'Democratic_Percent', 'Democratic_EV', 
               'Republican_Votes', 'Republican_Percent', 'Republican_EV', 'Others_Votes', 'Others_Percent', 'Others_EV']
    
    # Create DataFrame
    df = pd.DataFrame(processed_rows, columns=headers)
    
    # Filter out the header row if it got included
    df = df[df['STATE'] != 'STATE']
    
    return df


# Main execution
if __name__ == "__main__":
    try:
        # Create output directory if it doesn't exist
        # Using Path from pathlib is more modern and cleaner
        from pathlib import Path
        
        # Script is in: crime-analysis/scripts/web_scrape_full.py
        # We need to save to: crime-analysis/data/raw/
        # So go up one level (..) then into data/raw
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