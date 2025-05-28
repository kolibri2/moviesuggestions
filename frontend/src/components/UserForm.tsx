import React from 'react';

interface UserFormProps {
    username: string;
    onUsernameChange: (value: string) => void;
    onSubmit: (e: React.FormEvent) => void;
}

/**
 * Renders the input field and submit button for username entry.
 */
export function UserForm({username, onUsernameChange, onSubmit}: UserFormProps) {
    return (
        <form onSubmit={onSubmit} style={{marginBottom: 20}}>
            <input
                type="text"
                placeholder="Enter your username"
                value={username}
                onChange={(e) => onUsernameChange(e.target.value)}
                style={{padding: 8, width: '70%', marginRight: 8}}
            />
            <button type="submit" style={{padding: '8px 16px'}}>
                Get Recommendations
            </button>
        </form>
    );
}