import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def get_artist_songs(artist_slug):
    """Retorna lista de músicas de um artista"""
    
    artist_url = f"https://www.cifraclub.com.br/{artist_slug}/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        logger.info(f"Buscando músicas de: {artist_url}")
        response = requests.get(artist_url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        songs = []
        
        # Procurar elementos <p> com classes específicas
        keywords = ['styles_text__', 'primaryLabel', 'labelFixedNormalBase']
        
        # Encontrar todos os elementos <p>
        all_paragraphs = soup.find_all('p')
        logger.debug(f"Total de elementos <p>: {len(all_paragraphs)}")
        
        for p in all_paragraphs:
            classes = p.get('class', [])
            class_str = ' '.join(classes)
            text = p.text.strip()
            
            # Filtrar: deve ter texto e classes específicas
            if text and len(text) > 2:
                # Verificar se tem pelo menos uma das palavras-chave
                has_keyword = any(keyword in class_str for keyword in keywords)
                
                if has_keyword:
                    # Tentar encontrar o link associado
                    parent_link = p.find_parent('a')
                    url = ''
                    
                    if parent_link and parent_link.get('href'):
                        href = parent_link['href']
                        if href.startswith('/'):
                            url = f"https://www.cifraclub.com.br{href}"
                        else:
                            url = href
                    
                    songs.append({
                        'name': text,
                        'url': url,
                        'artist': artist_slug
                    })
        
        # Se não encontrou pelo padrão, buscar de outra forma
        if not songs:
            logger.debug("Buscando por links de música...")
            
            all_links = soup.find_all('a', href=True)
            
            for link in all_links:
                href = link['href']
                text = link.text.strip()
                
                # Filtrar links que parecem ser músicas
                if (href.startswith(f'/{artist_slug}/') and 
                    href.count('/') == 2 and 
                    text and 
                    len(text) > 2):
                    
                    # Garantir que a URL aponte para a cifra
                    if not href.endswith('#'):
                        href = href.rstrip('/') + '/#'
                    
                    url = f"https://www.cifraclub.com.br{href}"
                    
                    songs.append({
                        'name': text,
                        'url': url,
                        'artist': artist_slug
                    })
        
        # Remover duplicados
        unique_songs = []
        seen_urls = set()
        
        for song in songs:
            if song['url'] and song['url'] not in seen_urls:
                seen_urls.add(song['url'])
                unique_songs.append(song)
        
        logger.info(f"Encontradas {len(unique_songs)} músicas para {artist_slug}")
        return unique_songs
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro de rede ao buscar {artist_slug}: {e}")
        raise Exception(f"Erro ao acessar o site: {e}")
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar {artist_slug}: {e}")
        raise

def get_song_cifra(song_url):
    """Extrai o texto da cifra de uma música"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        logger.debug(f"Buscando cifra: {song_url}")
        response = requests.get(song_url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscar a cifra na tag <pre>
        cifra = soup.find('pre')
        
        if cifra:
            return cifra.text.strip()
        else:
            # Tentar métodos alternativos
            cifra_div = soup.find('div', class_=lambda x: x and 'cifra' in x.lower())
            if cifra_div:
                return cifra_div.text.strip()
            
            logger.warning(f"Cifra não encontrada em: {song_url}")
            return None
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro de rede ao buscar cifra: {e}")
        return None
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar cifra: {e}")
        return None

# Função auxiliar para extrair nome da música da URL
def extract_song_name_from_url(url):
    """Extrai o nome da música da URL"""
    if not url:
        return ""
    
    # Exemplo: https://www.cifraclub.com.br/marina-sena/lua-cheia/#
    parts = url.rstrip('/#').split('/')
    if len(parts) >= 2:
        song_slug = parts[-1]
        return song_slug.replace('-', ' ').title()
    return ""