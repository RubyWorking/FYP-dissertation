import pandas as pd
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Assume the data file we want to process has been uploaded and read
file_path = 'Blossoms_Food_Tiktok4.xlsx'
data = pd.read_excel(file_path)

# Expanded keyword list
keywords = [
    "打卡了", "刚去", "吃了", "去过", "吃过", "好吃", "去吃", "想吃", "超想吃", "度假", "出游",
    "旅游", "打卡", "景点", "想去", "去玩", "参观", "游玩", "去看看", "旅行", "度假", "出游", 
    "探险", "游览", "美景", "景区", "名胜", "胜地", "行程", "攻略", "路线", "预订", 
    "游客", "导游", "走走", "好玩", "放松", "休闲", "太美了", "必须去", "不能错过", "好想去", 
    "真的不错", "绝了", "爱了", "值得一去"
]
emojis = ["[比心]", "[赞]", "[强]", "[舔屏]", "[爱心]", "[送心]", "[玫瑰]"]  # Example emojis
special_phrases = ["【发表图片】"]  # Phrases containing image posts

def label_by_keywords(comment, keywords, emojis, special_phrases):
    # Check if it contains the @ symbol
    if "@" in comment:
        return 1
    
    # Check if it contains emojis
    for emoji in emojis:
        if emoji in comment:
            return 1
    
    # Check if it contains special phrases like 【发表图片】
    for phrase in special_phrases:
        if phrase in comment:
            return 1
    
    # Check if it contains keywords
    for keyword in keywords:
        if keyword in comment:
            return 1
    
    # If none of the above conditions are met, label as 0
    return 0

# Relabel the data
data['label'] = data['评论'].apply(lambda x: label_by_keywords(str(x), keywords, emojis, special_phrases))

# Remove duplicate and blank comments
data_cleaned = data.dropna(subset=['评论']).drop_duplicates(subset=['评论'])

# Perform word segmentation on comments
data_cleaned['评论_分词'] = data_cleaned['评论'].apply(lambda x: " ".join(jieba.cut(x)))

# Vectorize the text using TF-IDF
tfidf_vectorizer = TfidfVectorizer(max_features=5000)
X = tfidf_vectorizer.fit_transform(data_cleaned['评论_分词'])

# Build training and test sets
y = data_cleaned['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the random forest model
rf_model = RandomForestClassifier(class_weight='balanced', random_state=42)

# Train the model
rf_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = rf_model.predict(X_test)

# Output the classification report
print(classification_report(y_test, y_pred))
