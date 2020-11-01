# %% [markdown]
# # COVID 19 LEX example

# %% import pandas
import pandas as pd

# %% [markdown]
## Set decimall precision
pd.options.display.float_format = "{:.5f}".format

# %% [markdown]
# ## Load the csv data file into pandas
covid_data_file = pd.read_csv("owid-covid-data.csv")

# %% [markdown]
# ## Examine the loaded data
covid_data_file.describe()

# %% [markdown]
# ## Extract relevant data for analysis
covid_ds = covid_data_file[["location", "date", "new_tests", "new_cases"]]

# %% [markdown]
# ## Examine the new dataframe
covid_ds.describe(include="all")

# %% [markdown]
# ## Printing missing values in dataframe
print (covid_ds.isnull().sum(axis=0))

# %% [markdown]
# ## Remove records with no value at new_tests cloumn
covid_ds.dropna(subset=["new_tests"], inplace=True)
print (covid_ds.isnull().sum(axis=0))

# %% [markdown]
# ## Same thing for new_cases
covid_ds.dropna(subset=["new_cases"], inplace=True)
print (covid_ds.isnull().sum(axis=0))

# %% [markdown]
# ## Examine the dataframe without missing data
covid_ds.describe(include="all")

# %% [markdown]
# ## Look for cases when there are more new cases than new tests
covid_ds.loc[covid_ds["new_cases"] > covid_ds["new_tests"]]

# %% [markdown]
# ## Remove those records
covid_ds.drop(covid_ds[covid_ds["new_cases"] > covid_ds["new_tests"]].index, inplace=True)
covid_ds.loc[covid_ds["new_cases"] > covid_ds["new_tests"]]

# %% [markdown]
# ## Examine dataframe without those records
covid_ds.describe(include="all")

# %% [markdown]
# ## Look for cases when there are exactly the same new cases than new tests
covid_ds.loc[covid_ds["new_cases"] == covid_ds["new_tests"]]

# %% [markdown]
# ## Look for cases when there are negative values
# New Cases
print(covid_ds.loc[covid_ds["new_cases"] < 0].count())

# %% [markdown]
# New tests
print(covid_ds.loc[covid_ds["new_tests"] <= 0].count())

# %% [markdown]
# ## Remove records with negative new_cases
covid_ds.drop(covid_ds[covid_ds["new_cases"] < 0].index, inplace=True)
print(covid_ds.loc[covid_ds["new_cases"] < 0].count())

# %% [markdown]
# ## Examine the dataframe without those records
covid_ds.describe(include="all")

# %% [markdown]
# ## List records by country
covid_ds.groupby(["location"])["location"].count()

# %% [markdown]
# ## Create the new percentage column
covid_ds["test_pct"] = covid_ds["new_cases"] / covid_ds["new_tests"] * 100
covid_ds.describe(include="all")

# %% [markdown]
# ## Sample result
covid_ds.head(10)

# %% [markdown]
# ## Positive tests percentage by county
covid_ds.groupby(["location"])["test_pct"].mean().reset_index().sort_values(["test_pct"], ascending=False)

# %% [markdown]
# ## Positive tests percentage by county just in october
oct = covid_ds.loc[(covid_ds["date"] >= "2020-10-01") & (covid_ds["date"] <= "2020-10-31")] \
    .groupby(["location"])["test_pct"] \
    .mean() \
    .reset_index() \
    .sort_values(["test_pct"], ascending=False)
oct

# %% [markdown]
# ## Import matplotlib
import matplotlib.pyplot as plt

# %% [markdown]
# ## Create the plot
oct_plot = oct.head(20).plot(x ="location", y="test_pct", kind = "bar")
plt.xticks(rotation=90)
plt.title("COVID-19 data results")
plt.legend(["Octuber"])
plt.xlabel("Countries")
plt.ylabel("cases vs. test ratio in %")
plt.show()
