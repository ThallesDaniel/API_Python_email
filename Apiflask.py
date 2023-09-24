from flask import Flask, request, jsonify 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configurações do servidor SMTP e conta de e-mail
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'seuemailaqui'
SMTP_PASSWORD = 'suasenhaaqui'

@app.route('/enviar-email', methods=['POST'])
def enviar_email():
    try:
        # Recebe os dados do formulário
        data = request.form
        destinatario = data['destinatarioaqui']
        assunto = data['[ASSUNTO AQUI]']
        mensagem = data['mensagem']
        anexo = request.files.get('anexo')

        # Configura a mensagem de e-mail
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = destinatario
        msg['Subject'] = assunto
        msg.attach(MIMEText(mensagem, 'plain'))

        # Anexa o arquivo, se fornecido
        if anexo:
            anexo_multipart = MIMEApplication(anexo.read(), Name=anexo.filename)
            anexo_multipart['Content-Disposition'] = f'attachment; filename="{anexo.filename}"'
            msg.attach(anexo_multipart)

        # Conecta-se ao servidor SMTP e envia o e-mail
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, destinatario, msg.as_string())
        server.quit()

        return jsonify({'message': 'E-mail enviado com sucesso!'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
