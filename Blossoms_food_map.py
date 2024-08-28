import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Use the actual shapefile path
shapefile_path = r'gadm41_CHN_shp/gadm41_CHN_1.shp'

# Load the shapefile
china_map = gpd.read_file(shapefile_path)

# Assume province_group is the DataFrame you have prepared containing provinces, comment counts, and ratings
province_group = pd.DataFrame({
    'IP': ['上海', '北京', '广东', '江苏', '浙江', '山东', '四川', '辽宁', '湖北', '陕西'],
    'comment_count': [142, 98, 147, 123, 110, 87, 65, 58, 43, 37],
    'avg_rating': [4.5, 4.3, 4.6, 4.4, 4.5, 4.2, 4.4, 4.3, 4.1, 4.2]
})

# Manually adjust the name mapping
province_mapping = {
    '上海': 'Shanghai',
    '北京': 'Beijing',
    '广东': 'Guangdong',
    '江苏': 'Jiangsu',
    '浙江': 'Zhejiang',
    '山东': 'Shandong',
    '四川': 'Sichuan',
    '辽宁': 'Liaoning',
    '湖北': 'Hubei',
    '陕西': 'Shaanxi',
}

# Apply the name mapping
province_group['Province_CN'] = province_group['IP'].map(province_mapping)

# Set province names as index
china_map = china_map.set_index('NAME_1')

# Sort by rating in descending order
province_group = province_group.sort_values(by='avg_rating', ascending=False)
province_group['Rank'] = range(1, len(province_group) + 1)

# Unicode circled number characters
circle_numbers = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩']

# Merge data, using how='left' to retain all provinces
merged_data = china_map.join(province_group.set_index('Province_CN'), how='left')

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(12, 10))

# Plot and display the map, adjust legend size
merged_data.plot(column='avg_rating', ax=ax, cmap='OrRd', edgecolor='black',
                 legend=True, legend_kwds={'orientation': "horizontal", 'shrink': 0.5, 'pad': 0.05},
                 missing_kwds={'color': '#f0f0f0'})

# Add labels for province names and comment counts, avoiding overlap
offsets = {
    'Beijing': (0, 1),
    'Shanghai': (4, -1),
    'Guangdong': (-1, -1),
    'Jiangsu': (1, 1),
    'Zhejiang': (-1, -1),  # Adjust Zhejiang's position to avoid overlap with Shanghai
    'Shandong': (1, 1),
    'Sichuan': (-1, 0),
    'Liaoning': (1, 1),
    'Hubei': (-1, -1),
    'Shaanxi': (1, 0)
}

for idx, row in merged_data.iterrows():
    if pd.notna(row['comment_count']) and pd.notna(row['Rank']):
        rank_index = int(row['Rank']) - 1  # Ensure Rank is an integer and not NaN
        if rank_index < len(circle_numbers):  # Ensure index does not go out of range
            x, y = row['geometry'].centroid.x, row['geometry'].centroid.y
            dx, dy = offsets.get(idx, (0, 0))
            
            # Combine circled number and province name
            label = f"{circle_numbers[rank_index]} {idx}"
            
            # Display province name and comment data on the map
            ax.text(x + dx, y + dy, 
                    f"{label}\n{int(row['comment_count'])} comments\n{row['avg_rating']:.1f} rating",
                    ha='center', va='center', fontsize=8, fontweight='bold',
                    bbox=dict(facecolor='white', alpha=0.5))

ax.set_title("Food-related Comments and Average Rating by Province")
ax.axis('off')

plt.savefig('food_comments_map.png', dpi=300, bbox_inches='tight')

plt.show()
