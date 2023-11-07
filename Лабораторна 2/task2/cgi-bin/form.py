#!/usr/bin/env python3
import cgi
import os

# Отримання даних з форми
form = cgi.FieldStorage()

# Отримання введених даних
name = form.getvalue("name")
email = form.getvalue("email")
age = form.getvalue("age")
gender = form.getvalue("gender")
interests = form.getlist("interests")
review = form.getvalue("review")

# Вивід заголовка та початок HTML-сторінки
print("Content-type: text/html; charset=utf-8\n")
print("<html>")
print("<head>")
print("<title>Результати опитування</title>")
print("</head>")
print("<body>")

def get_form_count():
    # Отримання кількості форм із cookies
    count = 0
    if "HTTP_COOKIE" in os.environ:
        cookies = os.environ["HTTP_COOKIE"]
        cookies_list = cookies.split("; ")
        for cookie in cookies_list:
            if cookie.startswith("form_count="):
                count = int(cookie.split("=")[1])
    return count

# Перевірка, чи всі обов'язкові поля заповнені
if not name or not email:
    print("<h1>Помилка: Будь ласка, заповніть обов'язкові поля (Ім'я та Email).</h1>")
else:
    # Вивід результатів опитування
    print("<h1>Результати опитування</h1>")
    print("<p><strong>Ім'я:</strong> " + name + "</p>")
    print("<p><strong>Email:</strong> " + email + "</p>")
    print("<p><strong>Вік:</strong> " + age + "</p>")
    print("<p><strong>Стать:</strong> " + gender + "</p>")
    print("<p><strong>Цікавості:</strong> " + ", ".join(interests) + "</p>")
    print("<p><strong>Відгук:</strong> " + review + "</p>")

    count = get_form_count()
    count += 1

    # Зберігання лічильника в cookies
    print(f"<br>Set-Cookie: form_count={count}")

# Виведення лічильника
print("<p><strong>Кількість заповнених форм:</strong> " + str(count) + "</p>")

# Кнопка для видалення cookies
print('<form action="/cgi-bin/clear_cookies.py" method="post">')
print('<input type="submit" value="Видалити всі cookies">')
print('</form>')

# Закінчення HTML-сторінки
print("</body>")
print("</html>")
