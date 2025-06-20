from flask import Flask, request, render_template_string
from models import db, Player
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/")
def index():
    players = Player.query.all()
    return "<br>".join([
        f"{p.name} — {p.race}, {p.player_class}, Золото: {p.gold}, HP: {p.health}, Энергия: {p.energy}, Мана: {p.mana}"
        for p in players
    ]) or "Игроков пока нет"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        race = request.form["race"]
        player_class = request.form["player_class"]

        # Базовые параметры
        health = 100
        energy = None
        mana = None

        # Логика классов
        if player_class in ["Воин", "Разбойник"]:
            energy = 100
        elif player_class == "Маг":
            mana = 100

        new_player = Player(
            name=name,
            race=race,
            player_class=player_class,
            health=health,
            energy=energy,
            mana=mana
        )
        db.session.add(new_player)
        db.session.commit()

        return f"Игрок {name} успешно создан!"

    form_html = """
    <h2>Регистрация Игрока</h2>
    <form method="POST">
        Имя: <input type="text" name="name"><br>
        Раса:
        <select name="race">
            <option>Человек</option>
            <option>Орк</option>
            <option>Эльф</option>
            <option>Лесной Эльф</option>
            <option>Чупакабра</option>
        </select><br>
        Класс:
        <select name="player_class">
            <option>Воин</option>
            <option>Разбойник</option>
            <option>Маг</option>
        </select><br>
        <input type="submit" value="Создать">
    </form>
    """
    return render_template_string(form_html)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
