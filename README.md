# Sistema de Agendamento para Barbearia

Este projeto é um sistema de agendamento online desenvolvido para barbearias, permitindo aos usuários agendar, visualizar e cancelar agendamentos. Administradores podem visualizar todos os agendamentos, adicionar ou remover serviços e gerenciar agendamentos.

## Funcionalidades

- **Agendamento de Serviços**: Usuários podem escolher serviços e horários disponíveis para fazer um agendamento.
- **Visualização de Agendamentos**: Usuários podem ver seus próximos agendamentos e administradores podem ver todos os agendamentos.
- **Cancelamento de Agendamentos**: Usuários podem cancelar seus agendamentos, com uma confirmação de cancelamento.
- **Gestão de Serviços**: Administradores podem adicionar e remover serviços.
- **Filtro por Data**: Administradores podem filtrar agendamentos por data.

## Tecnologias Utilizadas

- **Flask**: Framework web usado para construir o backend.
- **Flask-SQLAlchemy**: ORM utilizado para interações com o banco de dados.
- **Flask-Migrate**: Para migrações do banco de dados.
- **Flask-Login**: Para gerenciamento de sessões de usuário.
- **Jinja2**: Template engine para renderização de páginas HTML.
- **Bootstrap**: Framework de front-end para design responsivo.

## Configuração e Execução

### Pré-Requisitos

- Python 3.6+
- pip
- virtualenv (opcional)

### Instalação

1. Clone o repositório:
git clone [URL do repositório]
cd [nome-do-repositorio]

csharp
Copiar código

2. Crie e ative um ambiente virtual (opcional):
python -m virtualenv venv
source venv/bin/activate # No Windows use venv\Scripts\activate

csharp
Copiar código

3. Instale as dependências:
pip install -r requirements.txt

csharp
Copiar código

4. Configure as variáveis de ambiente:
export FLASK_APP=run.py
export FLASK_ENV=development # Ajuste conforme o necessário para produção

markdown
Copiar código

5. Inicialize o banco de dados:
flask db upgrade

css
Copiar código

6. Execute a aplicação:
flask run

markdown
Copiar código

Acesse a aplicação via `http://localhost:5000` no seu navegador.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE.md para detalhes.

## Autores

- **Seu Nome** - *Trabalho Inicial* - [SeuPerfil](https://github.com/SeuPerfil)

## Agradecimentos

- Reconhecimento a qualquer pessoa cujo código foi usado
- Inspiração
- etc