from flask import Flask, jsonify, request # flask crea la aplicación web, jsonify convierte diccionarios/listas d epyhton en JSON y request deja leer lo que nos manda el cliente (JSON del POST)
from flask_cors import CORS # permite que http://localhost:3000 (React) pueda llamar a http://localhost:5000 (Flask). # Importa CORS para permitir que React (otro puerto) pueda llamar a este backend sin bloqueo
from flask_sqlalchemy import SQLAlchemy # es le ORM, permite crear modelos (clases) que representan tablas y hacer queries sin SQL manual


# llamando dependencias e inicializando la app
app = Flask(__name__)
CORS(app) # Esto permite llamadas desde http://localhost:3000 hacia http://localhost:5001.

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///songs.db" # URI de la base de datos, sqlite es un motor de base de datos liviano que guarda todo en un archivo local llamado songs.db
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Desactiva el seguimiento de modificaciones para mejorar el rendimiento

db = SQLAlchemy(app) # Inicializa SQLAlchemy con la aplicación Flask

# Modelo ORM: Esta clase representa una tabla en la BD
class Song(db.Model):
    # nombre real de la tabla en la bd
    __tablename__ = "songs"

    # columnas de la tabla
    idSong = db.Column(db.Integer, primary_key=True) 
    songName = db.Column(db.String(250), nullable=False)
    artist =db.Column(db.String(250), nullable=False)

    # metodo para convertir un objeto song a diccionario (para devolverlo como JSON)
    def to_dict(self):
        return {
            "idSong": self.idSong,
            "songName": self.songName,
            "artist": self.artist
        }

# Ruta simple para probar si el bacckend responde
@app.route("/")
def home():
    return "¡Hola desde Flask!"

# Get canciones: devuelve una lista de canciones en formato JSON
@app.route("/songs", methods=["GET"])
def get_song():
    # Song.query es ORM: hace consultas a la tabla sin SQL
    # Order_by ordena por idSong, all() devuelve todas las filas como objetos Song
    songs = Song.query.order_by(Song.idSong.desc()).all()

    # convertimos cada Song a dict y devolvemos una lista de JSON
    return jsonify([s.to_dict() for s in songs]), 200 # 200 es el código HTTP de éxito

# Post canciones: ruta para crear/agregar una canción
@app.route("/songs", methods=["POST"])
def add_song():
    # request.get_json() lee el JSon que mande React/Postman 
    data = request.get_json()

    if not data:
        return jsonify({"error": "No se proporcionó ningún dato"}), 400 # 400 es el código HTTP de error por mala solicitud
    
    # Agarramos el name y artist del JSON
    songName = (data.get("songName") or "").strip() # .strip() elimina espacios al inicio/final
    artist = (data.get("artist") or "").strip()

    # Validamos ambos campos son obligatorios
    if not songName or not artist:
        return jsonify({"error": "Los campos 'songName' y 'artist' son obligatorios"}), 400

    # Creamos un nuevo objeto Song con los datos, aqui es donde ORM reemplaza el INSERT SQL
    song = Song(songName=songName, artist=artist)

    db.session.add(song) # Agregamos el objeto a la sesión (como “preparar” el insert)
    db.session.commit() # Confirmamos los cambios en la base (aquí se guarda de verdad en songs.db)
    
    return jsonify(song.to_dict()), 201 # Devolvemos la canción creada como JSON, 201 es el código HTTP de recurso creado


# Este bloque solo se ejecuta si corres el archivo directamente: python app.py
if __name__ == "__main__":
    # necesitamos un contexto de la app para que SQLAlchemy pueda crear las tablas
    with app.app_context():
        db.create_all() # Crea las tablas si no existen (songs.db + tabla songs)

    # corre el servidor en el puerto 5000, debug=True reinicia automáticamente cuando guardas cambios (para desarrollo)
    app.run(host="0.0.0.0", port=5001, debug=True)
