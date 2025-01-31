import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Set up the page configuration
st.set_page_config(
    page_title="Heart Disease EDA",  # Title in browser tab
    page_icon="❤️",  # Icon in the tab
    layout="wide",  # Layout (wide)
)

# Streamlit title and description with animated fade-in
st.title("Heart Disease EDA 🫀")
st.markdown("""
    Welcome to the **Heart Disease Dataset Explorer**.  
    This app helps in visualizing and analyzing various aspects of the heart disease dataset.  
    The dataset contains key health indicators like age, cholesterol, heart rate, and more.  
    Let's dive in! 😃
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.header("Dataset Information 📊")
st.sidebar.write("### First Five Rows of the Dataset 📋")
df = pd.read_csv('heart.csv')
st.sidebar.dataframe(df.head())

# Dataset statistics and column info
st.sidebar.write("### Dataset Statistics 📊")
st.sidebar.write(df.describe())

# Show column names
st.sidebar.write("### Dataset Columns 🔢")
st.sidebar.write(df.columns.tolist())

# Sidebar for selecting plot types with a neat animation for selection
st.sidebar.header("Visualization Controls 🎨")
plot_type = st.sidebar.radio("Choose Plot Type 🖼️",
                             ["Distribution Plots 📈", "Pie Charts 🍰", "Violin Plots 🎻", "Correlation Matrix & Heatmap 🔥",
                              "Joint Plots 🤝", "Pairplot 🔗"], index=0)

# Function to add animation
def animate_plot(fig):
    st.markdown(
        """
        <style>
        .stApp {
            animation: fadein 1s ease-out;
        }
        @keyframes fadein {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        </style>
        """, unsafe_allow_html=True)
    st.pyplot(fig)

# Display selected plot type with improved animations
if plot_type == "Distribution Plots 📈":
    st.header("Distribution of Features 📊")
    columns_to_plot = ['Age', 'RestingBP', 'Cholesterol', 'MaxHR']

    def show_distribution_plot(column_name):
        fig, ax = plt.subplots()
        sns.histplot(df[column_name], kde=True, color='skyblue', ax=ax)
        ax.set_title(f"Distribution of {column_name}")
        animate_plot(fig)

    for col in columns_to_plot:
        show_distribution_plot(col)

elif plot_type == "Pie Charts 🍰":
    st.header("Categorical Feature Distribution (Pie Charts) 🥧")

    def show_pie_chart(column_name):
        fig, ax = plt.subplots(figsize=(6, 6))
        df.groupby(column_name).size().plot(kind='pie', autopct='%.1f%%', ax=ax, colors=sns.color_palette("coolwarm"))
        ax.set_ylabel('')
        animate_plot(fig)

    categorical_columns = ['Sex', 'ChestPainType', 'RestingECG', 'ST_Slope', 'HeartDisease']

    for col in categorical_columns:
        show_pie_chart(col)

elif plot_type == "Violin Plots 🎻":
    st.header("Violin Plots for Feature Distributions 🎶")

    def show_violin_plot(x=None, y=None):
        fig, ax = plt.subplots(figsize=(6, 4))
        if y is None:
            sns.violinplot(x=df[x], ax=ax, palette="coolwarm")
        else:
            sns.violinplot(x=df[x], y=df[y], ax=ax, palette="coolwarm")
        animate_plot(fig)

    violin_plots = [
        ('Age', None),
        ('HeartDisease', 'Sex'),
        ('HeartDisease', 'Age'),
        ('HeartDisease', 'Cholesterol')
    ]

    for x, y in violin_plots:
        show_violin_plot(x, y)

elif plot_type == "Correlation Matrix & Heatmap 🔥":
    st.header("Correlation Matrix 🔗")

    # Compute the correlation matrix
    correlation_matrix = df.corr(numeric_only=True)

    st.write(correlation_matrix)

    st.write("### Heatmap of the Correlation Matrix 🔥")

    def show_heatmap():
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
        ax.set_title("Correlation Heatmap 🔥")
        animate_plot(fig)

    show_heatmap()

elif plot_type == "Joint Plots 🤝":
    st.header("Joint Plots for Feature Relationships 🤝")

    def show_jointplot(x, y, kind):
        g = sns.jointplot(x=df[x], y=df[y], kind=kind, color="skyblue")
        g.fig.suptitle(f"Joint Plot: {x} vs {y} ({kind})", fontsize=14)
        g.fig.tight_layout()
        g.fig.subplots_adjust(top=0.95)  # Adjust title to fit
        animate_plot(g.fig)

    jointplot_list = [
        ('Age', 'MaxHR', 'hex'),
        ('Age', 'MaxHR', 'reg'),
        ('Cholesterol', 'MaxHR', 'reg'),
        ('HeartDisease', 'MaxHR', 'reg')
    ]

    for x, y, kind in jointplot_list:
        show_jointplot(x, y, kind)

elif plot_type == "Pairplot 🔗":
    st.header("Pairplot of Features 🔗")
    fig = sns.pairplot(df, palette="coolwarm")
    animate_plot(fig)

# Footer with smooth animation
st.markdown("""
---
Created with ❤️ by **Heart Disease Dataset Explorer**.  
Enjoy exploring the data and visualizations! 🎉
""", unsafe_allow_html=True)
