from flask import Flask, render_template, request, make_response

app = Flask(__name__)

# Список для збереження відгуків
reviews = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        review = request.form['review']

        # Перевірка на дублікат відгука
        for _, existing_review in reviews:
            if existing_review == review:
                return "Ви вже додали цей відгук."

        if name and review:
            reviews.append((name, review))
            response = make_response(render_template('index.html', reviews=reviews))
            # Додавання куки для відзначення відгука як вже доданого
            response.set_cookie(f'review_{len(reviews)}', review)
            return response
    return render_template('index.html', reviews=reviews)

if __name__ == '__main__':
    app.run(debug=True)
