import os
from dotenv import load_dotenv
import requests

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_NAME = os.getenv("SENDER_NAME", "Orchid Cosmetics")

def send_email(request, email, order_identifier, total, address, name=None):
    if not BREVO_API_KEY:
        print("Error: BREVO_API_KEY no está configurada")
        return False

    if not SENDER_EMAIL:
        print("Error: SENDER_EMAIL no está configurada")
        return False

    base_url = request.build_absolute_uri('/')[:-1]
    order_url = f"{base_url}/orders/uuid/{order_identifier}"

    if name:
        greeting = f"Hola {name}, gracias por tu compra en <strong>Orchid Cosmetics</strong>."
    else:
        greeting = "Hola, gracias por tu compra en <strong>Orchid Cosmetics</strong>."

    html_template = f"""
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
            {greeting}<br>
            Tu pedido ha sido creado con éxito y ahora puedes consultarlo en el siguiente enlace.
          </p>

          <div style="text-align:center; margin: 32px 0;">
            <a href="{order_url}"
               style="background:#7b3fa1; color:white; padding:14px 28px; text-decoration:none; font-size:16px; border-radius:8px; display:inline-block; font-weight:600;">
              Ver mi pedido
            </a>
          </div>

          <p style="color:#555; font-size:15px; line-height:1.6;">
            Si el botón no funciona, también puedes acceder directamente a este enlace:<br>
            <a href="{order_url}" style="color:#7b3fa1;">{order_url}</a>
          </p>

          <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">

          <h3 style="color:#4a2767; margin-bottom:10px;">Detalles del pedido</h3>
          <p style="color:#444; font-size: 15px; line-height: 1.6;">
            <strong>Total pagado:</strong> {total} €<br>
            <strong>Dirección de entrega:</strong><br>
            {address.replace('\n','<br>')}
          </p>

          <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">

          <p style="color:#777; text-align:center; font-size:12px; line-height:1.5;">
            Este es un correo automático. Si no realizaste ningún pedido, puedes ignorar este mensaje.
          </p>
        </div>
      </body>
    </html>
    """

    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    data = {
        "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
        "to": [{"email": email}],
        "subject": f"Detalles de tu pedido ({order_identifier}) - Orchid Cosmetics",
        "htmlContent": html_template
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        print(f"Email enviado a {email}")
    except requests.exceptions.RequestException as e:
        print(f"Error enviando email: {e}")
