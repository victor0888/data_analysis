import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels
import math
from numpy import median
data = pd.read_csv(r'Medical\\DataCleaning\\life_expectancy_by_country.csv')
data2 = pd.read_csv(r'Medical\\DataCleaning\\DataTransformation\\all_data.csv')
print(data2.head(5))
print(data2.dtypes)
#print(data.head(5))

data = data.rename(columns={"Life Expectancy": "Life_Expectancy"})
life_expectancy = data['Life_Expectancy']

data2 = data2.rename(columns={"Life expectancy at birth (years)": "Life_Expectancy"})
life_expectancy = data2['Life_Expectancy']

#life_expectancy_quartiles = np.quantile(life_expectancy,[0.25,0.5,0.75])
#print(life_expectancy_quartiles)

#gdp = data2.GDP
#median_gdp = np.quantile(gdp,0.5)
#print(median_gdp)
#low_gdp = data2[data2.GDP <= median_gdp]
#high_gdp = data2[data2.GDP > median_gdp]

#low_gdp_quartiles = np.quantile(low_gdp['Life_Expectancy'],[0.25,0.5,0.75])
#print(low_gdp_quartiles)

#high_gdp_quartiles = np.quantile(high_gdp['Life_Expectancy'],[0.25,0.5,0.75])
#print(high_gdp_quartiles)

#plt.hist(high_gdp.Life_Expectancy, alpha = 0.5, label = "High GDP")
#plt.hist(low_gdp.Life_Expectancy, alpha = 0.5, label = "Low GDP")
#plt.legend()
#plt.show()
#plt.clf()

print(np.mean(data2.GDP))
print(np.median(data2.GDP))


# Has life expectancy increased over time in the six nations? - Our observation is that Life expectancy has increased over time for all the six nations.
sns.barplot(data=data2 ,x="Year", y="Life_Expectancy", hue="Country")
plt.xticks(rotation=90)
plt.ylabel("Life Expectancy")
plt.title('Life Expectancy by Country')
plt.show()

# VIOLINE PLOT LIFE EXPECTANCY COMPARISON - The observation here is that Zimbabwe has the lowest Life Expectancy out of all six countries.
fig = plt.subplots(figsize=(15, 10))
sns.violinplot (
    data=data2,
    x='Country' , 
    y='Life_Expectancy', 
    palette="Blues")
plt.ylabel("Life Expectancy")
plt.title('Life Expectancy Distrobution by Country')
plt.savefig("Codecademy_violinplot_Life_Expectancy.png")
plt.show()


# LINE PLOT OF LIFE EXPECTANCY PER YEAR PER COUNTRY - Year by year, the Life Expactancy in Zimabwe has increased beyond 2014.
gr = sns.FacetGrid(

    data2,
    col="Country",
    col_wrap=3,
    height=4
)

gr= (gr.map(plt.plot, "Year", "Life_Expectancy").add_legend())

plt.subplots_adjust(top=0.9)
gr.fig.suptitle("Line Plot for Life Expectancy period of year 2000 to 2015.")
#gr.set_xticklabels(rotation=90)
plt.show()

# Has GDP increased over time in the six nations? - Our observation is that GDP has increased over time for China, USA, Mexico, Chile, and Germany overall. Zimbabwe GDP has been stagnating.
f, ax = plt.subplots(figsize=(10, 15))

ax = sns.barplot(data=data2, x="Country", y="GDP", hue="Year")
plt.xticks(rotation=90)
plt.ylabel("GDP in Trillions of US Dollars")
plt.title('GDP per Year')
plt.savefig("Codecademy_bar_plot_GDP.png")
plt.show()


gr = sns.FacetGrid(

    data2,
    col="Country",
    col_wrap=3,
    height=4
)

gr= (gr.map(plt.plot, "Year", "GDP").add_legend())
plt.subplots_adjust(top=0.9)
gr.fig.suptitle("Line Plot for GDP period of year 2000 to 2015.")
plt.show()

# GDP AND LIFE EXPECTANCY PER YEAR AND COUNTRY - We can clearly find corelation between very low GDP and Life Expectancy for Zimbabwe. However the same does not apply for Chie and Mexico as the GDP for these two countries is relatively low, but life expectancy is 80.5 and 76.7 retrospectively.
gr = sns.FacetGrid(

    data2,
    col='Year', 
    hue='Country',
    col_wrap=4,
    height=2
)

gr= (gr.map(plt.scatter, "GDP", "Life_Expectancy", edgecolor="w").add_legend())

plt.subplots_adjust(top=0.9)
gr.fig.suptitle("Scatter Plot for GDP and Life Expectancy for the period of year 2000 to 2015.")
plt.savefig("codecademy_Scatter_Plots of GDP and Life Expectancy Data.png")
plt.show()

'''
70 is below the first quartile of the high GDP dataset, so it falls in the first quarter of that dataset. 
70 is between the second and third quartile of the low GDP dataset, so it falls in the third quarter.

You can start to build graphs from the data by first importing Matplotlib or seaborn and then making some plots!

Some components that you may want to include:

Has life expectancy increased over time in the six nations?
Has GDP increased over time in the six nations?
Is there a correlation between GDP and life expectancy of a country?
What is the average life expectancy in these nations?


CONCLUSION

Based on the data visuals, it is evidant that there is overall link between the encrease of GDP and Life Expectancy by looking at Countries like Chine that has gone over rapid growth over the period between 2000 and 2015. Same can be confirmed for Zimbabwe where the GDP and Life Expectancy are the lowest out of all six countries in our dataset
'''
