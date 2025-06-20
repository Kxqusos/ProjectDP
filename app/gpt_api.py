import g4f

def generate_recipe(ingredients: list[str]) -> str:
    prompt = (
        f"У меня есть такие продукты: {', '.join(ingredients)}. " \
        "Предложи подробный пошаговый рецепт их приготовления на русском языке." \
        "В конце говори только Приятного аппетита" \
        "Также не размечай текст жирным через **" \
        "Используй только русский язык"
    )
    try:
        response = g4f.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            stream=False
        )
        return str(response)
    except Exception as e:
        return f"Ошибка генерации рецепта: {e}"