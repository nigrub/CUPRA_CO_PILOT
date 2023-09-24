import openai
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

    tables_data = {}
    for table_name, (start_cell, end_cell) in tables_references.items():
        start_row, start_col = cell_to_indices(start_cell)
        end_row, end_col = cell_to_indices(end_cell)
        extracted_table = data.iloc[start_row:end_row + 1, start_col:end_col + 1]
        extracted_table.rename(columns={extracted_table.columns[0]: 'Week'}, inplace=True)
        extracted_table['Week'] = pd.to_datetime(extracted_table['Week'], format='%d/%m/%Y')
        tables_data[table_name] = extracted_table
    return tables_data

def generate_initial_question(selected_week):
    # Generates the initial question for the GPT API based on the selected week
    question = f"Generate a summary and analysis for the data up to {selected_week}:"
    question += (
    "\n\n1. Visits – Compare the number of visits between the most recent week (ending 4th September) and the previous week. "
    "Calculate the percentage increase and provide specific numbers. Mention if all channels saw an increase and highlight "
    "significant changes in channels like Social and Email."
    "\n\n2. Configs – Analyze the week-over-week increase in the number of configurations. Identify the most popular model and "
    "any notable trends in model preferences."
    "\n\n3. Finance Calcs – Examine the week-over-week change in finance calculations. Highlight any records or significant changes "
    "in model preferences."
    "\n\n4. Test Drive – Provide the number of test drive leads generated in the most recent week compared to the previous week."
    "\n\n5. Contact Me – Compare the number of contact leads generated in the most recent week with the previous week."
    "\n\n6. Part Exchange Leads – Analyze the number of part exchange leads generated in the most recent week and compare it to the "
    "previous week. Mention any trends over the last four weeks."
    "\n\n7. Virtual Showroom – Provide insights into the number of leads generated in the virtual showroom for the most recent week "
    "and any notable changes."
    "\n\n8. TLA lead gen. – Compare the number of leads generated through TLA in the most recent week with the previous week. Highlight "
    "any contributions towards the September target."
    "\n\nPlease provide detailed information and statistics for each of the above points."
    )
    return question

# Load the data
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    tables_dataframes = extract_tables(data)
    available_dates = list(tables_dataframes["Overall Traffic Visits"]['Week'].dt.strftime('%d/%m/%Y'))
    selected_week = st.selectbox('Select a week for YTD view', available_dates)

    # Date Selector
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
    selected_week = st.selectbox('Select a week for YTD view', available_dates)

    # Setting up the chatbot interface
    user_input = st.text_input("Ask me about the data:")
    if user_input:
        response = chat_with_document(user_input, selected_week)
        st.write(response)

def chat_with_document(user_query, selected_week):
    # Convert the selected week to its index for calculations
    reverse_indexed_dates = {date: i for i, date in enumerate(available_dates)}
    selected_week_index = reverse_indexed_dates[selected_week]

    # Based on user_query, extract the required information from tables_dataframes
    # and consider only rows up to selected_week_index

    # ... (Your logic to process the user's query and extract information)

    return "Response based on the user's query and selected date"

st.title("Welcome To The CUPRA Co-Pilot")
openai.api_key = st.secrets["openai"]["api_key"]

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    tables_dataframes = extract_tables(data)
    available_dates = list(tables_dataframes["Overall Traffic Visits"]['Week'].dt.strftime('%d/%m/%Y'))
    selected_week = st.selectbox('Select a week for YTD view', available_dates)

    initial_question = generate_initial_question(selected_week)
    response = openai.Completion.create(model="gpt-4", prompt=initial_question, max_tokens=500)
    st.write("GPT's response to the initial question goes here")  # Replace this with the actual GPT response

    user_input = st.text_input("Ask me about the data:")
    if user_input:
        response = chat_with_document(user_input, selected_week, tables_dataframes)
        # Display the response
        st.write(response)