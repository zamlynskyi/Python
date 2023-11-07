#!/usr/bin/env python3

# Очищення cookies
print("Set-Cookie: form_count=0; expires=Thu, 01 Jan 1970 00:00:00 GMT")

# Перенаправлення на головну сторінку
print("Location: /form.html")
print("Content-type: text/html; charset=utf-8\n")
print("")

# HTML-сторінка з повідомленням
print("<html>")
print("<head><title>Cookies видалені</title></head>")
print("<body>")
print("<h1>Cookies були видалені.</h1>")
print('<a href="/form.html">Повернутися</a>')
print("</body>")
print("</html>")
