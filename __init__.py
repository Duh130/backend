import requests
import time
import csv
import random
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/'
}

session = requests.Session()
session.headers.update(headers)

def extract_movie_details(movie_link):
    """Extrai os detalhes de um filme individual"""
    time.sleep(random.uniform(1, 3))  # pausa para evitar bloqueio
    response = session.get(movie_link)
    if response.status_code != 200:
        print(f"Erro ao acessar {movie_link}")
        return None

    movie_soup = BeautifulSoup(response.content, 'html.parser')

    title = movie_soup.find('h1')
    title = title.get_text(strip=True) if title else "N/A"

    date_tag = movie_soup.find('a', href=lambda href: href and 'releaseinfo' in href)
    date = date_tag.get_text(strip=True) if date_tag else "N/A"

    rating_tag = movie_soup.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'})
    rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"

    plot_tag = movie_soup.find('span', attrs={'data-testid': 'plot-xs_to_m'})
    plot = plot_tag.get_text(strip=True) if plot_tag else "N/A"

    return [title, date, rating, plot]

def main():
    # cria o arquivo CSV
    with open('movies.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Título', 'Data de Lançamento', 'Classificação', 'Sinopse'])

        # acessa a página Top 250
        url = 'https://www.imdb.com/chart/top/'
        response = session.get(url)
        if response.status_code != 200:
            print(f"Erro ao acessar a página principal: {response.status_code}")
            return

        soup = BeautifulSoup(response.content, 'html.parser')

        # pega os 10 primeiros filmes
        movies = soup.find_all('li', class_='ipc-metadata-list-summary-item')[:10]
        if not movies:
            print("⚠️ Nenhum filme encontrado. O IMDB pode ter alterado a estrutura novamente.")
            return

        for movie in movies:
            link = movie.find('a')
            if link and link['href']:
                movie_url = 'https://www.imdb.com' + link['href']
                details = extract_movie_details(movie_url)
                if details:
                    print(details)
                    writer.writerow(details)

    print("✅ Extração concluída! Arquivo movies.csv criado.")

if __name__ == '__main__':
    main()
