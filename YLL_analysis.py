import numpy as np
import os
from numpy import genfromtxt

################################
################################ path
################################

os.chdir(os.path.realpath(''))

################################
################################ Import Data 
################################
################################ Import cases in Italy as stated in Hanlon et al. (2020)
deaths_male, deaths_female = [], []
data = genfromtxt('italy_data.txt')
for i in range(len(data)):
    deaths_female.append(data[i][1])
    deaths_male.append(data[i][2])

deaths_female = np.array(deaths_female)
deaths_male = np.array(deaths_male)

################################ Using the WHO table from the paper (averaging two age classes to obtain expected years left to live!)
mle = np.zeros(len(deaths_female))
data = genfromtxt('who_table_paper.csv')
for i in range(len(mle)-2):
    mle[i] = (data[2*i+1]+data[2*(i+1)])/2

mle[-1] = data[-1]
mle[-2] = data[-2]

################################
################################ Compute YLL due to SARS-CoV-2 - same result as in Hanlon et al. (2020)
################################
YLL_hanlon_male = np.sum(deaths_male*mle)/np.sum(deaths_male)
YLL_hanlon_fem = np.sum(deaths_female*mle)/np.sum(deaths_female)

print('Hanlon et al. (2020) estimates')
print(YLL_hanlon_male)
print(YLL_hanlon_fem)

################################
################################ Compute YLL with aging as the cause of death (the baseline YLL) 
################################
deaths_male_null, deaths_female_null = [], []
temp_male, temp_female = [],[]
data = genfromtxt('italy_life_table_2016.csv', delimiter=',')
for i in range(int((len(data))/2)):
    temp_male.append(data[2*i][-2])
    temp_female.append(data[2*i+1][-2])

################################ averaging over two age classes to obtain years left to live for a decade + starting with people aged 30 (as was done in the manuscript by Hanlon et al. (2020))
for i in range(len(mle)-1):
    deaths_male_null.append((temp_male[2*i+7]+temp_male[2*i+8])/2)
    deaths_female_null.append((temp_female[2*i+7]+temp_female[2*i+8])/2)

deaths_male_null.append(temp_male[-1])
deaths_female_null.append(temp_female[-1])

deaths_male_null = np.array(deaths_male_null)
deaths_female_null = np.array(deaths_female_null)

male_YLL_null = np.sum(deaths_male_null*mle)/np.sum(deaths_male_null)
female_YLL_null = np.sum(deaths_female_null*mle)/np.sum(deaths_female_null)

print('Null model estimates')
print(male_YLL_null)
print(female_YLL_null)


print('Subtracting the null estimate from Hanlon et al. (2020) results')
print(YLL_hanlon_male - male_YLL_null)
print(YLL_hanlon_fem - female_YLL_null)
