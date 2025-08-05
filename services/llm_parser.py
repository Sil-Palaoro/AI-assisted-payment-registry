import anthropic

from config.settings import ANTHROPIC_API_KEY

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def build_llm_prompt(texto):
    return f"""
        A continuación tienes el texto extraído de un comprobante de pago. Extrae los siguientes datos en formato JSON con claves en minúscula:
        
        - nombre: nombre completo de quien hizo el pago (originante)
        - monto: valor numérico del pago, sin símbolos, punto como separador decimal
        - fecha: fecha del pago en formato yyyy-mm-dd
        - destinatario: debe ser uno de estos tres valores exactos: "Silvina Palaoro", "Olivia Deane" o "Olivia Isabel Deane"
        - medio: medio de pago del destinatario, si se indica (ej: Banco Nación, PayPal, Wise, MercadoPago, etc.)
        
        Texto del comprobante:
        \"\"\"
        {texto}
        \"\"\"
        
        Devuelve **solo el JSON**. Si alguno de los datos **no está expresado explícitamente** en el texto, colócalo como null.
        
        ❗ Reglas importantes:
        
        - No inventes el nombre del originante: si no aparece claramente en el texto, el campo "nombre" debe ser null.
        - Si aparece el nombre del destinatario pero no el pagador, no los confundas. "nombre" ≠ "destinatario".
        - Si no se menciona el medio de pago pero el destinatario es Olivia, puedes inferir "Wise o PayPal?" (entre comillas). Si es Silvina, "Bco Nación o MP?".
        
        Ejemplo correcto:
        {{
          "nombre": null,
          "monto": "240.00",
          "fecha": "2025-02-21",
          "destinatario": "Olivia Isabel Deane",
          "medio": "Wise o PayPal?"
        }}
        
        Responde sólo el JSON, sin explicaciones ni texto adicional.
        """


def parse_with_llm(texto):
    prompt = build_llm_prompt(texto)

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=500,
        temperature=0,
        messages=[
            {"role":"user", "content": prompt}
        ]
    )

    #Esperamos que Claude devuelva un JSON directamente
    respuesta_texto = response.content[0].text

    import json
    try:
        return json.loads(respuesta_texto)
    except json.JSONDecodeError:
        print("Error al interpretar la respuesta del LLM:")
        print(respuesta_texto)
        return {}