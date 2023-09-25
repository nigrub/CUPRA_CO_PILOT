import openai
import streamlit as st
import pandas as pd

st.title('CSV Data Analyser')

openai.api_key = st.secrets["openai"]["api_key"]
st.session_state["openai_model"] = "gpt-4"

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
        header_row = extracted_table.iloc[0]
        extracted_table = extracted_table[1:]
        extracted_table.columns = header_row

        first_column_name = extracted_table.columns[0]
        extracted_table[first_column_name] = pd.to_datetime(extracted_table[first_column_name], format='%d/%m/%Y')
        extracted_table.rename(columns={first_column_name: 'Week'}, inplace=True)

        tables_data[table_name] = extracted_table
    return tables_data


# Function to generate the initial question for the GPT API
def generate_initial_question(selected_week):
    question = f"Generate a summary and analysis for the data up to {selected_week}:"
    question += (
    "\n\n1. Visits – Compare the number of visits between the most recent week (ending 4th September) and the previous week. "
    "Calculate the percentage increase and provide specific numbers. Mention if all channels saw an increase and highlight "
    "significant changes in channels like Social and Email."
    "\n\n2. Configs – Analyze the week-over-week increase in the number of configurations. Identify the most popular model and "
    "any notable trends in model preferences."
    "\n\n3. Finance Calcs – Examine the week-over-week change in finance calculations. Highlight any records or significant changes "
    "in model preferences."
    "\n\n4. Testdrive Requests – Analyze the week-over-week change in test drive requests. Identify any significant changes in "
    "test drive preferences or sources of requests."
    "\n\n5. Contact Me Pages – Analyze the week-over-week change in the use of 'Contact Me' pages. Highlight any trends or notable "
    "changes in the use of these pages."
    "\n\n6. Part Exchange Requests – Examine the week-over-week change in part exchange requests submitted to retailers. Highlight "
    "significant changes or trends in the types of vehicles being exchanged."
    )
    return question

# Function to answer Question 1
def answer_question_1(tables_data, selected_week_index):
    data = tables_data["Overall Traffic Visits"]
    current_week_visits = float(data.iloc[selected_week_index, 2])  # 3rd column
    previous_week_visits = float(data.iloc[selected_week_index - 1, 2]) if selected_week_index > 0 else None
    if previous_week_visits is not None:
        change = current_week_visits - previous_week_visits
        return f"The number of visits in the most recent week increased by {change} from the previous week."
    else:
        return f"The number of visits in the most recent week is {current_week_visits}."

# Function to answer Question 2
def answer_question_2(tables_data, selected_week_index):
    data = tables_data["Overall Traffic Actions"]
    current_week_configs = float(data.iloc[selected_week_index, 2])  # 3rd column
    previous_week_configs = float(data.iloc[selected_week_index - 1, 2]) if selected_week_index > 0 else None
    if previous_week_configs is not None:
        change = current_week_configs - previous_week_configs
        return f"The number of configurations in the most recent week increased by {change} from the previous week."
    else:
        return f"The number of configurations in the most recent week is {current_week_configs}."

# Function to answer Question 3
def answer_question_3(tables_data, selected_week_index):
    data = tables_data["Overall Traffic Actions"]
    current_week_finance_calcs = float(data.iloc[selected_week_index, 1])  # 2nd column
    previous_week_finance_calcs = float(data.iloc[selected_week_index - 1, 1]) if selected_week_index > 0 else None
    if previous_week_finance_calcs is not None:
        change = current_week_finance_calcs - previous_week_finance_calcs
        return f"The number of finance calculations in the most recent week increased by {change} from the previous week."
    else:
        return f"The number of finance calculations in the most recent week is {current_week_finance_calcs}."

# Function to answer Question 4
def answer_question_4(tables_data, selected_week_index):
    data = tables_data["New Visitors Leads"]
    current_week_testdrive_requests = float(data.iloc[selected_week_index, 1])  # 2nd column
    previous_week_testdrive_requests = float(data.iloc[selected_week_index - 1, 1]) if selected_week_index > 0 else None
    if previous_week_testdrive_requests is not None:
        change = current_week_testdrive_requests - previous_week_testdrive_requests
        return f"The number of test drive requests in the most recent week increased by {change} from the previous week."
    else:
        return f"The number of test drive requests in the most recent week is {current_week_testdrive_requests}."

# Function to answer Question 5
def answer_question_5(tables_data, selected_week_index):
    data = tables_data["New Visitors Actions"]
    current_week_contact_me_pages = float(data.iloc[selected_week_index, 2])  # 3rd column
    previous_week_contact_me_pages = float(data.iloc[selected_week_index - 1, 2]) if selected_week_index > 0 else None
    if previous_week_contact_me_pages is not None:
        change = current_week_contact_me_pages - previous_week_contact_me_pages
        return f"The use of 'Contact Me' pages in the most recent week increased by {change} from the previous week."
    else:
        return f"The use of 'Contact Me' pages in the most recent week is {current_week_contact_me_pages}."

# Function to answer Question 6
def answer_question_6(tables_data, selected_week_index):
    data = tables_data["Overall Traffic Actions"]
    current_week_part_exchange_requests = float(data.iloc[selected_week_index, 3])  # 4th column
    previous_week_part_exchange_requests = float(data.iloc[selected_week_index - 1, 3]) if selected_week_index > 0 else None
    if previous_week_part_exchange_requests is not None:
        change = current_week_part_exchange_requests - previous_week_part_exchange_requests
        return f"The number of part exchange requests in the most recent week increased by {change} from the previous week."
    else:
        return f"The number of part exchange requests in the most recent week is {current_week_part_exchange_requests}."

# Your streamlit interface code remains the same
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    tables_dataframes = extract_tables(data)
    available_dates = list(tables_dataframes["Overall Traffic Visits"]['Week'].dt.strftime('%d/%m/%Y'))
    selected_week = st.selectbox('Select a week for YTD view', available_dates)

    # Display answers to the fixed questions
    selected_week_index = available_dates.index(selected_week)
    st.write("1. ", answer_question_1(tables_dataframes, selected_week_index))
    st.write("2. ", answer_question_2(tables_dataframes, selected_week_index))
    st.write("3. ", answer_question_3(tables_dataframes, selected_week_index))
    st.write("4. ", answer_question_4(tables_dataframes, selected_week_index))
    st.write("5. ", answer_question_5(tables_dataframes, selected_week_index))
    st.write("6. ", answer_question_6(tables_dataframes, selected_week_index))






