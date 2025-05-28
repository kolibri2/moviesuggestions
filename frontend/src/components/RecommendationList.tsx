import React from 'react';
import {Movie} from '../services/api';

interface RecommendationListProps {
    movies: Movie[];
}

/**
 * Displays a list of movie recommendations or a placeholder message.
 */
export function RecommendationList({movies}: RecommendationListProps) {
    if (movies.length === 0) {
        return <p>No recommendations yet—enter a username above.</p>;
    }
    return (
        <ul>
            {movies.map(m => (
                <li key={m.movie_id} style={{marginBottom: 12}}>
                    <strong>{m.title}</strong>
                    <p style={{margin: '4px 0'}}>{m.overview}</p>
                </li>
            ))}
        </ul>
    );
}
