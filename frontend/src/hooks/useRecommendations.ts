import {useState} from 'react';
import {getRecommendations, Movie} from '../services/api';


export function useRecommendations() {
    const [recs, setRecs] = useState<Movie[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchRecs = async (username: string) => {
        setLoading(true);
        setError(null);
        try {
            const movies = await getRecommendations(username);
            setRecs(movies);
        } catch (err: any) {
            setError(err.message ?? 'An error occurred');
            setRecs([]);
        } finally {
            setLoading(false);
        }
    };

    return {recs, loading, error, fetchRecs};
}