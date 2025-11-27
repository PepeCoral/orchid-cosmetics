import os
from dotenv import load_dotenv
import requests

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL") 
SENDER_NAME = os.getenv("SENDER_NAME", "Orchid Cosmetics")

def send_email(request, email, order_identifier):
    if not BREVO_API_KEY:
        print("Error: BREVO_API_KEY no está configurada")
        return False
        
    if not SENDER_EMAIL:
        print("Error: SENDER_EMAIL no está configurada")
        return False

    # El resto de tu código funciona perfectamente...
    base_url = request.build_absolute_uri('/')[:-1]
    order_url = f"{base_url}/orders/uuid/{order_identifier}"

    html_template = """
    ... (tu template HTML)
    """

    html_content = html_template.replace("{{ORDER_URL}}", order_url)

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
        "htmlContent": html_content
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        print(f"Email enviado a {email}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error enviando email: {e}")
        return False