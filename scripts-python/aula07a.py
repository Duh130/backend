                        movie_writer.writerow([title, date, rating, plot_text])
def extract_movies(soup):
    movies_table = soup.find('div', attrs={'data-testid': 'chart-layout-main-column'}).find('ul')
    movies_table_rows = movies_table.find_all('li')
    movie_links = ['https://imdb.com' + movie.find('a')['href'] for movie in movies_table_rows]
    threads = min(MAX_THREADS, len(movie_links))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(extract_movie_details, movie_links)
def main():
    start_time = time.time()
    # Criar arquivo CSV com cabeçalho
    with open('movies.csv', mode='w', newline='', encoding='utf-8') as file:
        movie_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        movie_writer.writerow(['Título', 'Data de Lançamento', 'Classificação', 'Sinopse'])
    # IMDB Most Popular Movies - 100 movies
    popular_movies_url = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'
    response = requests.get(popular_movies_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Main function to extract the 100 movies from IMDB Most Popular Movies
    extract_movies(soup)
    end_time = time.time()
    print('Total time taken: ', end_time - start_time)
if __name__ == '__main__':
    main()