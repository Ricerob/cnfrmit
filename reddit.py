from bs4 import BeautifulSoup
import requests
# import re
from analysis import comment_analysis
# import sys
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from gpapi import GimmeProxyApi

def grab_comments(post_url):
    # Send a GET request to the post URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'https://www.google.com/',
    }
    api = GimmeProxyApi() # initiate the class (you can pass an apikey if you have one)
    random_proxy = api.get_proxy()
    print(random_proxy)
    ip = random_proxy['ip']
    port = random_proxy['port']

    response = requests.get(post_url, headers, proxy=f'https://{ip}:{port}')
    soup = BeautifulSoup(response.text, 'html.parser')

    # # remove script tags
    # for script in soup(["script"]):
    #     script.extract()

    # # print the response without script tags
    # print(soup.text)
    # print(response.status_code)

    # Find the username of the poster
    # post_author_link = soup.find_all('a')
    # print(post_author_link)
    # if post_author_link:
    #     username = post_author_link.text.strip()
    #     print('The username of the poster is:', username)

    with open('example.html', 'w') as file:
        file.write(soup.prettify())

    print(soup.text)

    # Find the comments on the post
    comments = []
    comment_container = soup.find('div', {'id': 'overlayScrollContainer'})
    if comment_container:
        for comment in comment_container.find_all('div', {'class': 'Comment'}):
            comment_author_link = comment.find('a', {'data-testid': 'post-comment-header'})
            if comment_author_link and comment_author_link.text.strip() != username:
                comment_text = comment.find('div', {'data-testid': 'comment'}).find_all('p')
                comments.append('\n'.join([p.text.strip() for p in comment_text]))

    return comments


if __name__ == "__main__":
    link = 'https://www.reddit.com/r/SideProject/comments/1126cue/markwhen_write_markdownish_text_of_events_and/'

    grab_comments(link)