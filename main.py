from time import sleep

import pandas as pd
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    'Accept-Language': 'en-IN, en;q=0.5'
}

def main():
    search_category = input("Enter Category you want to scrap:")
    search_query = search_category.replace(' ', '+')
    try:
        base_url = 'https://www.amazon.com/s?k={0}'.format(search_query)
    except:
        print("No such category found")

    no_of_pages = int(input("Enter no pages to scrap data"))
    items = []
    for i in range(1, no_of_pages+1):
        print('Processing {0}...'.format(base_url + '&page={0}'.format(i)))
        response = requests.get(base_url + '&page={0}'.format(i), headers=headers)
        if response.ok:
            soup = BeautifulSoup(response.content, 'html.parser')

            results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

            for result in results:
                product_name = result.h2.text
                # print(product_name)
                try:
                    rating = result.find('i', {'class': 'a-icon'}).text
                    rating_count = result.find_all('span', {'aria-label': True})[1].text
                except (AttributeError,IndexError):
                    continue

                try:
                    price1 = result.find('span', {'class': 'a-price-whole'}).text
                    product_url = 'https://amazon.com' + result.h2.a['href']
                    items.append([product_name, rating, rating_count, price1, product_url])
                except AttributeError:
                    continue
        sleep(1.5)

    df = pd.DataFrame(items, columns=['product', 'rating', 'rating count', 'price', 'product url'])
    df.to_csv('{0}.csv'.format(search_query), index=False)


if __name__ == "__main__":
    main()
