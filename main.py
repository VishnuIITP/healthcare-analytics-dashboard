# This is a sample Python script.

# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press F9 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("mysql+pymysql://root:1234@localhost:3306/healthcare")




import matplotlib.pyplot as plt
import streamlit as st

# create bar chart
# get unique values
query = """
SELECT * FROM appointment"""

df = pd.read_sql(query , engine)
age_options = df['age_group'].dropna().unique()
risk_options = ['All', 'Low Risk', 'High Risk']

st.sidebar.header(" Filters")

# dropdowns
selected_age = st.sidebar.selectbox("Select Age Group", ['All'] + list(age_options))
selected_risk = st.sidebar.selectbox("Select Risk Level", risk_options)

filtered_df = df.copy()

df_waits = pd.read_sql(query, engine)
st.subheader("📌 Key Metrics")
total_appointments = filtered_df.shape[0]

no_show_rate = round(filtered_df['no_show'].mean() * 100, 2)

high_risk_count = filtered_df['high_risk'].sum()
col1, col2, col3 = st.columns(3)

col1.metric("Total Appointments", total_appointments)

col2.metric("No-show Rate (%)", no_show_rate)

col3.metric("High-Risk Patients", high_risk_count)

query = """
SELECT
    CASE
        WHEN waiting_days <= 3 THEN 'Short Wait'
        WHEN waiting_days <= 10 THEN 'Medium Wait'
        ELSE 'Long Wait'
    END AS wait_category,

    ROUND(AVG(no_show) * 100, 2) AS no_show_rate

FROM appointment
GROUP BY wait_category
"""

df_wait = pd.read_sql(query, engine)

print(df_wait)

st.header("# No-show Analysis Based on Waiting Time")

st.write("This chart shows how waiting time impacts patient no-show behavior.")

fig, ax = plt.subplots()
ax.bar(df_wait['wait_category'], df_wait['no_show_rate'])
ax.set_xlabel("Waiting Time Category")
ax.set_ylabel("No-show Rate (%)")

st.pyplot(fig)

# insight
st.success("Insight: Longer waiting times lead to higher no-show rates, indicating scheduling inefficiencies.")

query2 = """
SELECT 
    age_group,
    COUNT(*) AS total
FROM appointment
GROUP BY age_group
"""

df_age = pd.read_sql(query2, engine)

df_age['age_group'] = df_age['age_group'].fillna("Unknown")
df_age['age_group'] = df_age['age_group'].astype(str)
print(df_age)

st.header(" --> Patient Distribution by Age Group")

st.write("This chart highlights which age groups contribute most to hospital visits.")

fig2, ax2 = plt.subplots()
ax2.bar(df_age['age_group'], df_age['total'])
ax2.set_xlabel("Age Group")
ax2.set_ylabel("Total Appointments")

st.pyplot(fig2)

st.success("Insight: Adults form the majority of patients, indicating higher healthcare demand in this segment.")

query3 = """
SELECT 
    high_risk,
    ROUND(AVG(no_show)*100,2) AS no_show_rate
FROM appointment
GROUP BY high_risk
"""

df_risk = pd.read_sql(query3, engine)

df_risk['high_risk'] = df_risk['high_risk'].map({
    0: 'Low Risk',
    1: 'High Risk'
})

st.header(" --> High-Risk Patient Behavior")

st.write("This chart compares no-show rates between high-risk and low-risk patients.")

fig3, ax3 = plt.subplots()

ax3.bar(df_risk['high_risk'], df_risk['no_show_rate'])

ax3.set_xlabel("Risk Category")
ax3.set_ylabel("No-show Rate (%)")

st.pyplot(fig3)

st.success("Insight: High-risk patients show different no-show patterns, which can help hospitals design targeted interventions.")






