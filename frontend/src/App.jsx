import { useEffect, useState } from 'react'
import './App.css'

const API = '/api'

async function jsonOrText(res) {
  const text = await res.text()
  try {
    return JSON.parse(text)
  } catch {
    return text
  }
}

export default function App() {
  const [usernameInput, setUsernameInput] = useState(
    () => localStorage.getItem('username') || ''
  )
  const [username, setUsername] = useState(
    () => localStorage.getItem('username') || ''
  )
  const [movies, setMovies] = useState([])
  const [recommendations, setRecommendations] = useState([])
  const [seen, setSeen] = useState([])
  const [status, setStatus] = useState('')

  useEffect(() => {
    fetch(`${API}/all_movies`)
      .then((r) => r.json())
      .then(setMovies)
      .catch(() => setStatus('Failed to load movies. Is the API running?'))
  }, [])

  useEffect(() => {
    if (!username) return
    refreshSeen()
  }, [username])

  async function refreshSeen() {
    const res = await fetch(
      `${API}/user/seen_movies?username=${encodeURIComponent(username)}`
    )
    const data = await jsonOrText(res)
    setSeen(Array.isArray(data) ? data : [])
  }

  async function setActiveUser() {
    const name = usernameInput.trim()
    if (!name) return
    setStatus(`Setting up ${name}...`)
    await fetch(`${API}/users?username=${encodeURIComponent(name)}`, {
      method: 'POST',
    })
    localStorage.setItem('username', name)
    setUsername(name)
    setRecommendations([])
    setStatus(`Active user: ${name}`)
  }

  async function rate(movieId, rating) {
    if (!username) {
      setStatus('Set a username first.')
      return
    }
    const res = await fetch(
      `${API}/rate_movie?username=${encodeURIComponent(
        username
      )}&movie_id=${movieId}&rating=${rating}`,
      { method: 'POST' }
    )
    const msg = await jsonOrText(res)
    setStatus(typeof msg === 'string' ? msg : JSON.stringify(msg))
    refreshSeen()
  }

  async function getRecommendations() {
    if (!username) {
      setStatus('Set a username first.')
      return
    }
    setStatus('Computing recommendations...')
    const res = await fetch(
      `${API}/get_recommendation?username=${encodeURIComponent(username)}`
    )
    const data = await jsonOrText(res)
    if (Array.isArray(data)) {
      setRecommendations(data)
      setStatus(`Got ${data.length} recommendations.`)
    } else {
      setRecommendations([])
      setStatus(typeof data === 'string' ? data : JSON.stringify(data))
    }
  }

  const seenSet = new Set(seen)

  return (
    <div className="app">
      <header>
        <h1>Movie suggestions</h1>
        <div className="user-bar">
          <input
            placeholder="username"
            value={usernameInput}
            onChange={(e) => setUsernameInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && setActiveUser()}
          />
          <button onClick={setActiveUser}>Set user</button>
          {username && <span className="active">→ {username}</span>}
        </div>
        {status && <p className="status">{status}</p>}
      </header>

      <section>
        <div className="section-head">
          <h2>Recommendations</h2>
          <button onClick={getRecommendations} disabled={!username}>
            Get recommendations
          </button>
        </div>
        {recommendations.length === 0 ? (
          <p className="muted">Rate a few movies, then click above.</p>
        ) : (
          <ul className="movie-list">
            {recommendations.map((m) => (
              <MovieCard key={m.internal_id} movie={m} onRate={rate} />
            ))}
          </ul>
        )}
      </section>

      <section>
        <h2>Browse & rate ({movies.length})</h2>
        <ul className="movie-list">
          {movies.map((m) => (
            <MovieCard
              key={m.internal_id}
              movie={m}
              onRate={rate}
              rated={seenSet.has(m.title)}
            />
          ))}
        </ul>
      </section>
    </div>
  )
}

function MovieCard({ movie, onRate, rated }) {
  return (
    <li className={`movie ${rated ? 'rated' : ''}`}>
      <div className="movie-head">
        <h3>{movie.title}</h3>
        {rated && <span className="badge">rated</span>}
      </div>
      <p className="overview">{movie.overview}</p>
      <div className="actions">
        <button className="like" onClick={() => onRate(movie.internal_id, 1)}>
          Like
        </button>
        <button className="dislike" onClick={() => onRate(movie.internal_id, 0)}>
          Dislike
        </button>
      </div>
    </li>
  )
}
