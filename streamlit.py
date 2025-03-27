import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Set Streamlit Page Configuration
st.set_page_config(page_title="Booking Data Dashboard", layout="wide")

# Load Dataset
st.write("##  Data Cleaning and Analysis")
st.write("### Step 1: Load the Data")
dataset = pd.read_excel(r"DataAnalyst_Assesment_Dataset.xlsx")

st.write("Raw Data Sample:")
st.dataframe(dataset.head())

# Data Cleaning Steps
st.write("### Step 2: Handle Missing Values")
dataset["Class Type"].fillna('Not Specified', inplace=True)
dataset["Instructor"].fillna('Not Assigned', inplace=True)
dataset["Time Slot"].fillna("Unknown", inplace=True)
dataset["Duration (mins)"].fillna(dataset["Duration (mins)"].median(), inplace=True)
dataset["Facility"].fillna("No Facility", inplace=True)
dataset["Theme"].fillna("No Theme", inplace=True)
dataset["Subscription Type"].fillna('No Subscription', inplace=True)
dataset["Customer Email"].fillna('unknown@example.com', inplace=True)
dataset["Customer Phone"].fillna('000-000-0000', inplace=True)

st.write("### Step 3: Convert Data Types")
dataset['Booking Date'] = pd.to_datetime(dataset['Booking Date'], errors='coerce')

st.write("### Step 4: Remove Duplicates")
dataset.drop_duplicates(inplace=True)

st.write("### Step 5: Handle Outliers (Price)")
dataset = dataset[dataset["Price"] > 0]  # Remove negative or zero price values

st.write("✅ Data Cleaning Completed! Cleaned Data Sample:")
st.dataframe(dataset.head())

# Save Cleaned Data
#ataset.to_csv("cleaned_data.csv", index=False)

# Dashboard Title
st.title("Booking Data Visualization")

# Key Metrics
st.write("### Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric(label="Total Bookings", value=dataset.shape[0])
col2.metric(label="Total Revenue", value=dataset["Price"].sum())
col3.metric(label="Avg Duration (mins)", value=round(dataset["Duration (mins)"].mean(), 2))

# Booking Type Distribution
st.write("### Booking Type Distribution")
fig = px.pie(dataset, names="Booking Type", title="Distribution of Booking Types")
st.plotly_chart(fig)

# Revenue by Service Type
st.write("### Revenue by Service Type")
fig = px.bar(dataset, x="Service Type", y="Price", title="Revenue by Service Type", color="Service Type")
st.plotly_chart(fig)

# Bookings Over Time
st.write("### Bookings Over Time")
daily_bookings = dataset.groupby(dataset['Booking Date'].dt.date).size().reset_index(name='Count')
fig = px.line(daily_bookings, x='Booking Date', y='Count', title='Bookings Over Time')
st.plotly_chart(fig)

# Top 10 Instructors
st.write("### Top 10 Instructors by Number of Classes")
instructor_counts = dataset['Instructor'].value_counts().nlargest(10).reset_index()
instructor_counts.columns = ['Instructor', 'Count']
fig = px.bar(instructor_counts, x='Instructor', y='Count', title='Top 10 Instructors')
st.plotly_chart(fig)

# Filter Data
st.write("### Filter Data")
booking_type = st.selectbox("Select Booking Type", dataset["Booking Type"].unique())
filtered_dataset = dataset[dataset["Booking Type"] == booking_type]
st.dataframe(filtered_dataset)

