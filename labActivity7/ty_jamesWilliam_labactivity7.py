# BEFORE RUNNING PASTE 'pip install ucimlrepo pandas plotly' IN TERMINAL ! ! !

import pandas as pd
import plotly.express as px
from ucimlrepo import fetch_ucirepo

# Use pandas to set x and y of plot
iris = fetch_ucirepo(id=53)
X = iris.data.features
y = iris.data.targets

# Combine features 
df = pd.concat([X, y], axis=1)

# Create scatterplot with plotly
fig = px.scatter(
    df, 
    x=df.columns[0], 
    y=df.columns[1], 
    color=y.columns[0], 
    title="Scatter Plot of Iris Dataset (Sepal Length vs. Sepal Width)",
    labels={df.columns[0]: "Sepal Length", df.columns[1]: "Sepal Width", y.columns[0]: "Species"}
)
# Display in web browser
fig.show()

# Add interpretation
print("From the scatter plot, we can observe the different characteristics of the three given species of the Iris flower. For example, the Iris-setosa is a width dominant species who has higher widths than length. While Iris-veriscolor and Iris-virginica almost share the same width and length, but from the plot we can observe that Iris-virginica can have greater sepal lengths")