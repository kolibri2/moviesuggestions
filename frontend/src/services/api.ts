export interface Movie {
    movie_id: number;
    title: string;
    overview: string;
}

const BASE = ""; // empty so fetch("/...") hits CRA proxy

export async function getRecommendations(username: string): Promise<Movie[]> {
    const res = await fetch(
        `${BASE}/get_recommendation?username=${encodeURIComponent(username)}`
    );
    if (!res.ok) throw new Error("API error");
    return res.json();
}