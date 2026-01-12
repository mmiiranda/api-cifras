from flask import Flask, jsonify, request
from flask_cors import CORS
from scraper import get_artist_songs, get_song_cifra
import logging

app = Flask(__name__)
CORS(app)  # Permite requisições de qualquer origem

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Página inicial da API"""
    return jsonify({
        'message': 'CifraClub API',
        'version': '1.0.0',
        'endpoints': {
            '/artist/<artist_slug>': 'Buscar músicas de um artista',
            '/cifra/<song_url>': 'Obter cifra de uma música',
            '/artist/<artist_slug>/songs': 'Buscar músicas com detalhes',
            '/health': 'Verificar status da API'
        }
    })

@app.route('/health')
def health():
    """Endpoint de saúde da API"""
    return jsonify({'status': 'healthy'}), 200

@app.route('/artist/<artist_slug>')
def get_artist(artist_slug):
    """
    Retorna lista de músicas de um artista
    
    Exemplo: /artist/marina-sena
    """
    try:
        logger.info(f"Buscando músicas do artista: {artist_slug}")
        songs = get_artist_songs(artist_slug)
        
        return jsonify({
            'artist': artist_slug.replace('-', ' ').title(),
            'count': len(songs),
            'songs': songs
        })
    
    except Exception as e:
        logger.error(f"Erro ao buscar artista {artist_slug}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/cifra')
def get_cifra():
    """
    Retorna a cifra de uma música a partir da URL
    
    Parâmetro: url (URL completa da música)
    Exemplo: /cifra?url=https://www.cifraclub.com.br/marina-sena/lua-cheia/#
    """
    song_url = request.args.get('url')
    
    if not song_url:
        return jsonify({'error': 'Parâmetro "url" é obrigatório'}), 400
    
    try:
        logger.info(f"Buscando cifra: {song_url}")
        cifra = get_song_cifra(song_url)
        
        if cifra:
            return jsonify({
                'url': song_url,
                'cifra': cifra,
                'success': True
            })
        else:
            return jsonify({
                'url': song_url,
                'error': 'Cifra não encontrada',
                'success': False
            }), 404
    
    except Exception as e:
        logger.error(f"Erro ao buscar cifra: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/artist/<artist_slug>/songs')
def get_artist_songs_with_cifra(artist_slug):
    """
    Retorna músicas de um artista com preview das cifras
    
    Parâmetros opcionais:
    - limit: número máximo de músicas (padrão: 10)
    - with_cifra: incluir preview da cifra (padrão: false)
    """
    limit = request.args.get('limit', 10, type=int)
    with_cifra = request.args.get('with_cifra', 'false').lower() == 'true'
    
    try:
        logger.info(f"Buscando músicas de {artist_slug} (limit: {limit})")
        songs = get_artist_songs(artist_slug)
        
        if limit > 0:
            songs = songs[:limit]
        
        result = {
            'artist': artist_slug.replace('-', ' ').title(),
            'count': len(songs),
            'songs': songs
        }
        
        # Adicionar preview da cifra se solicitado
        if with_cifra:
            for song in result['songs']:
                cifra = get_song_cifra(song['url'])
                if cifra:
                    # Pegar apenas as primeiras linhas como preview
                    lines = cifra.strip().split('\n')[:5]
                    song['cifra_preview'] = '\n'.join(lines)
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Erro: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)