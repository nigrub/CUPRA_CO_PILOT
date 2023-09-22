import streamlit as st
import pandas as pd


def cell_to_indices(cell_ref):
    col_ref, row_ref = ''.join(filter(str.isalpha, cell_ref)), ''.join(filter(str.isdigit, cell_ref))
    col_idx = sum([(ord(char) - ord('A') + 1) * (26 ** idx) for idx, char in enumerate(col_ref[::-1])]) - 1
    row_idx = int(row_ref) - 1
    return row_idx, col_idx


def extract_tables(data):
    tables_references = {
        "Overall Traffic Visits": ("A11", "S64"),
        "Overall Traffic Leads": ("A70", "D122"),
        "Overall Traffic Actions": ("A128", "F180"),
        "New Visitors Visits": ("A194", "S247"),
        "New Visitors Leads": ("A253", "D305"),
        "New Visitors Actions": ("A311", "F363"),
        "Return Visitors Visits": ("A377", "S430"),
        "Return Visitors Leads": ("A436", "D488"),
        "Return Visitors Actions": ("A494", "F546"),
        "Desktop Traffic Visits": ("A560", "S613"),
        "Desktop Traffic Leads": ("A619", "D671"),
        "Desktop Traffic Actions": ("A677", "F729"),
        "Mobile Traffic Visits": ("A743", "S796"),
        "Mobile Traffic Leads": ("A802", "D854"),
        "Mobile Traffic Actions": ("A860", "F912"),
        "Tablet Traffic Visits": ("A926", "S979"),
        "Tablet Traffic Leads": ("A985", "D1037"),
        "Tablet Traffic Actions": ("A1043", "F1095"),
        "Paid (SEA) Traffic Visits": ("A1109", "S1162"),
        "Paid (SEA) Traffic Leads": ("A1168", "D1220"),
        "Paid (SEA) Traffic Actions": ("A1226", "F1278"),
        "Organic (SEO) Traffic Visits": ("A1292", "S1345"),
        "Organic (SEO) Traffic Leads": ("A1351", "D1403"),
        "Organic (SEO) Traffic Actions": ("A1409", "F1461"),
        "Social Traffic Visits": ("A1475", "S1527"),
        "Social Traffic Leads": ("A1533", "D1585"),
        "Social Traffic Actions": ("A1591", "F1643"),
        "Direct Traffic Visits": ("A1657", "S1709"),
        "Direct Traffic Leads": ("A1715", "D1767"),
        "Direct Traffic Actions": ("A1773", "F1825"),
        "Session Refresh Traffic Visits": ("A1839", "S1891"),
        "Session Refresh Traffic Leads": ("A1897", "D1949"),
        "Session Refresh Traffic Actions": ("A1955", "F2007"),
        "Refferfal Traffic Visits": ("A2021", "S2073"),
        "Refferfal Traffic Leads": ("A2079", "D2131"),
        "Refferfal Traffic Actions": ("A2137", "F2189"),
    }

    tables_dataframes = {}
    for table_name, (start_ref, end_ref) in tables_references.items():
        start_row, start_col = cell_to_indices(start_ref)
        end_row, end_col = cell_to_indices(end_ref)

        extracted_table = data.iloc[start_row:end_row + 1, start_col:end_col + 1]
        extracted_table.columns = extracted_table.iloc[0]
        extracted_table = extracted_table.drop(extracted_table.index[0])

        # Convert 'Week' to DD/MM/YYYY format
        extracted_table['Week'] = pd.to_datetime(extracted_table['Week'], format='%d/%m/%Y')

        tables_dataframes[table_name] = extracted_table
    return tables_dataframes

def get_related_tables(tables, keyword):
    return {name: df for name, df in tables.items() if keyword in name}


def compute_means_for_type(tables, table_type, week_index):
    all_means = {}
    for name, table in tables.items():
        if table_type in name:
            # Filter the data up to the selected week index
            filtered_table = table.iloc[:week_index + 1]

            # Drop the 'Week' column as we're not computing its mean
            if 'Week' in filtered_table.columns:
                filtered_table = filtered_table.drop(columns=['Week'])

            # Compute the mean for the filtered data
            if not filtered_table.empty:
                mean_values = filtered_table.mean().fillna(0).round().astype(int)
                all_means[name] = mean_values.to_dict()

    # Convert the dictionary to a DataFrame for better presentation
    means_df = pd.DataFrame(all_means).transpose()
    return means_df


st.title('CSV Data Analyzer')
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    data = pd.read_csv(uploaded_file, header=None)
    tables_dataframes = extract_tables(data)

    if tables_dataframes:
        selected_table = st.selectbox('Select a table to view', list(tables_dataframes.keys()))

        available_dates = [
            "26/12/2022", "02/01/2023", "09/01/2023", "16/01/2023", "23/01/2023", "30/01/2023",
            "06/02/2023", "13/02/2023", "20/02/2023", "27/02/2023", "06/03/2023", "13/03/2023",
            "20/03/2023", "27/03/2023", "03/04/2023", "10/04/2023", "17/04/2023", "24/04/2023",
            "01/05/2023", "08/05/2023", "15/05/2023", "22/05/2023", "29/05/2023", "05/06/2023",
            "12/06/2023", "19/06/2023", "26/06/2023", "03/07/2023", "10/07/2023", "17/07/2023",
            "24/07/2023", "31/07/2023", "07/08/2023", "14/08/2023", "21/08/2023", "28/08/2023",
            "04/09/2023", "11/09/2023", "18/09/2023", "25/09/2023", "02/10/2023", "09/10/2023",
            "16/10/2023", "23/10/2023", "30/10/2023", "06/11/2023", "13/11/2023", "20/11/2023",
            "27/11/2023", "04/12/2023", "11/12/2023", "18/12/2023", "25/12/2023"
        ]

        # Indexed version of the available_dates
        indexed_dates = {i: date for i, date in enumerate(available_dates)}
        reverse_indexed_dates = {date: i for i, date in enumerate(available_dates)}

        # Use the available_dates directly in the dropdown for display
        selected_week = st.selectbox('Select a week for YTD view', available_dates)

        # Convert the selected week to its index for calculations
        selected_week_index = reverse_indexed_dates[selected_week]

        filtered_df = tables_dataframes[selected_table].iloc[:selected_week_index + 1]

        # Format the 'Week' column for display
        filtered_df['Week'] = filtered_df['Week'].dt.strftime('%d/%m/%Y')

        st.table(filtered_df.style.hide_index())

        if st.button("Show Summary Statistics"):
            keyword = None
            if "Visits" in selected_table:
                keyword = "Visits"
            elif "Leads" in selected_table:
                keyword = "Leads"
            elif "Actions" in selected_table:
                keyword = "Actions"

            related_tables = get_related_tables(tables_dataframes, keyword)
            means_df = compute_means_for_type(related_tables, keyword, selected_week_index)

            st.table(means_df)
