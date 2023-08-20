import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

@st.cache()
def load_data():

	df = pd.read_csv('https://student-datasets-bucket.s3.ap-south-1.amazonaws.com/whitehat-ds-datasets/adult.csv', header=None)
	df.head()

	column_name =['age', 'workclass', 'fnlwgt', 'education', 'education-years', 'marital-status', 'occupation', 'relationship', 'race','gender','capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income']

	for i in range(df.shape[1]):
	  df.rename(columns={i:column_name[i]},inplace=True)

	df['native-country'] = df['native-country'].replace(' ?',np.nan)
	df['workclass'] = df['workclass'].replace(' ?',np.nan)
	df['occupation'] = df['occupation'].replace(' ?',np.nan)

	df.dropna(inplace=True)
	df.drop(columns='fnlwgt',axis=1,inplace=True)

	return df

census_df = load_data()

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Census Data web app")
st.sidebar.subheader("Display Raw Data")
if st.sidebar.checkbox("Raw Data"):
	st.subheader("Full Raw Dataset")
	st.dataframe(census_df)

st.sidebar.subheader("Select Visualization Method")
graph = st.sidebar.multiselect("Select Charts/Plots to show:", ("Histogram", "Pie Chart", "Boxplot", "Count Plot", "Correlation Heatmap", "Pair Plots", "Scatter Plot"))

if graph == "Histogram":
	st.subheader("Histogram")
	x = st.sidebar.selectbox("Select column to draw histogram of:",('age', 'workclass', 'education', 'education-years', 'marital-status', 'occupation', 'relationship', 'race','gender','capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income'))
	plt.figure(figsize=(16,4))
	plt.hist(census_df[x],bins='sturges', edgecolor = "chocolate")
	st.pyplot()
if graph == "Boxplot":
    st.subheader("Box Plot")
    columns = st.sidebar.selectbox("Select the column to create its box plot", ('age', 'workclass', 'education', 'education-years', 'marital-status', 'occupation', 'relationship', 'race','gender','capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income'))
    plt.figure(figsize = (16, 4))
    plt.title(f"Box plot for {columns}")
    hue = st.sidebar.selectbox("Select grouping", ('age', 'workclass', 'education', 'education-years', 'marital-status', 'occupation', 'relationship', 'race','gender','capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income'))
    sns.boxplot(census_df[columns], hue=hue)
    st.pyplot()
if graph == "Count Plot":
    st.subheader("Count plot")
    columns = st.sidebar.selectbox("Select the column to create its count plot", ('age', 'workclass', 'education', 'education-years', 'marital-status', 'occupation', 'relationship', 'race','gender','capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income'))
    sns.countplot(x = columns, data = census_df)
    st.pyplot()
if graph=="Pie Chart":
    st.subheader("Pie Chart")
    columns = st.sidebar.selectbox("Select the column to create its pie chart", ('age', 'workclass', 'education', 'education-years', 'marital-status', 'occupation', 'relationship', 'race','gender','capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income'))
    pie_data = census_df[columns].value_counts()
    plt.figure(figsize = (8, 8), dpi=96)
    plt.pie(pie_data, labels = pie_data.index, autopct = '%1.2f%%', startangle = 30, explode = np.linspace(.06, .16, 6))
    st.pyplot()
if graph=="Correlation Heatmap":
    st.subheader("Correlation Heatmap")
    plt.figure(figsize = (8, 8), dpi=96)
    ax = sns.heatmap(census_df.corr(), annot = True) # Creating an object of seaborn axis and storing it in 'ax' variable
    bottom, top = ax.get_ylim() # Getting the top and bottom margin limits.
    ax.set_ylim(bottom + 0.5, top - 0.5) # Increasing the bottom and decreasing the top margins respectively.
    st.pyplot()
if graph=="Pair Plots":
    st.subheader("Pair Plots")
    plt.figure(figsize = (16, 16))
    sns.pairplot(census_df)
    st.pyplot()
