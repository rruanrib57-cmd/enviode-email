import os
import re
import smtplib
from getpass import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import Tk, filedialog
import pandas as pd


def validar_email(email: str) -> bool:
    return re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email.strip()) is not None


def carregar_contatos(caminho_arquivo: str) -> list[str]:
    if caminho_arquivo.endswith(".xlsx"):
        df = pd.read_excel(caminho_arquivo)
        emails = df.iloc[:, 0].dropna().astype(str).tolist()
    else:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            emails = [linha.strip() for linha in arquivo if "@" in linha]

    emails_validos = [email for email in emails if validar_email(email)]
    return emails_validos


# 1. Configurações do servidor
SMTP_SERVER = os.getenv("SMTP_SERVER") or input("Servidor SMTP (ex.: smtp.gmail.com): ").strip()
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE") or input("E-mail do remetente: ").strip()
SENHA_REMETENTE = os.getenv("SENHA_REMETENTE") or getpass("Senha de app: ")
ASSUNTO = input("Assunto do e-mail: ").strip() or "Assunto do E-mail"
MENSAGEM = input("Mensagem do e-mail: ").strip() or "Olá! Este é um e-mail enviado automaticamente."

# 2. Selecionar o arquivo com os contatos
root = Tk()
root.withdraw()
caminho_arquivo = filedialog.askopenfilename(
    title="Selecione um arquivo com e-mails",
    filetypes=[("Planilhas", "*.xlsx"), ("Textos", "*.txt"), ("CSV", "*.csv")],
)
root.destroy()

if not caminho_arquivo:
    print("Nenhum arquivo foi selecionado. Encerrando o script.")
    raise SystemExit

# 3. Carregar os e-mails do arquivo selecionado
try:
    lista_destinatarios = carregar_contatos(caminho_arquivo)
    print(f"Total de {len(lista_destinatarios)} contatos válidos carregados com sucesso!")
except Exception as e:
    print(f"Erro ao ler o arquivo: {e}")
    raise SystemExit

# 4. Enviar os e-mails
if lista_destinatarios:
    try:
        print("Conectando ao servidor...")
        servidor = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        servidor.starttls()
        servidor.login(EMAIL_REMETENTE, SENHA_REMETENTE)
        print("Login efetuado!")

        for destinatario in lista_destinatarios:
            msg = MIMEMultipart()
            msg["From"] = EMAIL_REMETENTE
            msg["To"] = destinatario
            msg["Subject"] = ASSUNTO

            msg.attach(MIMEText(MENSAGEM, "plain", "utf-8"))
            servidor.sendmail(EMAIL_REMETENTE, destinatario, msg.as_string())
            print(f"E-mail enviado para: {destinatario}")

    except Exception as e:
        print(f"Ocorreu um erro no envio: {e}")
    finally:
        if "servidor" in locals():
            servidor.quit()
        print("Conexão encerrada.")
else:
    print("Nenhum e-mail válido encontrado no arquivo selecionado.")
