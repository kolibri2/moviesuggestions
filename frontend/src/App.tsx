// src/App.tsx
import React, {useState} from 'react';
import {MoviePicker} from './components/MoviePicker';
import type {Movie} from './services/api';
import {useRecommendations} from './hooks/useRecommendations';
import {UserForm} from './components/UserForm';
import {RecommendationList} from './components/RecommendationList';
import {CreateUserForm} from "./components/CreateUser";

export default function App() {
    const [username, setUsername] = useState('');
    const {recs, loading, error, fetchRecs} = useRecommendations();
    const [chosen, setChosen] = useState<Movie | null>(null);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (username.trim()) {
            fetchRecs(username.trim());
        }
    };

    return (
        <div style={{maxWidth: 600, margin: '0 auto', padding: 20}}>
            <h1>Movie Recommender</h1>

            {/* Username form */}
            <UserForm
                username={username}
                onUsernameChange={setUsername}
                onSubmit={handleSubmit}
            />
            {loading && <p>Loading recommendations…</p>}
            {error && <p style={{color: 'red'}}>Error: {error}</p>}
            {!loading && !error && <RecommendationList movies={recs}/>}

            {/* Movie picker */}
            <h2>Or pick a movie from the full list</h2>
            <MoviePicker onMovieSelect={setChosen}/>
            {chosen && (
                <div style={{marginTop: 20}}>
                    <h3>{chosen.title}</h3>
                    <p>{chosen.overview}</p>
                </div>
            )}


            <CreateUserForm/>

            {/* existing recommendation UI below… */}
        </div>

    );
}
