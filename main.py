import os
import re
import smtplib
import time
from getpass import getpass
from email import encoders
from email.mime.base import MIMEBase
from email.message import EmailMessage
from tkinter import Tk, filedialog
import pandas as pd


def validar_email(email: str) -> bool:
    return re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email.strip()) is not None


def carregar_contatos(caminho_arquivo: str) -> list[str]:
    extensao = os.path.splitext(caminho_arquivo)[1].lower()

    if extensao == ".xlsx":
        df = pd.read_excel(caminho_arquivo)
        emails = df.iloc[:, 0].dropna().astype(str).tolist()
    elif extensao == ".csv":
        df = pd.read_csv(caminho_arquivo)
        emails = df.iloc[:, 0].dropna().astype(str).tolist()
    else:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            emails = [linha.strip() for linha in arquivo]

    return [email for email in emails if validar_email(email)]


# 1. Configurações do servidor
SMTP_SERVER = os.getenv("SMTP_SERVER") or input("Servidor SMTP (ex.: smtp.gmail.com): ").strip()
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE") or input("E-mail do remetente: ").strip()
SENHA_REMETENTE = os.getenv("SENHA_REMETENTE") or getpass("Senha de app: ")
ASSUNTO = input("Assunto do e-mail: ").strip() or "Assunto do E-mail"
MENSAGEM = input("Mensagem do e-mail: ").strip() or "Olá! Este é um e-mail enviado automaticamente."
NOME_REMETENTE = os.getenv("NOME_REMETENTE") or "Seu Nome"
ANEXO = input("Caminho do anexo (opcional): ").strip()

# 2. Selecionar o arquivo com os contatos
root = Tk()
root.withdraw()
caminho_arquivo = filedialog.askopenfilename(
    title="Selecione um arquivo com e-mails",
    filetypes=[("Planilhas", "*.xlsx"), ("CSV", "*.csv"), ("Textos", "*.txt")],
)
root.destroy()

if not caminho_arquivo:
    print("Nenhum arquivo foi selecionado. Encerrando o script.")
    raise SystemExit

# 3. Carregar os e-mails do arquivo selecionado
try:
    lista_destinatarios = carregar_contatos(caminho_arquivo)
    lista_destinatarios = list(dict.fromkeys(lista_destinatarios))
    print(f"Total de {len(lista_destinatarios)} contatos válidos carregados com sucesso!")
except Exception as e:
    print(f"Erro ao ler o arquivo: {e}")
    raise SystemExit

# 4. Enviar os e-mails
if lista_destinatarios:
    total = len(lista_destinatarios)

    try:
        print("Conectando ao servidor...")
        servidor = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
        servidor.starttls()
        servidor.login(EMAIL_REMETENTE, SENHA_REMETENTE)
        print("Login efetuado!")

        for i, destinatario in enumerate(lista_destinatarios, start=1):
            print(f"[{i}/{total}] Enviando para {destinatario}")
            try:
                msg = EmailMessage()
                msg["From"] = EMAIL_REMETENTE
                msg["To"] = destinatario
                msg["Subject"] = ASSUNTO

                nome_destinatario = destinatario.split("@", 1)[0].replace(".", " ").replace("_", " ").title()
                corpo = MENSAGEM.format(nome=nome_destinatario)

                html = f"""
                <html>
                <body>
                    <h2>Olá!</h2>
                    <p>{corpo}</p>
                    <br>
                    <p>Atenciosamente,<br>{NOME_REMETENTE}</p>
                </body>
                </html>
                """

                msg.set_content(corpo)
                msg.add_alternative(html, subtype="html")

                if ANEXO and os.path.exists(ANEXO):
                    with open(ANEXO, "rb") as arquivo_anexo:
                        parte = MIMEBase("application", "octet-stream")
                        parte.set_payload(arquivo_anexo.read())
                    encoders.encode_base64(parte)
                    nome_arquivo = os.path.basename(ANEXO)
                    parte.add_header("Content-Disposition", f'attachment; filename="{nome_arquivo}"')
                    msg.add_attachment(parte.get_payload(), maintype="application", subtype="octet-stream", filename=nome_arquivo)

                servidor.sendmail(EMAIL_REMETENTE, destinatario, msg.as_string())
                print(f"✓ {destinatario}")

                with open("envios.log", "a", encoding="utf-8") as log:
                    log.write(f"{destinatario}\n")

            except Exception as e:
                print(f"✗ Erro em {destinatario}: {e}")

            time.sleep(2)

    except Exception as e:
        print(f"Ocorreu um erro no envio: {e}")
    finally:
        if "servidor" in locals():
            servidor.quit()
        print("Conexão encerrada.")
else:
    print("Nenhum e-mail válido encontrado no arquivo selecionado.")
