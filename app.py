from flask import Flask, render_template_string,render_template, request, redirect, url_for
from models import db, Player
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/")
def index():
    players = Player.query.all()
    return render_template("index.html", players=players)


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

        return redirect(url_for("index"))

    return render_template("register.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
