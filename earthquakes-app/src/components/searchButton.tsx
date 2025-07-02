import React from 'react';
import { useFormStatus } from 'react-dom';

export default function SearchButton() {
    const { pending } = useFormStatus();

    return (
        <div className="flex justify-center">
            <button
                disabled={pending}
                className="px-4 py-2 bg-blue-900 text-white font-semibold rounded-md hover:bg-blue-300 transition-colors 
                min-w-[284px] sm:min-w-[320px] lg:w-auto lg:min-w-0 lg:max-w-40"
                type="submit"
            >
                {pending ? 'Searching...' : 'Search'}
            </button>
        </div>
    );
}