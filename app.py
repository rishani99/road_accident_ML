import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Road Accident Dashboard", layout="wide")

# Load Excel file
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("road_accident.xlsx")
        return df
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return pd.DataFrame()

df = load_data()

# Sidebar Navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Dataset", "Summary", "Pie Chart", "Scatter Plot"])

# Pages
if page == "Home":
    st.title("🚗 Road Accident Dashboard")
    st.markdown("Welcome! Analyze and visualize accident data.")

elif page == "Dataset":
    st.title("📄 Dataset")
    if not df.empty:
        st.dataframe(df)
    else:
        st.warning("No data found.")

elif page == "Summary":
    st.title("📊 Summary Statistics")
    if not df.empty:
        st.write(df.describe(include='all'))
    else:
        st.warning("No data to summarize.")

elif page == "Pie Chart":
    st.title("🥧 Pie Chart")
    if not df.empty:
        cat_cols = df.select_dtypes(include='object').columns.tolist()
        if cat_cols:
            col = st.selectbox("Select categorical column", cat_cols)
            pie_data = df[col].value_counts()

            fig, ax = plt.subplots()
            ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            st.pyplot(fig)
        else:
            st.warning("No categorical columns found.")
    else:
        st.warning("No data available.")

elif page == "Scatter Plot":
    st.title("📈 Scatter Plot")
    if not df.empty:
        num_cols = df.select_dtypes(include='number').columns.tolist()
        if len(num_cols) >= 2:
            x = st.selectbox("Select X-axis", num_cols)
            y = st.selectbox("Select Y-axis", num_cols, index=1)

            fig, ax = plt.subplots()
            sns.scatterplot(x=df[x], y=df[y], ax=ax)
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            st.pyplot(fig)
        else:
            st.warning("Not enough numeric columns for scatter plot.")
    else:
        st.warning("No data available.")
