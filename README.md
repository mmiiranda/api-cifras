# 🎸 API Cifras

Uma API robusta desenvolvida em Python para realizar web scraping de cifras musicais. O projeto permite extrair letras e acordes de forma estruturada, facilitando a integração com outros aplicativos de música ou estudos musicais.

---

## 🚀 Tecnologias e Ferramentas

* **Linguagem:** Python 3.9+
* **Web Framework:** Flask
* **Scraping:** BeautifulSoup4 / Requests
* **Containerização:** Docker & Docker Compose
* **Automação:** Makefile

---

## 🛠️ Como Executar o Projeto

Você pode subir o ambiente de três maneiras diferentes:

### 1. Via Docker (Recomendado)
Para rodar a aplicação isolada em um container:
```bash
docker-compose up --build
```

### 2. Via Makefile

Se você estiver em um ambiente Unix, utilize os atalhos do Makefile:
```bash
make install  # Para instalar as dependências locais
make run      # Para executar o servidor Flask
```

### 3. Instalação Manual
```bash
# Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
python app.py
```

---
## 📂 Organização do Repositório

* **`app.py`**: Ponto de entrada da API Flask. Gerencia as rotas, o logging de requisições e a configuração de CORS.
* **`scraper.py`**: Contém a lógica de extração de dados do Cifra Club, como a listagem de músicas e a raspagem da cifra completa.
* **`Dockerfile` & `docker-compose.yml`**: Define o ambiente containerizado para garantir que a API rode em qualquer máquina (atualmente configurada na porta `3000`).
* **`Makefile`**: Atalhos para simplificar comandos frequentes (`install`, `run`).
* **`requirements.txt`**: Dependências do projeto (Flask, flask-cors, beautifulsoup4, requests).

---

## 📡 Endpoints da API

Abaixo estão os endpoints reais configurados nesta API:

| Método | Endpoint | Descrição | Parâmetros |
| :--- | :--- | :--- | :--- |
| `GET` | `/artist/<slug>` | Retorna a lista de músicas de um artista. | `artist_slug` (ex: `queen`) |
| `GET` | `/cifra` | Retorna a cifra completa de uma música. | `url` (URL do Cifra Club) |
| `GET` | `/artist/<slug>/songs` | Lista músicas com opção de preview da cifra. | `limit` (int), `with_cifra` (bool) |

### 💡 Exemplos de Uso

**Buscar músicas de um artista:**
`GET http://localhost:3000/artist/pericles`

**Buscar cifra específica:**
`GET http://localhost:3000/cifra?url=https://www.cifraclub.com.br/pericles/ate-que-durou/`

---

## 📝 Licença

Este projeto está sob a licença MIT. Sinta-se à vontade para usar e estudar.
