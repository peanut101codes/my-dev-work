import React from 'react';
import { useFormStatus } from 'react-dom';

export default function SearchButton() {
    const { pending } = useFormStatus();

    return (
        <button
            disabled={pending}
            className="px-4 py-2 bg-[#002984] text-white font-semibold rounded-md hover:bg-[#757de8] transition md:w-[135px]"
            type="submit"
        >
            {pending ? 'Searching...' : 'Search'}
        </button>
    );
}