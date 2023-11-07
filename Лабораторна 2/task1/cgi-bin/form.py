#!/usr/bin/env python3

print("Content-type: text/html; charset=utf-8\n")

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import cgi

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
print("<html>")
print("<head>")
print("<title>Результати опитування</title>")
print("</head>")
print("<body>")

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

# Закінчення HTML-сторінки
print("</body>")
print("</html>")
