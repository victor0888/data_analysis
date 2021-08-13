import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels
import math
import matplotlib.ticker as tkr
from numpy import median




species = pd.read_csv(r"Medical\\DataCleaning\\DataTransformation\\BiodiversityEndangeredAnimalsProject\\species_info.csv")
observations = pd.read_csv(r"Medical\\DataCleaning\\DataTransformation\\BiodiversityEndangeredAnimalsProject\\observations.csv")
print(species.head())
print(observations.head())




species.conservation_status = species.conservation_status.fillna('Unknown')
print(f"Total number of conservation statuses:{species.conservation_status.nunique()}")
print(f"Conservation Statuses: {species.conservation_status.unique()}")

species.fillna('', inplace=True)
observations.fillna('', inplace=True)

print(observations.dtypes)




'''
Next, there will be a check for the dimensions of the data sets, for species there are 5,824 rows and 4 columns while observations has 23,296 rows and 3 columns.
'''

print(f"species shape: {species.shape}")
print(f"observations shape: {observations.shape}")



''' 
First we will find the number of distinct species in the data. 
We will use the column scientific_name to get 5,541 unique species. T
here seems to be a lot of species in the national parks!
'''

print(f"number of species:{species.scientific_name.nunique()}")




'''
Now let's check the number of categories that are represented in the data and there are 7 including animals and plants.
'''

print(f"nnumber of categories:{species.category.nunique()}")
print(f"categories:{species.category.unique()}")




'''
Chaeck the actual number of species per category in the data. 
Vascular plants are the largest share of species with 4,470 in the data, while reptiles being the fewest with 79.
'''
print(species.groupby("category").size())




'''
Next a count of the number of observations in the breakdown of the categories in conservation_status is done. There are 5,633 nan values which means that they are species without concerns. On the other hand there are 161 species of concern, 16 endangered, 10 threatened, and 4 in recovery.

Note: In most cases coming across nan values must be treated carefully, but the absence of data here means that these species are not under any conservation status.
'''
print(species.groupby("conservation_status").size())



'''
The next section looks at observations data. 
The first task is to check the number of parks that are in the dataset and there are only 4 national parks.
'''

print(f"number of parks:{observations.park_name.nunique()}")
print(f"unique parks:{observations.park_name.unique()}")




'''
Total number of observations.
'''
print(f"The total number of observations is: {observations.observations.sum()}")




conservationByStatus = species[species.conservation_status != "Unknown"].groupby(["conservation_status", "category"])["scientific_name"].count().unstack()

print(conservationByStatus)




ax = conservationByStatus.plot(kind = 'bar', figsize=(8,6), 
                               stacked=True)
ax.set_xlabel("Conservation Status")
ax.set_ylabel("Number of Species")
plt.show()



'''
The next question is if certain types of species are more likely to be endangered?
This can be answered by creating a new column called is_protected and include any species that had a value other than No Intervention.
'''

species['is_protected'] = species.conservation_status != "Unknown"




category_counts = species.groupby(['category', 'is_protected'])                        .scientific_name.nunique()                        .reset_index()                        .pivot(columns='is_protected',
                                      index='category',
                                      values='scientific_name')\
                        .reset_index()
category_counts.columns = ['category', 'not_protected', 'protected']

print(category_counts)




'''
Calculate the percentage of species that are protected per category
'''
category_counts["category_protected_tate"] = category_counts.protected / (category_counts.protected + category_counts.not_protected)* 100

print(category_counts)




'''
Statistical Significance
Here we will run a chi-squared tests to see if different species have statistically significant differences in conservation status rates. 
To run a chi squared test, a contingency table will need to be created. 

The first test will be called contingency1 and will need to be filled with the correct numbers for mammals and birds.

The results from the chi-squared test returns many values, the second value which is 0.69 is the p-value. 
The standard p-value to test statistical significance is 0.05. 
For the value retrieved from this test, the value of 0.69 is much larger than 0.05. 
In the case of mammals and birds there doesn't seem to be any significant relationship between them i.e. the variables independent.
'''
from scipy.stats import chi2_contingency

first_contingency = [[30, 146]], [[75,413]]

print(chi2_contingency(first_contingency))



'''
The next pair, is going to test the difference between Reptile and Mammal.
This time the p-value is 0.039 which is below the standard threshold of 0.05 which can be take that the difference between reptile and mammal is statistically significant. 
Mammals are shown to have a statistically significant higher rate of needed protection compared with Reptiles.
'''

second_contingency = [[30, 146]], [[5,73]]

print(chi2_contingency(second_contingency))




'''
The next set of analysis will come from data from the conservationists as they have been recording sightings of different species at several national parks for the past 7 days.

The first step is to look at the the common names from species to get an idea of the most prevalent animals in the dataset. 
The data will be need to be split up into individual names.
'''
from itertools import chain
import string

def split_names(txt):
    for punctuation in string.punctuation:
        txt = txt.replace(punctuation, '')
    return txt

common_names = species[species.category == "Mammal"].common_names.apply(split_names).str.split().tolist()

print(common_names[0:6])




'''
Now we can clean up all the duplicate words in each row since they should no be counted more than once per species.
'''

cleanrow = []

for word in common_names:
    word = list(dict.fromkeys(word))
    cleanrow.append(word)
    
print(cleanrow[0:6])




'''
Now we create one list, which will be easier to manipulate.
'''

one_list = list(chain.from_iterable(i if isinstance(i, list) else [i] for i in cleanrow))

print(one_list[0:10])



'''
Now the data is normalized and ready to count, we can calculate the number of occurrences of each word. 
From this analysis, it seems that Bat occurred 23 times while Shrew came up 18 times.
'''
word_count = []
for i in one_list:
    x = one_list.count(i)
    word_count.append((i,x))
    
print(pd.DataFrame(set(word_count), columns=['Word','Total']).sort_values('Total', ascending = False).head(20))
    



'''
In the data, there are multiple different scientific names for different types of bats. 
The next step is to figure out which rows of species are referring to bats. 
A new column made up of boolean values will be created to check if is_bat is True.
'''

species["is_bat"] = species.common_names.str.contains(r"\bBat\b", regex = True)

print(species.head(15))




'''
Print all the bat species.
'''

print(species[species.is_bat == True])



'''
Now we can merge bats with observations to create a new dataframe that include all observations accross the national park for bat species.
'''

bat_observations = observations.merge(species[species.is_bat])

print(bat_observations)




'''
How many total bat observations(across all species) were made at each national park.

The total number of bats observed in each park over the past 7 days are in the table below. Yellowstone National Park seems to have the largest with 8,362 observations and the Great Smoky Mountains National Park having the lowest with 2,411.
'''

print(bat_observations.groupby('park_name').observations.sum().reset_index())




'''
How many for each park broken down by protected bats vs. non-protected bat sightings. 
It looks like each park except for the Great Smoky Mountains National Park has more sightings of protected bats than not. 
This could be considered a hopefull sign for bats populations.
'''

obs_by_park = bat_observations.groupby(['park_name', 'is_protected']).observations.sum().reset_index()

print(obs_by_park)




'''
Below is a plot from the output of the last data manipulation. 
From this chart one can see that Yellowstone and Bryce National Parks seem to be doing a great job with their bat populations since there are more sightings of protected bats compared to non-protected species. 
The Great Smoky Mountains National Park might need to beef up there efforts in conservation as they have seen more non-protected species.
'''

plt.figure(figsize=(16, 4))
sns.barplot(x=obs_by_park.park_name, y= obs_by_park.observations, hue=obs_by_park.is_protected)
plt.xlabel('National Parks')
plt.ylabel('Number of Observations')
plt.title('Observations of Bats per Week')
plt.show()



'''
Conclusions
The project was able to make several data visualizations and inferences about the various species in four of the National Parks that comprised this data set.

This project was also able to answer some of the questions first posed in the beginning:

What is the distribution of conservation status for species?
The vast majority of species were not part of conservation.(5,633 vs 191)
Are certain types of species more likely to be endangered?
Mammals and Birds had the highest percentage of being in protection.
Are the differences between species and their conservation status significant?
While mammals and Birds did not have significant difference in conservation percentage, mammals and reptiles exhibited a statistically significant difference.
Which animal is most prevalent and what is their distribution amongst parks?
the study found that bats occurred the most number of times and they were most likely to be found in Yellowstone National Park.
'''

