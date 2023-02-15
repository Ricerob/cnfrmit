from bs4 import BeautifulSoup
import requests
import re
from analysis import comment_analysis
import sys

def get_poster_username(soup):
    author_div = soup.find('div', {'class': 'post-page__inline-author'})
    author_a = author_div.find('a')
    href = author_a['href']
    username = re.search('(?<=\/)[^\/]+(?=\?)', href).group(0)
    return username

def get_comments(soup, poster_username):
    comment_divs = soup.find_all('div', {'class': 'comment__main'})
    comments = []
    for div in comment_divs:
        # check if comment was posted by the same user
        author_a = div.find('a', {'class': 'user-link__link'}, href=True)
        if author_a:
            author_href = author_a['href']
            author_username = re.search('(?<=\/)[^\/]+(?=\?)', author_href).group(0)
            if author_username == poster_username:
                continue
        
        # extract comment text
        p_tags = div.find_all('p')
        comment_text = '\n'.join([p.text for p in p_tags])
        if comment_text.strip() == 'This comment has been voted down. Click to show.':
            continue
        comments.append(comment_text)
        
    return comments

def grab_comments(link):
    # send GET request to link and retrieve HTML content
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')

    # get the username of the poster
    poster_username = get_poster_username(soup)
    
    # get the comments on the page
    comments = get_comments(soup, poster_username)
    
    return comments

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please provide a link as a command line argument')
        sys.exit()

    # get user input for link
    link = sys.argv[1]
    
    # call the grab_comments function to extract the comments
    comments = grab_comments(link)
    
    comment_analysis(comments)