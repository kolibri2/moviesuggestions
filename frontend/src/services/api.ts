export interface Movie {
    movie_id: number;
    title: string;
    overview: string;
    movie_key: number;
}

const BASE = ""; // empty so fetch("/...") hits CRA proxy

export async function getRecommendations(username: string): Promise<Movie[]> {
    const res = await fetch(
        `${BASE}/get_recommendation?username=${encodeURIComponent(username)}`
    );
    if (!res.ok) throw new Error("API error");
    return res.json();
}

export async function getAllMovies(): Promise<Movie[]> {
    const res: Response = await fetch(
        `${BASE}/all_movies`
    );

    if (!res.ok) throw new Error("API error");
    return res.json();
}


export async function createUser(username: string) {
    const res: Response = await fetch(
        `${BASE}/users?username=${encodeURIComponent(username)}`, {method: 'POST'}
    );
    const message = await res.text();
    if (!res.ok) throw new Error("API error");
    return message
}