# eLearning IPLeiria Downloader

# Script ainda em Desenvolvimento! TODO: Download de cada item individual.

Script em Python que permite transferir para arquivo todo o conteúdo da plataforma de eLearning do IPLeiria. É criado localmente uma cópia com HTML de cada UC e respectivos conteúdos.

## Preparando o Script

Para correr o script necessita de um sistema com Python instalado.

### Pre requisitos

Necessita de um sistema com Python configurado. Testado em Python 3.6. Necessita do módulo requests e jinja2 instalado. Para configurar corra o seguinte comando.

```
python -m pip install requests jinja2
```

### Correr o script

Para correr o script basta executar o seguinte comando.

```
python downloader.py -u <nomedeutilizador> -p <password>
```

## Autores

* **Ruben Nogueira** - [rubnogueira](https://github.com/rubnogueira)