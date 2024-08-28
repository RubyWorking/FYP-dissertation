import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the Excel file
file_path = 'Blossoms_DouBan_Review.xlsx'
df = pd.read_excel(file_path)

# Define a list of food-related keywords mentioned in the drama
drama_food_keywords = ['和平饭店', '至真园', '泡饭', '排骨年糕', '青鱼秃肺拼海参', '红烧划水', '定胜糕', '油墩', 
                        '川沙鸡爪', '牛河', '黄鱼面', '粢饭团', '仙鹤神针', '船王炒饭', '火焰大王蛇', 
                        '三文鱼', '鲇鱼', '茶叶蛋', '火锅', '辣肉面', '宝总套餐']

# Retain only comments that contain food-related keywords
df['food_related'] = df['内容'].apply(lambda x: any(kw in str(x) for kw in drama_food_keywords))
food_related_comments = df[df['food_related']]

# Analysis 1: Relationship between food-related comments and ratings
plt.figure(figsize=(10, 6))
sns.countplot(data=food_related_comments, x='星级')
plt.title('Rating Distribution of Food-related Comments')
plt.xlabel('Rating')
plt.ylabel('Number of Comments')
plt.show()

# Analysis 2: Interaction analysis of food-related comments (Useful Count, Response Count)
# Rename columns to English
food_related_comments = food_related_comments.rename(columns={'有用数': 'Useful Count', '回应数': 'Response Count'})

plt.figure(figsize=(10, 6))
sns.boxplot(data=food_related_comments[['Useful Count', 'Response Count']])
plt.title('Interaction Analysis of Food-related Comments')
plt.ylabel('Counts')
plt.show()

# Analysis 3: Geographic distribution of food-related comments
ip_counts = food_related_comments['IP'].value_counts().head(10)

# Translate IP addresses
from deep_translator import GoogleTranslator
translator = GoogleTranslator(source='zh-CN', target='en')
ip_counts.index = [translator.translate(ip) for ip in ip_counts.index]

plt.figure(figsize=(10, 6))
sns.barplot(x=ip_counts.index, y=ip_counts.values)
plt.title('Top 10 Regions by IP for Food-related Comments')
plt.xlabel('IP Address')
plt.ylabel('Number of Comments')
plt.xticks(rotation=45)
plt.show()

# Analysis 4: Proportion of 5-star ratings in food-related comments
food_related_five_star = food_related_comments[food_related_comments['星级'] == 5]
overall_five_star = df[df['星级'] == 5]

food_five_star_rate = len(food_related_five_star) / len(food_related_comments) * 100
overall_five_star_rate = len(overall_five_star) / len(df) * 100

print(f'Percentage of 5-star ratings in food-related comments: {food_five_star_rate:.2f}%')
print(f'Percentage of 5-star ratings in overall comments: {overall_five_star_rate:.2f}%')

# Visualization comparison: Comparison of 5-star rating percentage between food-related comments and overall comments
plt.figure(figsize=(8, 5))
plt.bar(['Food-related Comments', 'Overall Comments'], [food_five_star_rate, overall_five_star_rate], color=['blue', 'green'])
plt.title('Comparison of 5-star Rating Percentage')
plt.ylabel('5-star Rating Percentage (%)')
plt.show()




# Calculate the average rating
average_rating = df['星级'].mean()
print(f'The average rating of the show is: {average_rating:.2f}')

# Calculate the average rating for food-related comments
average_food_rating = food_related_comments['星级'].mean()
average_food_rating

import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

# Calculate the difference in average ratings
diff = average_food_rating - average_rating

# Set the chart style
sns.set(style="whitegrid")

# Visual comparison
plt.figure(figsize=(8, 6))
bars = plt.bar(['Food-related Comments', 'Overall Comments'], [average_food_rating, average_rating], color=['#4c72b0', '#55a868'])

# Add numerical labels
for bar in bars:
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 0.2, f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=12, color='white')

# Add chart title and axis labels
plt.title('Average Rating Comparison', fontsize=16, fontweight='bold')
plt.ylabel('Average Rating', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Show gridlines
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Statistical test (t-test)
t_stat, p_val = stats.ttest_ind(food_related_comments['星级'], df['星级'])

# Display a more precise p-value
annotation_text = f'Difference between food-related and overall ratings: {diff:.2f}\nT-statistic: {t_stat:.2f}, p-value: {p_val:.10f}'
plt.text(0.5, 0.01, annotation_text, ha='center', va='center', fontsize=12, color='black', transform=plt.gcf().transFigure)

# Save the figure
plt.savefig('average_rating_comparison.png', dpi=300, bbox_inches='tight')

# Display the chart
plt.tight_layout()
plt.show()
