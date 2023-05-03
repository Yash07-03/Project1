#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import numpy as np 
from matplotlib import pyplot as plt 
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib
matplotlib.rcParams["figure.figsize"]=(20,10)


# In[2]:


df1 = pd.read_csv("Bengaluru_House_Data.csv")
df1.head()


# In[3]:


df1.tail()


# In[5]:


df1.shape


# In[9]:


df1.groupby('area_type')['area_type'].agg('count')


# In[12]:


df2 = df1.drop(['area_type','society','balcony','availability'],axis='columns')
df2.head()


# In[14]:


df2.isnull().sum()


# In[15]:


df3 = df2.dropna()
df3.isnull().sum()


# In[17]:


df3.shape


# In[18]:


df3['size'].unique()


# In[83]:


df3['bhk'] =df3['size'].apply(lambda x : int(x.split(' ')[0]))
df3.head()


# In[84]:


df4 = df3.drop(['size','BHK'],axis='columns')
df4.head()


# In[85]:


df4[df4.bhk>20]


# In[23]:


df4.total_sqft.unique()


# In[27]:


def isfloat(x):
    try:
        float(x)
    except:
        return False
    return True


# In[86]:


df4[~df4['total_sqft'].apply(isfloat)].head(10)


# In[31]:


def convert_sqft_to_num(x):
    tokens = x.split("-")
    if len(tokens) ==2:
        return (float(tokens[0])+float(tokens[1]))/2
    try:
        return float(x)
    except:
        return None 


# In[87]:


df5 = df4.copy()
df5['total_sqft'] = df5['total_sqft'].apply(convert_sqft_to_num)
df5


# In[88]:


df5.loc[30]


# In[89]:


df6  = df5.copy()
df6['price_per_sqft'] = df6['price']*100000/df6['total_sqft']
df6.head(10)


# In[36]:


df6.total_sqft.unique()


# In[40]:


df6.groupby('location')['location'].agg('count')


# In[41]:


df6.location.unique()


# In[117]:


df6.location = df6.location.apply(lambda x: x.strip())
location_stats = df6.groupby('location')['location'].agg('count').sort_values(ascending = False)
location_stats.head(40)


# In[54]:


len(location_stats[location_stats<=10])


# In[119]:


location_stats_less_than_10 = location_stats[location_stats<=10]
location_stats_less_than_10.head(45)


# In[61]:


df6.location = df6.location.apply(lambda x: 'Other' if x in location_stats_less_than_10 else x)
len(df6.location.unique())


# In[90]:


df6.head(20)


# In[64]:


# Let say Threshold value of per bedroom area  = 300 sq ft


# In[91]:


df6[df6.total_sqft/df6.bhk<300].head()


# In[67]:


# REMOVE OUTLIERS AS IT IS NOT POSSIBLE 


# In[68]:


df6.shape


# In[92]:


df7 = df6[~(df6.total_sqft/df6.bhk<300)]
df7.shape


# In[97]:


df7.price_per_sqft.describe()


# In[98]:


def remove_pps_outliers(df):
    df_out = pd.DataFrame()
    for keys,subdf in df.groupby('location'):
        m = np.mean(subdf.price_per_sqft)
        st = np.std(subdf.price_per_sqft)
        reduced_df = subdf[(subdf.price_per_sqft>(m-st)) & (subdf.price_per_sqft <=(m+st))]
        df_out = pd.concat([df_out,reduced_df],ignore_index=True)
    return df_out
df8 = remove_pps_outliers(df7)
df8.shape


# In[99]:


def plot_scatter_chart(df,location):
    bhk2 = df[(df.location==location) & (df.bhk==2)]
    bhk3 = df[(df.location==location) & (df.bhk==3)]
    matplotlib.rcParams['figure.figsize'] =(15,10)
    plt.scatter(bhk2.total_sqft,bhk2.price,color='blue',label='2 BHK',s = 50)
    plt.scatter(bhk3.total_sqft,bhk3.price,marker='+',color='green',label='3 BHK',s = 50)
    plt.xlabel("Total Square Feet Area")
    plt.ylabel("Price")
    plt.title(location)
    l=plt.legend()
plot_scatter_chart(df8,"Rajaji Nagar")


# In[100]:


plot_scatter_chart(df8,"Hebbal")


# In[78]:


# We should also remove properties where for same locations , the price of (for example) 3 bedroom apartment is less than 
#2 bedroom apartment (with same square ft area). What we wil do is for a given location , we will build a dictionary of stats 
#per bhk i.e 


# In[101]:


def remove_bhk_outliers(df):
    exclude_indices = np.array([])
    for location, location_df in df.groupby('location'):
        bhk_stats = {}
        for bhk, bhk_df in location_df.groupby('bhk'):
            bhk_stats[bhk] = {
                'mean':np.mean(bhk_df.price_per_sqft),
                'std': np.std(bhk_df.price_per_sqft),
                'count':bhk_df.shape[0]
            }
        for bhk, bhk_df in location_df.groupby('bhk'):
            stats = bhk_stats.get(bhk-1)
            if stats and stats['count']>5:
                exclude_indices = np.append(exclude_indices,bhk_df[bhk_df.price_per_sqft<(stats['mean'])].index.values)
    return df.drop(exclude_indices,axis="index")
df9 = remove_bhk_outliers(df8)
df9.shape


# In[102]:


plot_scatter_chart(df9,"Hebbal")


# In[103]:


import matplotlib
matplotlib.rcParams["figure.figsize"] =(20,10)
plt.hist(df9.price_per_sqft,rwidth =0.8)
plt.xlabel("Price Per Square Feet")
plt.ylabel("Count")


# In[104]:


df9.bath.unique()


# In[105]:


df9[df9.bath>10]


# In[106]:


plt.hist(df9.bath,rwidth =0.8)
plt.xlabel("Number of bathroom")
plt.ylabel("Count")


# In[107]:


df9[df9.bath>df9.bhk+2]


# In[109]:


df0 = df9[df9.bath<df9.bhk+2]
df0.shape


# In[110]:


df11 = df0.drop(['price_per_sqft'],axis ="columns")
df11.head()


# In[113]:


dummies = pd.get_dummies(df11.location)
dummies.head(3)


# In[ ]:




