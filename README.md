#  Envio Automático de E-mails em Python

Script desenvolvido em **Python** para envio automatizado de e-mails utilizando SMTP, com suporte a:

- Leitura de contatos por **Excel (.xlsx)**, **CSV (.csv)** ou **TXT (.txt)**;
- Validação de e-mails;
- Remoção de destinatários duplicados;
- Mensagens em **HTML**;
- Personalização do nome do destinatário;
- Anexos opcionais;
- Registro de envios em arquivo de log;
- Tratamento de erros durante o envio.

---

##  Funcionalidades

-  Envio em massa via SMTP
-  Suporte a Gmail, Outlook e outros servidores SMTP
-  Leitura automática de planilhas Excel
-  Suporte a arquivos CSV e TXT
-  Validação de e-mails
-  Remoção de e-mails duplicados
-  Mensagens em HTML
-  Personalização da mensagem utilizando `{nome}`
-  Anexos opcionais
-  Registro dos envios em `envios.log`
-  Barra de progresso no terminal
-  Tratamento individual de erros

---

##  Tecnologias

- Python 3.10+
- pandas
- openpyxl
- smtplib
- tkinter
- email
- re

---

##  Instalação

Clone o repositório:

```bash
git clone https://github.com/SEU-USUARIO/envio-email-python.git
```

Entre na pasta:

```bash
cd envio-email-python
```

Crie um ambiente virtual:

### Windows

```bash
python -m venv .venv
```

Ative o ambiente:

```powershell
.venv\Scripts\Activate.ps1
```

ou

```cmd
.venv\Scripts\activate.bat
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Caso não exista o arquivo `requirements.txt`:

```bash
pip install pandas openpyxl
```

---

## ▶ Como executar

```bash
python main.py
```

O programa solicitará:

```
Servidor SMTP:
E-mail do remetente:
Senha de app:
Assunto:
Mensagem:
Caminho do anexo (opcional):
```

Depois abrirá uma janela para selecionar o arquivo contendo os contatos.

---

##  Formatos suportados

### Excel (.xlsx)

| Email |
|--------|
| joao@email.com |
| maria@email.com |

---

### CSV (.csv)

```csv
Email
joao@email.com
maria@email.com
```

---

### TXT (.txt)

```
joao@email.com
maria@email.com
```

---

##  Personalização da mensagem

Você pode utilizar:

```
Olá {nome},

Seu cadastro foi realizado com sucesso!
```

Se o destinatário for:

```
joao.silva@email.com
```

O e-mail será enviado como:

```
Olá João Silva,

Seu cadastro foi realizado com sucesso!
```

---

##  Anexos

Informe o caminho completo do arquivo:

```
C:\Users\User\Documents\arquivo.pdf
```

Ou deixe vazio caso não queira anexar nenhum arquivo.

---

##  Arquivo de Log

Após cada envio bem-sucedido é criado (ou atualizado) o arquivo:

```
envios.log
```

Exemplo:

```
joao@email.com
maria@email.com
pedro@email.com
```

---

##  Configuração do Gmail

Caso utilize Gmail:

1. Ative a autenticação em duas etapas.
2. Gere uma **Senha de App**.
3. Utilize:

| Configuração | Valor |
|--------------|-------|
| Servidor SMTP | smtp.gmail.com |
| Porta | 587 |

 **Não utilize a senha normal da sua conta Google.**

---

##  Estrutura do projeto

```
envio-email-python/
│
├── main.py
├── requirements.txt
├── README.md
├── envios.log
├── contatos.xlsx
└── .venv/
```

---

##  Dependências

```
pandas
openpyxl
```

Instalação:

```bash
pip install pandas openpyxl
```

---

##  Melhorias futuras

- Interface gráfica completa (Tkinter ou CustomTkinter)
- Envio com imagens incorporadas
- Agendamento de envios
- Suporte a múltiplos anexos
- Barra de progresso gráfica
- Templates HTML externos
- Envio utilizando nomes da planilha
- Exportação de relatório em Excel
- Suporte a Outlook API e Microsoft 365

---

##  Aviso

Este projeto destina-se ao envio de e-mails autorizados e automações internas.

O uso para envio de spam pode resultar em bloqueio da conta de e-mail e violar as políticas do provedor SMTP.

Sempre obtenha o consentimento dos destinatários antes de realizar envios em massa.

---

##  Autor

Desenvolvido por **Ruan Ribeiro**.

Caso este projeto tenha sido útil, considere deixar uma ⭐ no repositório.
