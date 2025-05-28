import React, {useState, useEffect} from 'react';
import {getAllMovies, Movie} from '../services/api';

interface MoviePickerProps {
    /** called with the selected Movie (or null if cleared) */
    onMovieSelect: (movie: Movie | null) => void;
}

export function MoviePicker({onMovieSelect}: MoviePickerProps) {
    const [movies, setMovies] = useState<Movie[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [selectedMovieId, setSelectedMovieId] = useState<string>('');

    useEffect(() => {
        setLoading(true);
        getAllMovies()
            .then(list => setMovies(list))
            .catch(err => setError(err.message || 'Failed to load movies'))
            .finally(() => setLoading(false));
    }, []);

    const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const idStr = e.target.value;
        setSelectedMovieId(idStr);

        // parse it
        const idNum = Number(idStr);
        const movie = movies.find(m => m.movie_key === idNum) || null;
        onMovieSelect(movie);
    };

    if (loading) return <p>Loading movies…</p>;
    if (error) return <p style={{color: 'red'}}>Error: {error}</p>;

    return (
        <select value={selectedMovieId} onChange={handleChange}>
            <option value="">— Select a movie —</option>
            {movies.map(m => (
                <option key={m.movie_key} value={m.movie_key}>
                    {m.title}
                </option>
            ))}
        </select>
    );
}
