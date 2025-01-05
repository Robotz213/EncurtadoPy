# EncurtaPy

## Breve Descrição

EncurtaPy é um encurtador de URL desenvolvido utilizando Python, Flask e MySQL no backend para cadastro e registro de URLs encurtadas. A interface web foi construída com Bootstrap, e a autenticação é gerenciada via JWT, permitindo que você crie seu próprio front-end.

## Como Configurar?

### Instalação do Ambiente Virtual (`venv`)

Para criar um ambiente virtual, utilize o comando abaixo. Se optar por um nome personalizado, adicione-o ao `.gitignore` para evitar que a pasta seja enviada ao repositório. O "xy" representa a versão do seu Python 3 (exemplo: python3.10/3.11/3.12).

- `python3.xy -m venv .venv`
  ou
- `python3.xy -m venv .{nomepersonalizado}`

### Instalação das Dependências

As dependências do projeto estão listadas no arquivo [`requirements.txt`](./requirements.txt).

#### No Windows:

Para habilitar a execução de scripts, siga as instruções da [documentação da Microsoft](https://learn.microsoft.com/pt-br/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.4).

- Ative o ambiente virtual: `.venv/Scripts/activate`
- Instale as dependências: `python -m pip install -r requirements.txt`

#### No Linux:

- Ative o ambiente virtual: `source .venv/bin/activate`
- Instale as dependências: `python -m pip install -r requirements.txt`

### Criação do Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com as seguintes configurações:

```
## Environment

DEBUG = False
Database = ""
DBLogin = ""
DBPassword = ""
DBHost = ""
```

## Estrutura do Projeto

- [`APP`](./app/): Diretório principal contendo rotas, formulários e models do Flask.

### Estrutura Interna do Diretório `/app`:

- [`Routes`](./app/routes.py): Arquivo contendo as rotas do projeto, organizadas por funções.
- [`Models`](./app/models/): Diretório onde estão os models e binds do SQL.
- [`Forms`](./app/forms/): Diretório contendo os formulários do projeto, organizados por funções.

## Tecnologias Utilizadas

<div style="display: inline_block">
<br>
  <img align="center" alt="BOOTSTRAP" src="https://img.shields.io/badge/Bootstrap-20232A?style=for-the-badge&logo=bootstrap&logoColor=61DAFB"/> 
  <img align="center" alt="PYTHON" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img align="center" alt="FLASK" src="https://img.shields.io/badge/Flask-092E20?style=for-the-badge&logo=flask&logoColor=white" />
  <img align="center" alt="MYSQL" src="https://img.shields.io/badge/MySQL-6488ea?style=for-the-badge&logo=mysql&logoColor=white" />
  <img align="center" alt="LINUX" src="https://img.shields.io/badge/Linux-000?style=for-the-badge&logo=linux&logoColor=FCC624" />
</div>

<br>

## Alternativas e Desafios

Para explorar alternativas e desafios relacionados ao backend, visite o repositório [Desafio-BackEnd](https://github.com/backend-br/desafios).

## URL para Visualização

Acesse o encurtador de URLs em [Encurtador](https://short.robotz.dev).
