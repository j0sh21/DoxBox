import requests
import os

# Giphy API settings
API_KEY = ""
LIMIT = 100  # Number of GIFs per theme

def search_gifs(theme):
    """Search for GIFs by theme using the Giphy API."""
    url = f'https://api.giphy.com/v1/gifs/search?api_key={API_KEY}&q={theme}&limit={LIMIT}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data']
    else:
        print(f'Error fetching GIFs for theme {theme}: {response.status_code}')
        return []

def download_gif(url, path):
    """Download a single GIF given its URL."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    else:
        print(f'Error downloading GIF {url}: {response.status_code}')

def main(themes):
    """Download GIFs for each theme."""
    for theme in themes:
        gifs = search_gifs(theme)
        for i, gif in enumerate(gifs):
            gif_url = gif['images']['original']['url']
            file_name = f'{theme}_{i+1}.gif'
            file_path = os.path.join('gifs', theme, file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            download_gif(gif_url, file_path)
            print(f'Downloaded {file_name}')

if __name__ == '__main__':
    themes = ['welcome', 'countdown', 'thx', 'error']  # Example themes
    main(themes)
