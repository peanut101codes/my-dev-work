import React from 'react';
import { useFormStatus } from 'react-dom';

interface FormSubmitButtonProps {
    idleText: string;
    pendingText: string;
    disabled?: boolean;
}

export default function FormSubmitButton({
    idleText,
    pendingText,
    disabled = false,
}: FormSubmitButtonProps) {
    const { pending } = useFormStatus();

    return (
        <button
            disabled={pending || disabled}
            className = "px-4 py-2 bg-blue-900 text-white font-semibold rounded-md hover:bg-blue-700 lg:w-auto lg:min-w-0 lg:max-w-40"
            type="submit"
        >
            {pending ? pendingText : idleText}
        </button>
    );
}