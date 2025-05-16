<div style="text-align: center; margin: 20px 0px">
    <h1> LARA Core Server - API </h1>
</div>

<div id='start-of-project'/>

<p align="center" width="100%">
    <img  style=" align-self: center; width:300px;" src="./assets/logo.png" alt="logo">
</p>

> **LARA** (**Laboratório em Redes de Aprendizagem**), trata de um **AVA** com o objetivo de ser uma plataforma educacional que relaciona recursos tecnológicos e métodos de ensino para aprimorar o processo de ensino de disciplinas do curso de Ciência da Computação.

### Ajustes e melhorias

O projeto ainda está em desenvolvimento e as próximas atualizações serão publicadas assim que forem sendo desenvolvidas

<!--
O projeto ainda está em desenvolvimento e as próximas atualizações serão voltadas nas seguintes tarefas:

- [x] Tarefa 1
- [x] Tarefa 2
- [x] Tarefa 3
- [x] Tarefa 4
- [ ] Tarefa 5
-->

## 📋 Documentação

-   [Arquitetura do LARA](https://www.figma.com/file/91UzMFaOk8D6278BwBMWLm/LARA-ARCHITECTURE?node-id=0%3A1&t=HMdsFm4ShjrrlXL5-1)

-   [Casos de Uso](https://raw.githubusercontent.com/sousaGab/core-lara-server/main/assets/documentation/use-case.png)
-   [Banco de Dados - Diagrama](https://raw.githubusercontent.com/sousaGab/core-lara-server/main/assets/documentation/data-base-diagram.png)
-   [Banco de Dados - Modelo Conceitual](https://raw.githubusercontent.com/sousaGab/core-lara-server/main/assets/documentation/data-base-conceptual-model.png)

## 🔗 Pré-requisitos

#### Antes de começar, verfique se você possui as ferramentas necessárias:

-   **[MYSQL](https://dev.mysql.com/doc/mysql-getting-started/en/)**
-   **[Python3](https://realpython.com/installing-python/)**
-   **[PIP](https://www.liquidweb.com/kb/install-pip-windows/)**
-   **[Git](https://git-scm.com/downloads/)**

#### Crie e configure o arquivo settings.py

-   Duplique o arquivo localizado no diretório `/coreLaraServer/settings-example.py`

-   Renomeie o arquivo duplicado criando o arquivo `/coreLaraServer/settings.py`

-   [Crie um novo banco de dados usando mysql](https://docs.rapidminer.com/7.6/server/installation/creating_mysql_db.html#:~:text=Open%20the%20MySQL%20Workbench%20as,command%20that%20creates%20the%20schema.)

-   Insira as informações do banco de dados criado dentro do arquivo `/coreLaraServer/settings.py`:
    ```python
    ...
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'db-name',
            'USER': 'db-user',
            'PASSWORD': 'db-password',
        }
    }
    ...
    ```

## 💻 Instalando o LARA Core Server

Para instalar o LARA Core Server, siga estas etapas:

```bash
# 1. Crie o ambiente virtual:
$ virtualenv venv
$ python -m venv /caminho/para/novo/ambiente/virtual

# 2. Ative o ambiente vitual:

# Linux/Mac
$ source venv/bin/activate

# Windows
$ source venv\Scripts\activate

# 3. Instale as dependências:
$ pip install -r requirements.txt

# 4. Migre as tabelas de banco de dados existentes executando
$ python manage.py migrate

#5. Execute o servidor de desenvolvimento Django usando
$ python manage.py runserver
```

## 🛠 Documentações das tecnologias utilizadas

As seguintes ferramentas foram usadas na construção do projeto:

-   **[Python 3](https://docs.python.org/3/#)**
-   **[Django](https://docs.djangoproject.com/en/4.1/)**
-   **[Django Rest Framework](https://www.django-rest-framework.org/)**
-   **[Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html#)**

<!--


## ☕ Usando LARA Core Server

Para usar LARA Core Server, siga estas etapas:

```
<exemplo_de_uso>
```

Adicione comandos de execução e exemplos que você acha que os usuários acharão úteis. Fornece uma referência de opções para pontos de bônus!

## Abstract

Simple JWT is a JSON Web Token authentication plugin for the `Django REST
Framework <http://www.django-rest-framework.org/>`\_\_.

For full documentation, visit `django-rest-framework-simplejwt.readthedocs.io
<https://django-rest-framework-simplejwt.readthedocs.io/en/latest/>`\_\_.
-->

[⬆ Voltar ao topo](#start-of-project)<br>
