from lxml import etree
import login
import requests

if __name__ == '__main__':
    login

# url = "https://github.com/LiuRoy/github_spider"
url = "https://github.com/settings/repositories"
response = requests.get(url)
# print(response)
text = response.text
print(text)
html = etree.HTML(text)
# print(html)


# html_data = html.xpath('//*[@id="js-repo-pjax-container"]/div[1]/div/ul/li[2]/a[2]/text()')
# stars_num = (html_data[0].replace("\n","").replace(" ",""))
# print(stars_num)