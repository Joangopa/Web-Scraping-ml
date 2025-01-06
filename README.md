# Monitoramento de Preço com Web Scraping 

Este projeto realiza o monitoramento de preços de produtos em sites de e-commerce, utilizando técnicas de web scraping. O projeto coleta preços e envia notificações no Telegram quando o valor atinge um limite específico definido pelo usuário


## Bibliotecas Utilizadas e Explicação

1. **requests**: Usada para fazer requisições HTTP e obter o HTML das páginas web.
2. **BeautifulSoup (bs4)**: Utilizada para analisar e extrair informações específicas do HTML das páginas.
3. **schedule**: Biblioteca para agendar tarefas, permitindo verificar preços em intervalos regulares.
4. **pandas**: Facilita a manipulação de dados.
5. **sqlite3**: Um banco de dados.
6. **python-telegram-bot**: Biblioteca para enviar mensagens ao Telegram.
7. **python-dotenv**: Carrega variáveis de ambiente de um arquivo `.env`.

## Pré-requisitos

1. **Python 3.12**: O projeto foi criado usando Python 3.12.
2. **Dependências**: Instale as bibliotecas listadas no arquivo `requirements.txt`.

Para instalar as bibliotecas, execute o comando:
```bash
pip install -r requirements.txt
```

## Configuração

1. **Configuração do Telegram**: Crie um bot no Telegram usando o BotFather e obtenha o token de autenticação.
2. **Arquivo `.env`**: Crie um arquivo `.env` na raiz do projeto e insira as credenciais do Telegram:
   ```
   TELEGRAM_TOKEN=SEU_TOKEN_DO_TELEGRAM
   TELEGRAM_CHAT_ID=SEU_CHAT_ID
   ```
   - Substitua `SEU_TOKEN_DO_TELEGRAM` com o token do seu bot.
   - Substitua `SEU_CHAT_ID` com o ID do chat onde você deseja receber notificações.
       O ID do chat pode ser achado em: `https://api.telegram.org/bot<seu-token>/getUpdates`

3. **Configuração do Banco de Dados**: O banco de dados SQLite será criado automaticamente na primeira execução.

## Como Executar

1. **Clone o Repositório**:
   ```bash
   git clone https://github.com/Joangopa/Web-Scraping-ml
   cd Web-Scraping-ml
   ```

2. **Instale as Dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure o `.env`**:
   - Siga as instruções em "Configuração" e adicione o arquivo `.env` com as variáveis de ambiente para o bot do Telegram.

4. **Execute o Script**:
   ```bash
   python app.py
   ```

O projeto agora iniciará o monitoramento do preço de produtos, verificando em intervalos regulares e notificando o usuário via Telegram caso o preço atinja o valor desejado.

## Migrando para Postgres

Para migrar de SQLite para PostgreSQL, você pode usar a biblioteca `psycopg2` para conectar-se ao banco de dados PostgreSQL. Abaixo está o código atualizado para suportar o PostgreSQL. Vou explicar as mudanças e as etapas adicionais necessárias para configurar o ambiente.

1. Atualize o arquivo `.env` com as credenciais do PostgreSQL:
   ```env
   TELEGRAM_TOKEN=SEU_TOKEN_DO_TELEGRAM
   TELEGRAM_CHAT_ID=SEU_CHAT_ID
   POSTGRES_DB=nome_do_banco
   POSTGRES_USER=seu_usuario
   POSTGRES_PASSWORD=sua_senha
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   ```
   **Execute o Script**:
   ```bash
   python app_postgres.py
   ```

   ## Docker

Aqui estão os comandos para construir e executar o contêiner Docker com o `.env`:

1. **Construir a Imagem Docker**:
   Navegue até o diretório onde o `Dockerfile` está localizado e execute:

   ```bash
   docker build -t product_prices .
   ```

   Esse comando cria uma imagem Docker chamada `product_prices` usando o `Dockerfile` atual.

2. **Executar o Contêiner com as Variáveis de Ambiente do `.env`**:
   Para iniciar o contêiner e carregar as variáveis de ambiente do arquivo `.env`, use:

   ```bash
   docker run -d --env-file .env --name product_prices_container product_prices
   ```

   - `-d`: Executa o contêiner em segundo plano (modo "detached").
   - `--env-file .env`: Carrega as variáveis de ambiente definidas no arquivo `.env`.
   - `--name product_prices_container`: Nomeia o contêiner como `product_prices_container`.
   - `product_prices`: Especifica a imagem que você criou no comando de build.

Esse processo configurará o contêiner para rodar o `app_postgres.py` com as variáveis de ambiente do `.env`.
