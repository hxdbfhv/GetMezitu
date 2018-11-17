import requests
import re
from bs4 import BeautifulSoup
import os
from multiprocessing import Process


def get_image_url(url):
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content,"lxml")  # lxml???
    html_image_url = soup.select("#pins li span a")
    urls = []
    for url in html_image_url:
        url = url.get('href')  # href???
        urls.append(url)
    return urls


def get_group_image_url(url):
    group_page = requests.get(url).text
    title = re.findall(r'<h2 class="main-title">(.*)</h2>',group_page)[0]
    max_page = re.findall(r'<span>(\d*)</span>',group_page)[-1]
    try:
        os.chdir("./"+title)
    except:
        os.mkdir("./"+title)
        os.chdir("./"+title)
    finally:
        pass
    print("下载 "+title+" 文件夹")
    return max_page


def get_image_content(url):
    image_url = requests.get(url).text
    image_content = re.findall(r'<img src="(.*)" alt=',image_url)[0]
    return image_content


def create_dir():
    try:
        os.mkdir("./妹子")
        os.chdir("./妹子")
        print("创建 妹子 文件夹成功")
    except:
        os.chdir("./妹子")
        print("妹子 文件夹已存在")


def download(url_list):
    for u in url_list:
        j = 0
        max_page = get_group_image_url(u)
        for k in range(1, int(max_page) + 1):
            j += 1
            image_url = u + '/' + str(k)
            print(image_url)
            image_page = get_image_content(image_url)
            image = requests.get(image_page, headers=head)
            with open("%d.jpg" % j, "wb") as f:
                f.write(image.content)
                print("美女图%d 下载successful" % j)
        os.chdir("../")


def main(x, n):
    # create_dir()
    for i in range(x, n):
        url = "http://www.mzitu.com/xinggan/page/{}/".format(i)
        url_list = get_image_url(url)
    # print(url_list)
        download(url_list)


if __name__ == "__main__":
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Referer': 'http://www.mzitu.com'}
    n = int(input("请输入要下载的页数，请大于3好吗？："))
    create_dir()
    x = int(n/2)
    p1 = Process(target=main, args=(0, x))
    p2 = Process(target=main, args=(x, n))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
