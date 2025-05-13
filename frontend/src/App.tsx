import {useEffect, useState} from "react";
import {getRecommendations, Movie} from "./services/api";

function App() {
    const [recs, setRecs] = useState<Movie[] | null>(null);

    useEffect(() => {
        // for demo, hardcode a username:
        getRecommendations("alice")
            .then(setRecs)
            .catch(console.error);
    }, []);

    if (!recs) return <div>Loading recommendations…</div>;

    return (
        <div>
            <h1>Your Movie Recommendations</h1>
            <ul>
                {recs.map(m => (
                    <li key={m.movie_id}>
                        <strong>{m.title}</strong>: {m.overview}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default App;