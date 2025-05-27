import g4f
import base64

def recognize_ingridients(img_path: str) -> list:
    with open(img_path, "rb") as f:
        img_bytes = f.read()
    img_b64 = base64.b64encode(img_bytes).decode()
    prompt = (
        "На фотографии изображены продукты. "
        "Пожалуйста, перечисли только сами продукты (игнорируя упаковку, этикетки и текст), "
        "списком через запятую, без лишних описаний. "
        "Пример: яйцо, огурец, сыр, яблоко."
    )
    messages = [
        {"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
        ]}
    ]
    
    try:
        response = g4f.ChatCompletion.create(
            model = "gpt-4o",
            messages = messages,
            stream = False
        )   

        answer = str(response)
        print(answer)
        products = [p.strip().lower() for p in answer.split(",") if p.strip()]
        return products
    except Exception as e:
        print(f"Ошибка vision g4f: {e}")
        return []