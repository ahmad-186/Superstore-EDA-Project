#!/usr/bin/env python
# coding: utf-8

# In[1]:


import warnings
warnings.filterwarnings('ignore')


# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[3]:


sns.set(style="whitegrid")


# In[4]:


df = pd.read_csv("Sample - Superstore.csv", encoding='ISO-8859-1')


# In[5]:


df


# In[6]:


df.head(3)


# In[7]:


df.columns


# #Shape of Data

# In[8]:


print("Rows and columns : ", df.shape)


# In[9]:


df.info()


# In[10]:


df.describe()


# #Check for Null Values

# In[11]:


df.isnull().sum()


# #Check for Duplicated Values

# In[12]:


df.duplicated().sum()


# Removing Unnecessary columns like Postal Code and Rows ID

# In[13]:


df = df.drop(columns = ["Postal Code"])


# In[14]:


df.info()


# Checking Unique Values in Categorical Columns

# In[15]:


print("Segments : ", df["Segment"].unique())
print("Countries : ", df["Country"].unique())
print("Region : ", df["Region"].unique())
print("Categories : ", df["Category"].unique())
print("Sub-Categories : ", df["Sub-Category"].unique())
print("Ship Mode : ", df["Ship Mode"].unique())


# Converting Order Date and Ship Date String to date format

# In[16]:


df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])


# New Columns Order Month and Order Year are created for better analysis

# In[17]:


df["Order Month"] = df["Order Date"].dt.month
df["Order Year"] = df["Order Date"].dt.year


# #### Univariate Analysis
# - (Study of individual columns — one variable at a time)

# ##### Top Categories by Sales

# In[18]:


category_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending = False)
print(category_sales)


# In[19]:


category_sales = category_sales.reset_index()
category_sales


# In[20]:


ax = sns.barplot(x = "Category", y = "Sales", data = category_sales, palette = 'Set2')
for bar in ax.containers:
    ax.bar_label(bar)
plt.title("Top Categories By Sales", fontsize = 16)


# In[21]:


#Graph Show that Technology Category has highest Sales while office supplies have Least Supplies


# ##### Top Sub-Categories By Sales

# In[22]:


sub_categories_sales = df.groupby("Sub-Category")["Sales"].sum().sort_values(ascending = False)
sub_categories_sales


# In[23]:


sub_categories_sales = sub_categories_sales.reset_index()
sub_categories_sales


# In[24]:


plt.figure(figsize = (10,4))
ax = sns.barplot( x = "Sub-Category", y = "Sales", data = sub_categories_sales, color = "#4D55CC")
ax.bar_label(ax.containers[0], rotation = 25)
plt.xticks(rotation = 25)
plt.title("Top Sub-Categories By Sales", fontsize = 16)


# In[25]:


#This Graph shows that Sub-Category Phones, Chairs have highest Sales while Fastners and labels have least Sales


# ##### Top Categories By Profit

# In[26]:


categories_profit = df.groupby("Category")["Profit"].sum().sort_values(ascending = False)
categories_profit


# In[27]:


ax = sns.barplot(x = categories_profit.index, y = categories_profit.values, palette = 'Set2' )
for bar in ax.containers:
    ax.bar_label(bar)
plt.title("Profit By Category", fontsize = 16)
plt.tight_layout()


# In[28]:


# Profit of Category Technology is highest while furniture category have least profit despite having good sales (more than oofice supplies)


# ##### Profit By Sub Categories

# In[29]:


sub_categories_profit = df.groupby("Sub-Category")["Profit"].sum().sort_values(ascending = False)
sub_categories_profit


# In[30]:


sub_categories_profit = sub_categories_profit.reset_index()
sub_categories_profit


# In[31]:


plt.figure(figsize = (10,5))
ax = sns.barplot( x = "Sub-Category", y = "Profit", data = sub_categories_profit, color = "#4D55CC")
ax.bar_label(ax.containers[0], rotation = 15)
plt.title("Profit By Sub-Category", fontsize = 16)
plt.tight_layout()
plt.xticks(rotation = 20)


# In[32]:


# According to this Sub-Category Copier have highest profit despite average sales compared to other sub-categories. 
# While Supplies, Bookcases and Tables have negative profit (loss) 


# #### Segment Distribution

# In[33]:


segment_counts = df["Segment"].value_counts()
segment_counts


# In[34]:


plt.pie(segment_counts, labels = segment_counts.index, autopct = '%1.1f%%', startangle = 90, shadow = True)
plt.title("Segment Distribution")


# #Segment Conumer have highest (51.9%) orders 

# #### Ship Mode Distribution

# In[35]:


ax = sns.countplot(x = "Ship Mode", data = df, palette = 'Set2')
for bar in ax.containers:
    ax.bar_label(bar)
ax.bar_label(ax.containers[1])
plt.title("Order Count by Shipping Mode")
plt.xlabel("Shipping Mode")
plt.ylabel("Number of Orders")


# Insights:
# - According to Shipping Mode Standard class have highest orders while same day shipping mode have least number of orders
# - Issue with Same day delivery

# #### Bivariate Analysis

# - Comparing two variables to find relationships

# #### Sales vs Profit

# In[36]:


plt.figure(figsize = (10,6))
sns.scatterplot(x = "Sales", y = "Profit", data = df, hue = "Category")
plt.title("Sales and Profit by Category")


# Insights:
# 1) Points with very high sales but negative profit show loss-making large orders.
# 2) There are many orders with small sales but decent profit, indicating frequent small but profitable orders.
# 3) There are many points with sales but negative profit	
# 4) Furniture points mostly below profit axis. Furniture may have low or negative profit margins.
# 5) Technology cluster in high profit zone.	
# 6) Technology may be the most profitable category.
# 

# #### Discount vs Profit

# In[37]:


plt.figure(figsize = (10, 6))
sns.scatterplot(x = "Discount", y = "Profit", data = df, hue = 'Category')
plt.title("Discount vs Profit")
plt.xlabel("Discount")
plt.ylabel("Profit")


# Insights: 
# 1) High Discount Price result into Negative profit or loss
# 2) Issue with Furniture Category even at low discount not producing enough profit
# 3) Profit > 0.2 result in making loss or negative profit
# 

# #### Region vs Sales

# In[38]:


region_sales = df.groupby("Region")["Sales"].sum().sort_values()
region_sales = region_sales.reset_index()
region_sales


# In[39]:


ax = sns.barplot(x = "Region", y = "Sales", data = region_sales, palette = "viridis")
for bar in ax.containers:
    ax.bar_label(bar)


# #### Sales and Profit By Region

# In[40]:


# Step 1: Grouped data
region_sales = df.groupby("Region")[["Sales", "Profit"]].sum()
region_sales


# In[41]:


# Step 2: Create position index
regions = region_sales.index
sales = region_sales['Sales']
profit = region_sales['Profit']

bar_width = 0.4
index = np.arange(len(regions))  # Position for each region

# Step 3: Plot
plt.figure(figsize=(10, 6))

# Plot sales bars
plt.barh(index, sales, height=bar_width, label='Sales', color='skyblue')

# Plot profit bars, offset by bar_width
plt.barh(index + bar_width, profit, height=bar_width, label='Profit', color='lightgreen')

# Step 4: Y-axis labels and formatting
plt.yticks(index + bar_width / 2, regions)
plt.xlabel("Amount")
plt.title("Sales and Profit by Region")
plt.legend()

plt.tight_layout()
plt.show()


# Insights:
# - Central Region generate decent Sales but still not able to generate healthy Profit
# - West Region generate high sales and High profit

# #### Region vs Discount

# In[42]:


region_discount = df.groupby("Region")["Discount"].sum()
region_discount = region_discount.reset_index()
region_discount


# In[43]:


ax = sns.barplot(x = "Region", y = "Discount", data = region_discount, palette = "viridis")
for bar in ax.containers:
    ax.bar_label(bar)


# Insights:
# - South Region offer least discount but still generate less profit 
# - Reason for least proit generation in Central Region is due to High Discount they offer
# - West and East Region Offer Decent discount and generate healthy profit

# #### Order Year vs Total Sales

# In[44]:


year_sales = df.groupby("Order Year")["Sales"].sum()


# In[45]:


year_sales


# In[46]:


year_sales.plot(kind = 'line', marker = 'o', color = 'green')
plt.title("Year-Wise Sales Trend")
plt.xlabel("Year")
plt.ylabel("Total Sales")
plt.grid(True)


# Order vs Sales line plot shows that Sales decreses first year then increases over the year

# #### Order Year vs Total Profit

# In[47]:


year_profit = df.groupby("Order Year")["Profit"].sum()


# In[48]:


year_profit


# In[49]:


year_profit.plot(kind = 'line', marker = 'o', color = 'green')
plt.title("Year-Wise Profit Trend")
plt.xlabel("Year")
plt.ylabel("Total Profit")
plt.grid(True)


# Order vs Year Plot Shows that profit increases over the year

# #### Correlation Heat Map

# In[50]:


corr = df[['Sales', 'Quantity', 'Discount', 'Profit']].corr()
corr


# In[51]:


sns.heatmap(corr, annot = True, cmap = "coolwarm", linewidth = 0.5)
plt.title("Correlation Heat Map")


# Heat Map shows that:
# - Sales and profit shows moderate positive correlation.
# - Discount and profit show moderate negative correlation

# ### Final Insight Summary
# #### Key Visualizations:
# - Bar plots (Sales & Profit by Category/Sub-Category)
# - Pie chart (Segment distribution)
# - Countplot (Shipping modes)
# - Scatter plots (Sales vs Profit, Discount vs Profit)
# - Line chart (Sales over years)
# - Heatmap (Correlation between numeric features)
# #### Business Insights
# ##### Sales vs Profit:
# - High sales ≠ high profit. Many large orders lead to losses.
# - Technology is the most profitable category.
# - Furniture often causes loss even at low discounts.
# ##### Discount Analysis:
# - Discounts above 20% generally lead to negative profits.
# - Central Region offers high discounts and suffers poor profits.
# ##### Regional Insights:
# - West: Highest sales & highest profit
# - Central: Decent sales but lowest profit (due to discounts)
# - South: Least sales and discount — could need marketing push
# ##### Sales Over Time:
# - Sales are growing year-over-year, showing positive business growth.
# ##### Heatmap Takeaway:
# - Discount & Profit have a strong negative correlation.
# - Sales & Profit show a moderate positive relationship.
