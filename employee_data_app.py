
import streamlit as st
import pandas as pd

# Load the Excel file
file_path = 'data generator.xlsx'
df = pd.read_excel(file_path, engine='openpyxl')

# Set admin password
admin_password = 'admin123'

# Function to authenticate user
def authenticate(employee_id, password):
    if employee_id in df['Employee ID'].values:
        stored_password = df.loc[df['Employee ID'] == employee_id, 'Password'].values[0]
        if stored_password == password:
            return True
    return False

# Function to display and edit employee data
def display_employee_data(employee_id):
    st.write(f"### Employee Data for ID: {employee_id}")
    employee_data = df.loc[df['Employee ID'] == employee_id]
    for column in df.columns:
        if column != 'Password':
            new_value = st.text_input(f"{column}", employee_data[column].values[0])
            df.loc[df['Employee ID'] == employee_id, column] = new_value

# Function to display and edit all employee data (admin view)
def display_all_data():
    st.write("### Admin View: All Employee Data")
    for index, row in df.iterrows():
        st.write(f"#### Employee ID: {row['Employee ID']}")
        for column in df.columns:
            if column != 'Password':
                new_value = st.text_input(f"{column}", row[column], key=f"{row['Employee ID']}_{column}")
                df.at[index, column] = new_value

# Streamlit app
st.title("Employee Data Generator")

# Login form
st.sidebar.title("Login")
employee_id = st.sidebar.text_input("Employee ID")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Login"):
    if authenticate(employee_id, password):
        st.sidebar.success("Login successful!")
        if password == admin_password:
            display_all_data()
        else:
            display_employee_data(employee_id)
        if st.button("Save Changes"):
            df.to_excel(file_path, index=False, engine='openpyxl')
            st.success("Changes saved successfully!")
    else:
        st.sidebar.error("Invalid Employee ID or Password.")
