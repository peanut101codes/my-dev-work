import React from 'react';
import { useFormStatus } from 'react-dom';

export default function SearchButton() {
    const { pending } = useFormStatus();

    return (
        <button
            disabled={pending}
            className="px-4 py-2 bg-red-600 text-white font-semibold rounded-md hover:bg-red-700 transition"
            type="submit"
        >
            {pending ? 'Searching...' : 'Search'}
        </button>
    );
}