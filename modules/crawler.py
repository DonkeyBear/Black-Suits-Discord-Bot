import requests
from bs4 import BeautifulSoup
import random
import re


def get_random_idiom():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}
    response_1 = requests.get(
        'https://dict.idioms.moe.edu.tw/bookView.jsp?ID=-1', headers=headers)
    soup_1 = BeautifulSoup(response_1.text, "html.parser")
    idiom_url = f'https://dict.idioms.moe.edu.tw{random.choice(soup_1.select("fieldset fieldset a")).get("href")}'
    response_2 = requests.get(idiom_url, headers=headers)
    soup_2 = BeautifulSoup(response_2.text, "html.parser")

    idiom_title = soup_2.select_one('h2').getText()
    idiom_desc = soup_2.select_one('#row_mean').getText().split('釋　　義')[-1]
    idiom_phonet_raw = soup_2.select('#row_mean nobr')
    idiom_phonet = ''
    for item in idiom_phonet_raw:
        if '變' in item.getText():
            idiom_phonet += '／ '
        else:
            idiom_phonet += f'`{item.getText()}` '
    idiom_story = soup_2.select_one(
        '#row_annotate').getText().replace('典故說明', '', 1)

    return {'title': idiom_title, 'desc': idiom_desc, 'url': idiom_url, 'phonet': idiom_phonet, 'story': idiom_story}


def get_random_wikipedia_article():
    response = requests.get(
        'https://zh.m.wikipedia.org/zh-tw/Special:%E9%9A%8F%E6%9C%BA%E9%A1%B5%E9%9D%A2')
    soup = BeautifulSoup(response.text, 'html.parser')
    wiki_title = soup.select_one('#firstHeading').getText()
    wiki_url = 'https:' + soup.select_one('#mw-mf-display-toggle').get(
        'href').replace('&mobileaction=toggle_view_desktop', '')
    wiki_summary_paragraph = soup.select('#mf-section-0 > p')

    # 檢查來源內容是否為空白，如果空白，則替換來源元素
    wiki_summary = ''
    for item in wiki_summary_paragraph:
        wiki_summary += item.getText().strip()
    if wiki_summary.strip() == '':
        wiki_summary = soup.select_one(
            '#bodyContent > p:not(.mw-empty-elt)').getText().strip()
        wiki_summary_paragraph = [wiki_summary]

    wiki_paragraphs = []
    for item in wiki_summary_paragraph:
        content = re.sub('\[\d+\]', '', item.getText().strip())
        if content != '':
            wiki_paragraphs.append(content)

    return {'title': wiki_title, 'url': wiki_url, 'paragraphs': wiki_paragraphs}


def get_random_fun_image():
    # 取得最新一篇「雜七雜八短篇漫畫翻譯」的編號
    response_1 = requests.get(
        'https://hornydragon.blogspot.com/search/label/%E9%9B%9C%E4%B8%83%E9%9B%9C%E5%85%AB%E7%9F%AD%E7%AF%87%E6%BC%AB%E7%95%AB%E7%BF%BB%E8%AD%AF?&max-results=1')
    soup_1 = BeautifulSoup(response_1.text, "html.parser")
    newest_post = soup_1.select_one(
        '.post-outer a').getText().replace('雜七雜八短篇漫畫翻譯', '')

    # 以隨機數搜尋一篇「雜七雜八短篇漫畫翻譯」
    target_post = random.randint(2, int(newest_post))
    response_2 = requests.get(
        f'https://hornydragon.blogspot.com/search?q=%E9%9B%9C%E4%B8%83%E9%9B%9C%E5%85%AB%E7%9F%AD%E7%AF%87%E6%BC%AB%E7%95%AB%E7%BF%BB%E8%AD%AF{target_post}')
    soup_2 = BeautifulSoup(response_2.text, "html.parser")
    target_post_url = soup_2.select_one('.post-outer a').get('href')

    # 取上一步搜尋結果第一項
    response_3 = requests.get(target_post_url)
    soup_3 = BeautifulSoup(response_3.text, "html.parser")

    # 在文章內隨機選擇一張圖
    fun_images = soup_3.select('.post-body img')
    random_fun_image = fun_images[random.randint(
        0, len(fun_images) - 1)].get('src')

    if random_fun_image.startswith('/'):
        random_fun_image = f'https:{random_fun_image}'

    return {'source': f'雜七雜八短篇漫畫翻譯{target_post}', 'source_url': target_post_url, 'image': random_fun_image}
