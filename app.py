from flask import Flask, render_template_string,render_template, request, redirect, url_for, session
from models import db, Player
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/")
def index():
    player_id = session.get("player_id")
    if player_id:
        player = Player.query.get(player_id)
        if player:
            return render_template("index.html", player=player)
    return render_template("index.html", player=None, show_auth=True)


@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("name").strip()
    player = Player.query.filter_by(name=name).first()
    if not player:
        # Передаём имя как параметр GET
        return redirect(url_for("register", name=name))
    session["player_id"] = player.id
    return redirect(url_for("index"))



@app.route("/profile")
def profile():
    player_id = session.get("player_id")
    if not player_id:
        return redirect(url_for("register"))

    player = Player.query.get(player_id)
    return render_template("profile.html", player=player)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        race = request.form["race"]
        player_class = request.form["player_class"]

        # базовые параметры
        health = 100
        energy = 100 if player_class in ["Воин", "Разбойник"] else None
        mana = 100 if player_class == "Маг" else None

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
        session["player_id"] = new_player.id
        return redirect(url_for("index"))

    # получаем name из GET-запроса, если передано
    name = request.args.get("name", "")
    return render_template("register.html", name=name)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
