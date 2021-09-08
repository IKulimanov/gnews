import datetime
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import requests
import lxml
from bs4 import BeautifulSoup


def get_news(search="Russia", interval="30d", region="en-US"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582 "
    }

    params = {
        "q": str(search) + "when:" + str(interval),
        "hl": str(region)
    }

    response = requests.get("https://news.google.com/search", headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'lxml')
    title = ""
    for result in soup.select('.xrnccd'):
        title = title + result.select_one('.DY5T1d').text
    return title


def calc_word_cloud(text):
    word_cloud = WordCloud(background_color='white', max_words=50,
                           stopwords={'Russia', 'Russian', 'to', 'in', 'of', 'and', 'for', 'the', 'with',
                                      'a', 'are', 'i', 's', 'say', 'over', 'not', 'has', 'from', 'what', 'on',
                                      'u', 'out', 'says', 'it', 'is', 'after', 'up', 'top', 'as'}).generate(text)

    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig("gnews_" + str(datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")) + ".png", format="png")
    plt.gcf().canvas.manager.set_window_title('Google News word cloud')
    plt.show()


if __name__ == '__main__':
    calc_word_cloud(get_news())
