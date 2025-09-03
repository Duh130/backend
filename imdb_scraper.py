import requests
import time
import csv
import random
import concurrent.futures
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://www.google.com/'
}

MAX_THREADS = 5

session = requests.Session()
session.headers.update(headers)

def extract_movie_details(movie_link):
    time.sleep(random.uniform(1, 2))  # pausa para evitar bloqueio
    response = session.get(movie_link)
    movie_soup = BeautifulSoup(response.content, 'html.parser')

    if movie_soup is not None:
        title = None
        date = None

        title_tag = movie_soup.find('h1')
        if title_tag:
            title = title_tag.get_text(strip=True)

        date_tag = movie_soup.find('a', href=lambda href: href and 'releaseinfo' in href)
        if date_tag:
            date = date_tag.get_text(strip=True)

        rating_tag = movie_soup.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'})
        rating = rating_tag.get_text(strip=True) if rating_tag else None

        plot_tag = movie_soup.find('span', attrs={'data-testid': 'plot-xs_to_m'})
        plot_text = plot_tag.get_text(strip=True) if plot_tag else None

        if all([title, date, rating, plot_text]):
            print(title, date, rating, plot_text)
            with open('ebac/movies.csv', mode='a', newline='', encoding='utf-8') as file:
                movie_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                movie_writer.writerow([title, date, rating, plot_text])

def extract_movies(soup):
    movies_table = soup.find('table', class_='chart')
    if not movies_table:
        print("⚠️ Tabela de filmes não encontrada.")
        return

    movies_table_rows = movies_table.find_all('tr')[1:]
    movie_links = ['https://www.imdb.com' + row.find('td', class_='titleColumn').a['href'] for row in movies_table_rows if row.find('td', class_='titleColumn')]

    if not movie_links:
        print("⚠️ Nenhum filme encontrado.")
        return

    threads = min(MAX_THREADS, len(movie_links))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(extract_movie_details, movie_links)

def main():
    start_time = time.time()

    with open('ebac/movies.csv', mode='w', newline='', encoding='utf-8') as file:
        movie_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        movie_writer.writerow(['Título', 'Data de Lançamento', 'Classificação', 'Sinopse'])

    top_movies_url = 'https://www.imdb.com/chart/top/'
    response = session.get(top_movies_url)
    if response.status_code != 200:
        print(f"Erro ao acessar a página: Status code {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    extract_movies(soup)

    end_time = time.time()
    print('⏳ Total time taken: ', end_time - start_time, "seconds")

if __name__ == '__main__':
    main()
