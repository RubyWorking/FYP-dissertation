import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Assume you have already loaded the data
# Read Excel data
tiktok_data = pd.read_excel('Blossoms_Food_Tiktok4.xlsx')
tiktok_data1 = pd.read_excel('Blossoms_Food_Tiktok1.xlsx')
tiktok_data2 = pd.read_excel('Blossoms_Food_Tiktok2.xlsx')
tiktok_data3 = pd.read_excel('Blossoms_Food_Tiktok3.xlsx')
tiktok_data5 = pd.read_excel('Blossoms_Food_Tiktok5.xlsx')
douban_data = pd.read_excel('Blossoms_DouBan_Review.xlsx')

# Convert the time column to datetime format
tiktok_data['时间'] = pd.to_datetime(tiktok_data['时间'])
tiktok_data1['时间'] = pd.to_datetime(tiktok_data1['时间'])
tiktok_data2['时间'] = pd.to_datetime(tiktok_data2['时间'])
tiktok_data3['时间'] = pd.to_datetime(tiktok_data3['时间'])
tiktok_data5['时间'] = pd.to_datetime(tiktok_data5['时间'])
douban_data['时间'] = pd.to_datetime(douban_data['时间'])

# Select data from the first three months
start_date = '2024-01-01'
end_date = '2024-03-31'

tiktok_data = tiktok_data[(tiktok_data['时间'] >= start_date) & (tiktok_data['时间'] <= end_date)]
tiktok_data1 = tiktok_data1[(tiktok_data1['时间'] >= start_date) & (tiktok_data1['时间'] <= end_date)]
tiktok_data2 = tiktok_data2[(tiktok_data2['时间'] >= start_date) & (tiktok_data2['时间'] <= end_date)]
tiktok_data3 = tiktok_data3[(tiktok_data3['时间'] >= start_date) & (tiktok_data3['时间'] <= end_date)]
tiktok_data5 = tiktok_data5[(tiktok_data5['时间'] >= start_date) & (tiktok_data5['时间'] <= end_date)]
douban_data = douban_data[(douban_data['时间'] >= start_date) & (douban_data['时间'] <= end_date)]

# Aggregate by day and count the number of comments
tiktok_daily_counts1_filtered = tiktok_data1.resample('D', on='时间').size()
tiktok_daily_counts2_filtered = tiktok_data2.resample('D', on='时间').size()
tiktok_daily_counts3_filtered = tiktok_data3.resample('D', on='时间').size()
tiktok_daily_counts4_filtered = tiktok_data.resample('D', on='时间').size()  # Previous tiktok_data is Tiktok4
tiktok_daily_counts5_filtered = tiktok_data5.resample('D', on='时间').size()
douban_daily_counts_filtered = douban_data.resample('D', on='时间').size()

# Set figure size
fig, ax = plt.subplots(figsize=(16, 9))

# Plot the time series
ax.plot(tiktok_daily_counts1_filtered, label='TikTok Food Video Comments 1')
ax.plot(tiktok_daily_counts2_filtered, label='TikTok Food Video Comments 2')
ax.plot(tiktok_daily_counts3_filtered, label='TikTok Food Video Comments 3')
ax.plot(tiktok_daily_counts4_filtered, label='TikTok Food Video Comments 4')
ax.plot(tiktok_daily_counts5_filtered, label='TikTok Food Video Comments 5')

# Highlight Douban Blossoms Reviews line with a thicker and more noticeable color
ax.plot(douban_daily_counts_filtered, label='Douban Blossoms Reviews', linestyle='--', linewidth=3, color='blue')

# Get the peak period for Douban comments
douban_peak = douban_daily_counts_filtered.idxmax()
douban_peak_value = douban_daily_counts_filtered.max()

# Get the peak period for each TikTok comment
tiktok_peak1 = tiktok_daily_counts1_filtered.idxmax()
tiktok_peak_value1 = tiktok_daily_counts1_filtered.max()

tiktok_peak2 = tiktok_daily_counts2_filtered.idxmax()
tiktok_peak_value2 = tiktok_daily_counts2_filtered.max()

tiktok_peak3 = tiktok_daily_counts3_filtered.idxmax()
tiktok_peak_value3 = tiktok_daily_counts3_filtered.max()

tiktok_peak4 = tiktok_daily_counts4_filtered.idxmax()
tiktok_peak_value4 = tiktok_daily_counts4_filtered.max()

tiktok_peak5 = tiktok_daily_counts5_filtered.idxmax()
tiktok_peak_value5 = tiktok_daily_counts5_filtered.max()

# Summarize peak data
peaks = {
    "Source": ["Douban", "TikTok 1", "TikTok 2", "TikTok 3", "TikTok 4", "TikTok 5"],
    "Peak Date": [douban_peak, tiktok_peak1, tiktok_peak2, tiktok_peak3, tiktok_peak4, tiktok_peak5],
    "Peak Value": [douban_peak_value, tiktok_peak_value1, tiktok_peak_value2, tiktok_peak_value3, tiktok_peak_value4, tiktok_peak_value5]
}

peaks_df = pd.DataFrame(peaks)

# Mark the peaks and annotate with the corresponding comment counts
ax.scatter([douban_peak, tiktok_peak1, tiktok_peak2, tiktok_peak3, tiktok_peak4, tiktok_peak5],
           [douban_peak_value, tiktok_peak_value1, tiktok_peak_value2, tiktok_peak_value3, tiktok_peak_value4, tiktok_peak_value5],
           color='red', zorder=5)

# Annotate the specific dates and corresponding comment counts on the graph
for i, txt in enumerate(peaks_df['Peak Date']):
    ax.annotate(f"{txt.strftime('%Y-%m-%d')}\n{peaks_df['Peak Value'][i]} comments", 
                (peaks_df['Peak Date'][i], peaks_df['Peak Value'][i]), 
                textcoords="offset points", xytext=(0,10), ha='center', fontsize=10, color='black')

# Set title and labels, move the title upwards
ax.set_title('Time Series Analysis of Douban and TikTok Comments with Peak Dates (First 3 Months)', fontsize=16, pad=30)
ax.set_xlabel('Date', fontsize=14)
ax.set_ylabel('Number of Comments', fontsize=14)

# Set the date format
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))

# Rotate date labels for readability
plt.xticks(rotation=45)

# Add legend
ax.legend(fontsize=12)

# Show grid
ax.grid(True)

# Adjust figure margins
plt.subplots_adjust(left=0.1, bottom=0.2)

# Save the chart
plt.savefig('time_series_analysis.png', dpi=300)

plt.show()





# Align the data to ensure dates are aligned, dropna() is used to remove dates with no data
aligned_data = pd.concat([douban_daily_counts_filtered, tiktok_daily_counts1_filtered,
                          tiktok_daily_counts2_filtered, tiktok_daily_counts3_filtered,
                          tiktok_daily_counts4_filtered, tiktok_daily_counts5_filtered], axis=1).dropna()

# Rename columns
aligned_data.columns = ['Douban', 'TikTok 1', 'TikTok 2', 'TikTok 3', 'TikTok 4', 'TikTok 5']

# Calculate correlations
correlations = aligned_data.corr().loc['Douban', ['TikTok 1', 'TikTok 2', 'TikTok 3', 'TikTok 4', 'TikTok 5']]

# Convert the result to a DataFrame
correlations_df = correlations.reset_index()
correlations_df.columns = ["TikTok Data", "Correlation with Douban"]

# Plot a bar chart to show the correlation between TikTok comments and Douban comments
plt.figure(figsize=(10, 6))
plt.bar(correlations_df["TikTok Data"], correlations_df["Correlation with Douban"], color='skyblue')

# Add numerical labels on top of each bar
for i, v in enumerate(correlations_df["Correlation with Douban"]):
    plt.text(i, v + 0.02, f"{v:.2f}", ha='center', fontsize=12)

# Set title and axis labels
plt.title('Correlation between Douban and TikTok Comments', fontsize=16)
plt.xlabel('TikTok Data', fontsize=14)
plt.ylabel('Correlation Coefficient', fontsize=14)

# Save the figure
plt.savefig('correlation_analysis.png', dpi=300, bbox_inches='tight')

# Show the chart
plt.ylim(0, 1)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
