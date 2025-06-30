import { clearEarthquakes } from '@/actions/search';
import { revalidatePath } from 'next/cache';

export default function RevalidateButton() {
  return (
    <form action={async () => {
        'use server';
        await clearEarthquakes();
        revalidatePath('/');
        }}
        className="flex md:justify-center items-center mb-4"
    >
    <div className="flex flex-col sm:flex-row items-start sm:items-center">
      <button
        type="submit"
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
      >
        Revalidate
      </button>
      <span className="text-sm text-gray-600 mt-2 sm:mt-0 sm:ml-2">
        Clear your search history cached by server
      </span>
    </div>
    </form>
  );
}