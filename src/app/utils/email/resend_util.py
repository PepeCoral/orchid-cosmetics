import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

load_dotenv()

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

def send_email(request, email, order_identifier):
    # Build URL based on the current host
    base_url = request.build_absolute_uri('/')[:-1]  # remove trailing slash
    order_url = f"{base_url}/orders/uuid/{order_identifier}"

    html_template = """
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8" />
        <title>Orchid Cosmetics - Detalles de tu pedido</title>
      </head>
      <body style="font-family: Arial, sans-serif; background-color: #f3f0f8; padding: 40px;">
        <div style="max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); border-top: 6px solid #7b3fa1;">

          <h2 style="text-align:center; color:#4a2767; margin-bottom: 20px; font-weight: 600;">
            Orchid Cosmetics
          </h2>

          <p style="color:#444; font-size: 16px; line-height: 1.6;">
            Hola, gracias por tu compra en <strong>Orchid Cosmetics</strong>.
            Tu pedido ha sido creado con éxito y ahora puedes consultarlo en el siguiente enlace.
          </p>

          <div style="text-align:center; margin: 32px 0;">
            <a href="{{ORDER_URL}}"
               style="background:#7b3fa1; color:white; padding:14px 28px; text-decoration:none; font-size:16px; border-radius:8px; display:inline-block; font-weight:600;">
              Ver mi pedido
            </a>
          </div>

          <p style="color:#555; font-size:15px; line-height:1.6;">
            Si el botón no funciona, también puedes acceder directamente a este enlace:<br>
            <a href="{{ORDER_URL}}" style="color:#7b3fa1;">{{ORDER_URL}}</a>
          </p>

          <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">

          <p style="color:#777; text-align:center; font-size:12px; line-height:1.5;">
            Este es un correo automático. Si no realizaste ningún pedido, puedes ignorar este mensaje.
          </p>

        </div>
      </body>
    </html>
    """

    html_content = html_template.replace("{{ORDER_URL}}", order_url)

    msg = MIMEText(html_content, "html")
    msg["Subject"] = f"Detalles de tu pedido ({order_identifier}) - Orchid Cosmetics"
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            smtp.send_message(msg)
        print(f"Email enviado a {email}")
    except Exception as e:
        print(f"Error enviando email: {e}")
