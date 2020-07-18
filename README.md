# Client Wishlist
Client Wishlist é um desafio técnico cujo objetivo é fazer com que um cliente possa montar sua lista de desejo de acordo com as especificações da empresa que ofereceu o desafio.

## Como instalar
Para rodar o projeto é necessário instalar primeiro o pipenv

Caso esteja usando Mac, use o comando:

    $ brew install pipenv

Caso esteja usando Debian Buster+:

    $ sudo apt install pipenv

Caso esteja usando Fedora:

    $ sudo dnf install pipenv
    
Caso esteja usando FreeBSD:

    # pkg install py36-pipenv

Caso contário:

    $ pip install pipenv

Se mesmo assim não foi possível a instalação cheque a [documentação](https://pipenv.pypa.io/en/latest/#install-pipenv-today) do pacote

## Configurando o ambiente

### Pipenv
Pipenv tratará todas as dependências necessárias para rodar o projeto.

Na pasta raíz do projeto onde o arquivo Pipfile e Pipfile.lock estão rode o comando:
    
    $ pipenv install

Para rodar o virtualenv use o comando

    $ pipenv shell
    
### Postgres
É necessário um postgres==12.3 para o projeto.
Verifique a [documentação](https://www.postgresql.org/docs/current/tutorial-install.html) para informacões de como instalar e iniciar o postgres.

Com o postgres instalado crie um banco de dados e altera as informações do banco em
```client_whishlist/settings.py``` conforme o exemplo abaixo:

```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "<seu_banco>",
        "HOST": "<seu_host>",
        "PORT": "<sua_porta>",
    }
}
```

### Migrando o banco de dados
Com o banco funcionando e dentro do shell do pipenv é necessário fazer a migração inicial dos modelos.

Para isso use o comando ```python manage.py migrate```

### Criando um superuser
Antes de acessar o admin do projeto é necessário criar um superuser.

Para isso rode o comando ```$ python manage.py createsuperuser``` e siga as instruções no terminal.

## Rodando o projeto
Para rodar o projeto use o comando ```python manage.py runserver``` na pasta que contenha o arquivo ```manage.py```
