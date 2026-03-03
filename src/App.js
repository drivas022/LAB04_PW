import { useEffect, useMemo, useState } from "react";
import "./App.css";

const API_URL = "http://localhost:5001";

export default function App() {
  const [songName, setSongName] = useState("");
  const [artist, setArtist] = useState("");
  const [songs, setSongs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [query, setQuery] = useState("");

  async function loadSongs() {
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API_URL}/songs`);
      const data = await res.json();
      setSongs(Array.isArray(data) ? data : []);
    } catch (e) {
      setError("No pude conectar con el backend. ¿Está corriendo en 5001?");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadSongs();
  }, []);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return songs;
    return songs.filter((s) => {
      const n = (s.songName || "").toLowerCase();
      const a = (s.artist || "").toLowerCase();
      return n.includes(q) || a.includes(q);
    });
  }, [songs, query]);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    const name = songName.trim();
    const art = artist.trim();

    if (!name || !art) {
      setError("Pon nombre de canción y artista 🙂");
      return;
    }

    try {
      const res = await fetch(`${API_URL}/songs`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ songName: name, artist: art }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data?.error || "Error al guardar");
        return;
      }

      setSongName("");
      setArtist("");
      await loadSongs();
    } catch (e) {
      setError("No pude guardar. Revisa que Flask esté corriendo.");
    }
  }

  return (
    <div className="page">
      <header className="topbar">
        <div className="brand">
          <div className="logoDot" />
          <div>
            <div className="brandTitle">Songs</div>
            <div className="brandSub">Library</div>
          </div>
        </div>

        <input
          className="search"
          placeholder="Buscar canción o artista"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </header>

      <main className="container">
        <section className="card">
          <div className="cardHeader">
            <h3>Agregar canción</h3>
            <span className="pill">Flask + ORM</span>
          </div>

          <form className="form" onSubmit={handleSubmit}>
            <div className="field">
              <label>Nombre</label>
              <input
                value={songName}
                onChange={(e) => setSongName(e.target.value)}
                placeholder="Ej: Yellow"
              />
            </div>

            <div className="field">
              <label>Artista</label>
              <input
                value={artist}
                onChange={(e) => setArtist(e.target.value)}
                placeholder="Ej: Coldplay"
              />
            </div>

            <button className="btn" type="submit">
              Guardar
            </button>
          </form>

          {error && <div className="error">{error}</div>}
        </section>

        <section className="card">
          <div className="cardHeader">
            <h3>Tu biblioteca</h3>
            <span className="muted">
              {loading ? "Cargando..." : `${filtered.length} canción(es)`}
            </span>
          </div>

          <div className="list">
            {loading ? (
              <div className="empty">Cargando canciones…</div>
            ) : filtered.length === 0 ? (
              <div className="empty">No hay canciones todavía.</div>
            ) : (
              filtered.map((s) => (
                <div className="row" key={s.idSong}>
                  <div className="cover" />
                  <div className="meta">
                    <div className="title">{s.songName}</div>
                    <div className="subtitle">{s.artist}</div>
                  </div>
                  <div className="right">
                    <span className="tiny">ID {s.idSong}</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </section>
      </main>

      <footer className="footer">
        <span className="tiny">API: {API_URL}</span>
      </footer>
    </div>
  );
}