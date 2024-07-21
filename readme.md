# EncurtaPy

## Breve descrição

#### Encurtador de URL usando Python / Flask / MySQL no backend para cadastro e registro de URL encurtadas.
#### Usei Bootstrap para fazer a interface Web para usuários e autenticação JWT para caso queira fazer o próprio Front



## Como configurar?

#### Instalação do `venv (Virtual Environment)`
> Caso opte por usar um nome personalizado, adicionar o mesmo no `.gitignore` para a pasta não subir para o repositório.
> O "xy" representa a versão do seu Python 3 (exemplo: python3.10/3.11/3.12).

- `python3.xy -m venv .venv` 
ou
- `python3.xy -m venv .{nomepersonalizado}` 

#### Instalação das dependências do projeto em [`requirements.txt`](./requirements.txt)
##### No Windows:
> Necessário habilitar execução de scripts [`.ps1 da Microsoft`](https://learn.microsoft.com/pt-br/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.4)


- `.venv/Scripts/activate`
- `python -m pip install -r requirements.txt`

##### No Linux:

- `source .venv/bin/activate`
- `python -m pip install -r requirements.txt`

#### Criação do arquivo `.env`

```.env

## Enviroment

DEBUG = False
Database = ""
DBLogin = ""
DBPassword = ""
DBHost = ""



```

## Estrutura do projeto

- [`APP`](./app/): É a pasta onde fica centralizado rotas, formulários e models do Flask

#### A partir de `/app`, teremos:

- [`Routes`](./app/routes.py): Rotas do Projeto, sempre mantendo separados por funções.

- [`Models`](./app/models/): Onde ficam os models e bind's do SQL.

- [`Forms`](./app/Forms/): Formulários do projeto, sempre mantendo separados por funções.

## Tecnologias Utilizadas: 
<div style="display: inline_block">
<br>
  <img align="center" alt="BOOTSTRAP" src="https://img.shields.io/badge/Bootstrap-20232A?style=for-the-badge&logo=bootstrap&logoColor=61DAFB"/> 
  <img align="center" alt="PYTHON" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img align="center" alt="FLASK" src="https://img.shields.io/badge/Flask-092E20?style=for-the-badge&logo=flask&logoColor=white" />
  <img align="center" alt="MYSQL" src="https://img.shields.io/badge/MySQL-6488ea?style=for-the-badge&logo=mysql&logoColor=white" />
  <img align="center" alt="LINUX" src="https://img.shields.io/badge/Linux-000?style=for-the-badge&logo=linux&logoColor=FCC624" />
</div>

<br>


## Caso queira alternativas, veja o Desafios Backend: 

[Desafio-BackEnd](https://github.com/backend-br/desafios)

## URL para visualização

[Encurtador](https://short.robotz.dev)

