import pandas as pd
from base import tables
from io import StringIO

#=====================================Fixing Data Format==========================================#
input1 = tables['0']
input1 =input1.rename(columns = {'Line Item':'Line Items','Total':'Total Exposure'})

#==================Converting data format from Horizontal to Verticle=============================#
def convert_and_update(input):
    # Convert the DataFrame columns to lists
    scenarios = input.columns.tolist()
    deltas = input.values.tolist()[0]

    # Create a new DataFrame with Scenario and Delta_EVE columns
    new_df = pd.DataFrame({'Scenario': scenarios, 'Delta_EVE': deltas})
    # Write the updated DataFrame back to the CSV file
    return new_df

input2 = tables['14']
input3 = tables['15']

input2 = convert_and_update(input2)   # Delta EVE Excluding NS Accounts
input3 = convert_and_update(input3)   # Delta EVE

#======================================Changing Column Name=======================================#
input4 = tables['20']
input5 = tables['28']

input4 = input4.rename(columns={'Percentage': 'Delta_NII'})
input5 = input5.rename(columns={'Percentage': 'Delta_NII'})

input4_data = input4.to_csv(index=False)
input5_data = input5.to_csv(index=False)
input4 = pd.read_csv(StringIO(input4_data))
input5 = pd.read_csv(StringIO(input5_data))

#======================================Concatenating 7 Dataframes=================================#
def concatenate_csv_files(file_paths):

    # Concatenate all DataFrames in the list
    concatenated_df = pd.concat(file_paths, ignore_index=True)

    # Get the last column name
    last_column = concatenated_df.columns[-1]
    
    # Move the last column to index 1
    cols = concatenated_df.columns.tolist()
    cols.remove(last_column)
    new_columns = [cols[0], last_column] + cols[1:]
    concatenated_df = concatenated_df[new_columns]
    return concatenated_df

file_paths = [tables['7'],tables['8'],tables['9'],tables['10'],tables['11'],tables['12'],tables['13']]
input6 = concatenate_csv_files(file_paths)

#=====================================GroupBy Line Items==========================================#
input7 = tables['21']
if "Line Item\r" in input7.columns:
    input7.rename(columns={'Line Item\r': 'Line Item'}, inplace=True)
df = input7.drop(['Instrument','GL Code','Product Code','Currency Code','Interest Rate',
                'weighted_avg_interest','EIBOR Rate','Avg_Margin'], axis=1)
input7 = df.groupby(["CLASSIFICATION1", "Line Item"]).sum()
input7 = pd.DataFrame(input7).reset_index()

#=================================================================================================#
#                                      Reading Dataset                                            #
#=================================================================================================#    
line_items_data = input1

Delta_EVE_data = input3

Delta_EVE_NS_data = input2

NII_1Y_data = input4

NII_3Y_data = input5

EVE_Report_data = input6

Base_Report_data = input7

NII_Report_data = tables['22']