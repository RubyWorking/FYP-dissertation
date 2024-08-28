import pandas as pd
import jieba
import jieba.posseg as pseg  # Import part-of-speech tagging module
from collections import Counter
from deep_translator import GoogleTranslator
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re

# Read the Excel file
file_path = 'Blossoms_DouBan_Review.xlsx'
df = pd.read_excel(file_path)

# Add custom words
custom_words = ['和平饭店', '至真园', '泡饭', '排骨年糕', '蓝鱼秃肺拼海参', '红烧划水', '定胜糕', '油墩子', '川沙鸡爪', 
                '牛河', '黄鱼面', '饭团', '鹤针', '舟王炒饭', '炎王蛇', '三文鱼', '鲶鱼', '茶叶蛋', '火锅', '辣肉面', '包子']
for word in custom_words:
    jieba.add_word(word)

# Get the comment content column and convert it to string type
comments = df['内容'].astype(str)

# Text preprocessing: word segmentation and part-of-speech tagging, remove names and organization names, but keep place names
filtered_words = []
for comment in comments:
    words = pseg.cut(comment)  # Use jieba for word segmentation and part-of-speech tagging
    for word, flag in words:
        # If it's a custom word, keep it regardless of its part-of-speech tag
        if word in custom_words:
            filtered_words.append(word)
        # Otherwise, only keep common nouns, proper nouns, idiomatic expressions, and place names
        elif flag in ('n', 'nz', 'ng', 'ns'):  
            filtered_words.append(word)

# Read the extended stop words file
with open('cn_stopwords.txt', 'r', encoding='utf-8') as f:
    file_stop_words = set(f.read().splitlines())

# Define and extend the stop words list, including words related to film and television
custom_stop_words = set([
    '的', '了', '和', '是', '我', '也', '在', '有', '就', '不', '人', '都', '这个', '上', '很', '你', '他', '她',
    '它', '我们', '他们', '她们', '自己', '所以', '因为', '这样', '这里', '那里', '什么', '但是', '如果', '那么', '有点',
    '还是', '虽然', '不过', '而且', '并且', '关于', '其中', '甚至', '一些', '还有', '或者', '所以', '其实', '另外', '其实',
    '以及', '就是', '与', '就', '最', '已经', '非常', '那么', '而', '并', '还', '其中', '所有', '所有的', '还有', '只是',
    '几乎', '其他', '而且', '但', '呢', '却', '哇', '哈', '吧', '啊', '的', '嘞', '啦', '吗', '呀',
    '剧名', '作者', '人物', '故事', '剧情', '电影', '导演', '演员', '编剧', '观众', '影视', '小说', '雪芝', '原著', '作品', '画面', '感觉',
    '影片', '电视', '剧集', '电视剧', '台词', '镜头', '角色', '导演', '男主', '女主', '男人', '女人', '男性', '女性', '主角', '繁花', '版权', '剧中', '关系', '先生', '爷叔', '形式'
])

# Combine custom stop words and stop words from the file
stop_words = custom_stop_words.union(file_stop_words)

# Filter out stop words and words with length less than 2
filtered_words = [word for word in filtered_words if word not in stop_words and len(word) > 1]

# Check the filtered word list
print(filtered_words[:200])  # Print the first 200 words to check the filtering effect

# Count word frequency
word_freq = Counter(filtered_words)
common_words = word_freq.most_common(30)
print(common_words)


# Use deep_translator to translate high-frequency words
translator = GoogleTranslator(source='zh-CN', target='en')
translated_words = {translator.translate(word): freq for word, freq in common_words}

# Generate a word cloud, using the default font to create an English word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(translated_words)

# # Display the word cloud
# plt.figure(figsize=(10, 5))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis('off')
# plt.show()

# Display the word cloud with a title and annotations
plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # Hide the axis
plt.title('Word Cloud', fontsize=20)  # Add a title and set the font size

plt.savefig('wordcloud.png', format='png', bbox_inches='tight')

plt.show()


# Count the occurrences of custom words
custom_word_counts = {word: filtered_words.count(word) for word in custom_words}

# Print the occurrence count for each custom word
for word, count in custom_word_counts.items():
    print(f"{word}: {count} times")
