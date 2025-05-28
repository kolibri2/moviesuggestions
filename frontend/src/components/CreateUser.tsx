import React, {useState} from 'react';
import {createUser} from '../services/api';

export function CreateUserForm() {
    const [username, setUsername] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState(false);
    const [info, setInfo] = useState<string | null>(null)

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        setSuccess(false);
        setInfo(null)
        if (!username.trim()) {
            setError('Username cannot be blank');
            return;
        }
        setLoading(true);

        try {
            const message = await createUser(username.trim())

            setInfo(message)

            setSuccess(true);
            setUsername('');
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} style={{marginBottom: 20}}>
            <h2>Create a username</h2>

            <input
                type="text"
                placeholder="Choose a username"
                value={username}
                onChange={e => setUsername(e.target.value)}
                style={{padding: 8, width: '70%', marginRight: 8}}
            />

            <button type="submit" disabled={loading} style={{padding: '8px 16px'}}>
                {loading ? 'Creating…' : 'Sign Up'}
            </button>

            {error && <p style={{color: 'red'}}>Error: {error}</p>}
            {success && <p style={{color: 'green'}}>{info}</p>}
        </form>
    );
}
