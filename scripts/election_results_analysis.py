import pandas as pd
import numpy as np
from pathlib import Path

def get_election_files(input_path):
    """
    Returns a list of full file paths to election CSVs.
    """
    election_year_list = [2012, 2016, 2020, 2024]
    file_paths = [input_path / f"election_{year}_data_cleaned.csv" for year in election_year_list]
    return file_paths

def add_voting_results_column(df):
    """
    Adds a new column 'Political_Party_Voting_Results' to the dataframe
    based on the comparison of 'Democratic_Votes' and 'Republican_Votes'.

    Parameters:
    df (pd.DataFrame): DataFrame containing 'Democratic_Votes' and 'Republican_Votes' columns.

    Returns:
    pd.DataFrame: DataFrame with the new column added.
    """
    
    df['Political_Party_Voting_Results'] = np.where(
    df['Democratic_Votes'] > df['Republican_Votes'], 'Democrat',
    np.where(
        df['Republican_Votes'] > df['Democratic_Votes'], 'Republican',
        'Tie'
    )
    )
    return df

def aggregate_results_by_state(file_paths):
    """
    Reads election CSVs and returns a dictionary:
    {state: [party_2012, party_2016, party_2020, party_2024]}
    """
    state_results = {}
    for path in file_paths:
        df = pd.read_csv(path)
        df = add_voting_results_column(df)
        for row in df.itertuples():
            if row.STATE not in state_results:
                state_results[row.STATE] = []
            state_results[row.STATE].append(row.Political_Party_Voting_Results)
    
    return state_results
    
def get_majority_party_by_state(state_results):
    """
    Determines the majority party for each state across the election years.

    Parameters:
    state_results (dict): Dictionary with state as key and list of party results as value.

    Returns:
    dict: Dictionary with state as key and majority party as value.
    """
    majority_party = {}
    for state, results in state_results.items():
        dem_count = results.count('Democrat')
        rep_count = results.count('Republican')
        
        if dem_count > rep_count:
            majority_party[state] = 'Democratic'
        elif rep_count > dem_count:
            majority_party[state] = 'Republican'
        else:
            majority_party[state] = 'Tie'
    
    return majority_party

def build_results_dataframe(majority_party):
    """
    Builds a DataFrame from the majority party dictionary.

    Parameters:
    majority_party (dict): Dictionary with state as key and majority party as value.

    Returns:
    pd.DataFrame: DataFrame with states and their majority party.
    """
    data = {
        'STATE': list(majority_party.keys()),
        'Majority_Party': list(majority_party.values())
    }
    return pd.DataFrame(data)

def write_results_to_csv(df, output_path):
    """
    Writes the results DataFrame to a CSV file.

    Parameters:
    df (pd.DataFrame): DataFrame containing the results.
    output_path (str): Path to save the CSV file.
    """
    df.to_csv(output_path, index=False)

def main():
    base_path = Path(__file__).parent.parent / "data"
    print(f"Saving files to: {base_path.absolute()}")
    base_path.mkdir(parents=True, exist_ok=True)

    input_path = base_path / "intermediate/"

    output_file = "final/state_majority_party.csv"
    output_path = base_path / output_file

    file_paths = get_election_files(input_path)    
    state_results = aggregate_results_by_state(file_paths)
    majority_party = get_majority_party_by_state(state_results)
    results_df = build_results_dataframe(majority_party)
    write_results_to_csv(results_df, output_path)
    print(f"Majority party results saved to {output_path}")

if __name__ == "__main__":
    main()