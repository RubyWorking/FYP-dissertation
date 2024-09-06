from DrissionPage import ChromiumPage
from DrissionPage.common import Actions
import random
import datetime
import time
import pandas as pd
from tqdm import *

# Initialize a ChromiumPage object
page = ChromiumPage()

# Open the Douyin website
page.get("https://www.douyin.com")

# Wait for the user to log in and then press Enter
input("登陆后回车：")

# Input the URL of the video to collect comments from
url = input("请输入要采集视频的url:")

# Input the number of comments to collect
num = int(input("请输入要采集的条数："))

# Navigate to the provided URL
page.get(url)

# Input the file name for saving the data
title = input("请输入文件名称：")

# Start listening for network requests to the comments endpoint
page.listen.start(targets="https://www.douyin.com/aweme/v1/web/comment/list/?")

# Click on the comment section to load comments
page.ele('x://*[@id="sliderVideo"]/div[1]/div[1]/div/div[1]/div[2]/div[3]/div/div[2]').click()

# Initialize counters and list to store comment data
nums = 0
info_lists = []

# Loop through the number of pages (each page contains 20 comments)
for i in tqdm(range(num // 20 + 1)):
    # Wait for a random time between 1 and 2 seconds
    page.wait(random.randint(1, 2))
    
    # Wait for the network request to complete and get the response
    res = page.listen.wait()
    
    # Scroll down to load more comments
    page.actions.move_to('x://*[@id="merge-all-comment-container"]/div/div[3]')
    page.actions.scroll(5000, 0)
    
    # Extract comments from the response
    comments = res.response.body["comments"]
    
    # Process each comment
    for i in comments:
        name = i["user"]["nickname"]  # User nickname
        province = i["ip_label"]  # User province label
        comment = i["text"]  # Comment content
        time = datetime.datetime.fromtimestamp(i["create_time"])  # Comment timestamp
        
        # Check if the comment contains an image
        try:
            img = i["image_list"][0]["medium_url"]
            comment = str(comment) + "【发表图片】"  # Append a note indicating the presence of an image
        except Exception as e:
            pass
        
        # Number of replies to the comment
        reply_comment_total = i["reply_comment_total"]
        
        # Number of likes on the comment
        digg_count = i["digg_count"]
        
        # Update comment count and add the comment details to the list
        nums += 1
        info_lists.append([name, province, comment, time, reply_comment_total, digg_count])
    
    # Check if there are no more comments to load
    try:
        if page.ele("text:No further comments for now", timeout=1):
            break
    except Exception as e:
        pass

# Print the total number of collected comments
print("The final number of collected items is：", nums)

# Save the collected data to an Excel file
df = pd.DataFrame(info_lists, columns=[ 'province', 'comment', 'time', "replies", "Number of likes"])
df.to_excel(f"{title}.xlsx", index=False)
