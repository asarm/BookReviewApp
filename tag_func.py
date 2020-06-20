from bs4 import BeautifulSoup
import requests

#url = "https://displaypurposes.com/"
tag = 'italy'
def get_tags(url,tag):
    url += f'hashtags/hashtag/{tag}'
    url = "https://displaypurposes.com/hashtags/rank/best/country"
    #url = "https://hashtagify.me/manual/api"
    html = requests.get(url).content
    # content = response.content
    soup = BeautifulSoup(html, 'html.parser')
    #tags = soup.find('div',{"class":"box-list"})
    print((soup))
    print(url)

#get_tags(url,tag)


def get_insta_info():
    url = "https://easy-instagram-service.p.rapidapi.com/username"

    querystring = {"random":"x8n3nsj2","username":"arda_asarr"}

    headers = {
        'x-rapidapi-host': "easy-instagram-service.p.rapidapi.com",
        'x-rapidapi-key': "bd40a73e82msh6e36037abf6433cp19ec76jsn97b220f2fd53"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

def get_hashtag_custom():
    url = "https://hashtagy-generate-hashtags.p.rapidapi.com/v1/custom_1/tags"

    querystring = {"keyword":"book"}

    headers = {
        'x-rapidapi-host': "hashtagy-generate-hashtags.p.rapidapi.com",
        'x-rapidapi-key': "bd40a73e82msh6e36037abf6433cp19ec76jsn97b220f2fd53"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

def get_comprehensive_hashtags():
    url = "https://hashtagy-generate-hashtags.p.rapidapi.com/v1/comprehensive/tags"

    querystring = {"filter": "top", "keyword": "travel"}

    headers = {
        'x-rapidapi-host': "hashtagy-generate-hashtags.p.rapidapi.com",
        'x-rapidapi-key': "bd40a73e82msh6e36037abf6433cp19ec76jsn97b220f2fd53"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

def get_insta_info_cheap():
    url = "https://instagram29.p.rapidapi.com/user/arda_asarr"

    headers = {
        'x-rapidapi-host': "instagram29.p.rapidapi.com",
        'x-rapidapi-key': "bd40a73e82msh6e36037abf6433cp19ec76jsn97b220f2fd53"
    }

    response = requests.request("GET", url, headers=headers)

    print(response.text)

get_insta_info()