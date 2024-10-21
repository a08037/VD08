from flask import Flask, render_template
import requests

app = Flask(__name__)

# Функция для получения случайной цитаты
def get_random_quote():
    try:
        # URL для API случайной цитаты
        url = "https://api.quotable.io/random"
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения с API цитат: {e}")
        # В случае ошибки, вернем сообщение об ошибке
        return {"content": "Цитата недоступна. Проверьте интернет-соединение.", "author": ""}

# Функция для получения случайного факта (резервный вариант)
def get_random_fact():
    try:
        # URL для API случайного факта
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения с API фактов: {e}")
        # В случае ошибки, вернем сообщение об ошибке
        return {"text": "Факт недоступен. Проверьте интернет-соединение."}

# Маршрут для главной страницы
@app.route('/')
def index():
    quote_data = get_random_quote()  # Пытаемся получить цитату
    # Если цитата недоступна, получаем случайный факт
    if quote_data['content'] == "Цитата недоступна. Проверьте интернет-соединение.":
        fact_data = get_random_fact()  # Получаем факт
        return render_template("index.html", quote=fact_data['text'], author="Random Fact")
    else:
        quote = quote_data['content']  # Извлекаем цитату
        author = quote_data['author']  # Извлекаем автора
        return render_template("index.html", quote=quote, author=author)

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)
