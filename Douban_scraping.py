import time
import random
from DataRecorder import Recorder
from DrissionPage import WebPage
import re


def crawl(id111):
    # Construct the URL for the movie review page
    link = f'https://movie.douban.com/subject/{id111}/reviews?start=1700'
    page.get(link)
    name = page.title
    # Initialize the data recorder, saving data to an Excel file
    recorder = Recorder(f'{name}.xlsx', cache_size=100)
    recorder.set.head(("Nickname", "Time", "Content", "Rating", "Useful Count", "Useless Count", "Reply Count", "IP"))
    number = 0
    # Loop through each page of reviews, up to 10,000 pages
    for i in range(1, 10001):
        try:
            # Get the current page
            page.get(link)
        except:
            print("All links have been accessed!")
        else:
            try:
                # Get the review list from the page
                div = page.ele('x://*[@id="content"]/div/div[1]/div[1]')
                elements = div.eles('tag:div@@class=main review-item')
            except:
                print("Failed to retrieve page content list....")
                break
            else:
                # If the page has no content, exit the loop
                if len(elements) == 0:
                    print("Page content is 0")
                    break
                else:
                    ids = []
                    # Collect all review IDs
                    for element in elements:
                        id_ = element.attr('id')
                        ids.append(id_)
                    recorder.record()
                    try:
                        # Get the link to the next page
                        numbers = re.findall("start=(\d+)", page('Next page>').attr('href'))[0]
                        link = f"https://movie.douban.com/subject/{id111}/reviews?start=" + numbers
                        print(link)
                    except:
                        print("Failed to get the next page address")
                        break
                    else:
                        print("Next page address successfully obtained::", link)
                    print("Fetching detailed information for this page:")
                    # Get detailed information for all reviews on the current page
                    for id in ids:
                        try:
                            # Access the detailed information page for a single review
                            info_link = f'https://movie.douban.com/review/{id}/'
                            page.get(info_link)
                            nick_name = page.ele(f'x://*[@id="{id}"]/header/a[1]/span', timeout=2).text  # Get nickname
                            content = page.ele(f'x://*[@id="link-report-{id}"]', timeout=2).text  # Get review content
                            create_time = page.ele(f'x://*[@id="{id}"]/header/div/span[1]', timeout=2).text  # Get review time
                            score_level = page.ele(f'x://*[@id="{id}"]/header/span[2]', timeout=2).text  # Get rating
                            useful_count = page.ele('@class=btn useful_count ', timeout=2).text.replace('Useful', '')  # Useful count
                            useless_count = page.ele('@class=btn useless_count ', timeout=2).text.replace('Useless', '')  # Useless count
                            reply_count = page.ele('@class=react-num', timeout=2).text  # Reply count
                            ip = page.eles('x://div[@class="main-meta"]//span', timeout=2)[-1].text  # Get IP address
                        except Exception as e:
                            pass
                        else:
                            number += 1
                            print(number, 'id:', id, nick_name, create_time, 'Content has been omitted....')
                            # Add review information to the recorder
                            recorder.add_data((
                                nick_name, create_time, content, score_level, useful_count, useless_count,
                                reply_count, ip))
                    recorder.record()  # Save the data for the current page
    recorder.record()  # Final data save


if __name__ == '__main__':
    # Initialize the WebPage object and open the Douban homepage
    page = WebPage('d')
    url = 'https://www.douban.com/'
    page.get(url)
    input('Press Enter after logging in:')  # Wait for the user to complete the login
    id111 = input('Movie ID:')  # Enter the movie ID
    crawl(id111=id111)  # Start crawling reviews
    # page.quit(force=True)
# url=[34794707,25907063,27180943,24827387，27186313，26617075，35182499]
