import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Heart Disease EDA",  # Title in browser tab
    page_icon="❤️",  # Path to your icon file (ensure it's in the same directory or provide the full path)
    layout="wide"  # Optional: You can adjust the layout (wide or centered)
)


# Streamlit title and description
st.title("Heart Disease EDA")
st.markdown("""
Welcome to the **Heart Disease Dataset Explorer**.  
This app helps in visualizing and analyzing various aspects of the heart disease dataset.  
The dataset contains key health indicators like age, cholesterol, heart rate, and more.
""")

# Load the dataset
df = pd.read_csv('heart.csv')

# Display dataset information
st.sidebar.header("Dataset Information")
st.sidebar.write("### First Five Rows of the Dataset")
st.sidebar.dataframe(df.head())

# Dataset statistics and column info
st.sidebar.write("### Dataset Statistics")
st.sidebar.write(df.describe())

# Show column names
st.sidebar.write("### Dataset Columns")
st.sidebar.write(df.columns.tolist())

# Sidebar for selecting plot types
st.sidebar.header("Visualization Controls")
plot_type = st.sidebar.radio("Choose Plot Type",
                             ["Distribution Plots", "Pie Charts", "Violin Plots",
                              "Correlation Matrix & Heatmap", "Joint Plots", "Pairplot"])

# Display selected plot type
if plot_type == "Distribution Plots":
    st.header("Distribution of Features")
    columns_to_plot = ['Age', 'RestingBP', 'Cholesterol', 'MaxHR']

    def show_distribution_plot(column_name):
        fig, ax = plt.subplots()
        sns.histplot(df[column_name], kde=True, color='blue', ax=ax)
        st.pyplot(fig)

    for col in columns_to_plot:
        st.write(f"#### Distribution of {col}")
        show_distribution_plot(col)

elif plot_type == "Pie Charts":
    st.header(" Categorical Feature Distribution (Pie Charts)")

    def show_pie_chart(column_name):
        fig, ax = plt.subplots(figsize=(6, 6))
        df.groupby(column_name).size().plot(kind='pie', autopct='%.1f%%', ax=ax)
        ax.set_ylabel('')  # Remove the y-label for better visualization
        st.pyplot(fig)

    categorical_columns = ['Sex', 'ChestPainType', 'RestingECG', 'ST_Slope', 'HeartDisease']

    for col in categorical_columns:
        st.write(f"#### Distribution of {col}")
        show_pie_chart(col)

elif plot_type == "Violin Plots":
    st.header(" Violin Plots for Feature Distributions")

    def show_violin_plot(x=None, y=None):
        fig, ax = plt.subplots(figsize=(6, 4))
        if y is None:
            sns.violinplot(x=df[x], ax=ax)
        else:
            sns.violinplot(x=df[x], y=df[y], ax=ax)
        st.pyplot(fig)

    violin_plots = [
        ('Age', None),
        ('HeartDisease', 'Sex'),
        ('HeartDisease', 'Age'),
        ('HeartDisease', 'Cholesterol')
    ]

    for x, y in violin_plots:
        st.write(f"#### Violin Plot: {y} vs {x}" if y else f"#### Violin Plot: {x}")
        show_violin_plot(x, y)

elif plot_type == "Correlation Matrix & Heatmap":
    st.header("Correlation Matrix")

    # Compute the correlation matrix
    correlation_matrix = df.corr(numeric_only=True)

    # Display the correlation matrix
    st.write(correlation_matrix)

    st.write("### Heatmap of the Correlation Matrix")

    # Function to generate heatmap
    def show_heatmap():
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
        st.pyplot(fig)

    # Display the heatmap
    show_heatmap()

elif plot_type == "Joint Plots":
    st.header(" Joint Plots for Feature Relationships")

    # Function to display joint plots
    def show_jointplot(x, y, kind):
        g = sns.jointplot(x=df[x], y=df[y], kind=kind)
        st.pyplot(g.figure)

    jointplot_list = [
        ('Age', 'MaxHR', 'hex'),
        ('Age', 'MaxHR', 'reg'),
        ('Cholesterol', 'MaxHR', 'reg'),
        ('HeartDisease', 'MaxHR', 'reg')
    ]

    for x, y, kind in jointplot_list:
        st.write(f"#### Joint Plot: {x} vs {y} ({kind})")
        show_jointplot(x, y, kind)

elif plot_type == "Pairplot":
    st.header("Pairplot of Features")
    fig = sns.pairplot(df)
    st.pyplot(fig)

# Footer
st.markdown("""
---
Created by **Heart Disease Dataset Explorer**.  
Enjoy exploring the data and visualizations!  
""")
