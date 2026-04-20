import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

df = pd.read_csv("company_dataset.csv")

def extract_reviews(x):
    num = re.findall(r'[\d\.]+', str(x))[0]
    if 'k' in str(x).lower():
        return float(num) * 1000
    return float(num)

df['Review_Count_Num'] = df['Review_Count'].apply(extract_reviews)

df['Years_Num'] = df['Years'].str.extract(r'(\d+)').astype(int)

def convert_employees(x):
    x = str(x)
    if '1 Lakh+' in x:
        return 100000
    elif '50k-1 Lakh' in x:
        return 75000
    elif '10k-50k' in x:
        return 30000
    elif '1k-5k' in x:
        return 3000
    else:
        return None

df['Employees_Num'] = df['Employees'].apply(convert_employees)

# 1. PIE CHART (EMPLOYEE WISE)

top_emp = df.sort_values(by='Employees_Num', ascending=False).head(10)

plt.figure(figsize=(8,8))
plt.pie(top_emp['Employees_Num'], labels=top_emp['Name'], autopct='%1.1f%%')
plt.title("Top 10 Companies by Employees")
plt.show()

# 2. FUNNEL CHART (REVIEW WISE)

top_reviews = df.sort_values(by='Review_Count_Num', ascending=False).head(10)

plt.figure(figsize=(8,6))
plt.barh(top_reviews['Name'], top_reviews['Review_Count_Num'], color='skyblue')
plt.gca().invert_yaxis()
plt.title("Funnel Chart (Top 10 by Reviews)")
plt.xlabel("Number of Reviews")
plt.show()

# 3. TOP 10 COMPANY HQ

top10_hq = df[['Name', 'hq']].head(10)

print("\nTop 10 Company Headquarters:\n")
print(top10_hq.to_string(index=False))

# 4. BAR CHART (RATING WISE)

plt.figure(figsize=(12,6))
sns.barplot(x='Name', y='Ratings', data=df.sort_values(by='Ratings', ascending=False), palette='viridis')
plt.xticks(rotation=90)
plt.title("Company Ratings")
plt.show()

# 5. LINE CHART (YEAR WISE)

df_year = df.sort_values(by='Years_Num')

plt.figure(figsize=(12,6))
plt.plot(df_year['Name'], df_year['Years_Num'], marker='o', linestyle='-')
plt.xticks(rotation=90)
plt.title("Company Age (Years)")
plt.ylabel("Years")
plt.grid()
plt.show()