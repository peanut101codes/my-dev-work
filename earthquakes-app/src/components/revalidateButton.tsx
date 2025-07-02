import { clearEarthquakes } from '@/actions/search';
import { revalidatePath } from 'next/cache';

export default function RevalidateButton() {
  return (
    <form action={async () => {
        'use server';
        await clearEarthquakes();
        revalidatePath('/');
        }}
      className="flex flex-col gap-4 items-center"
    >
      <button
        type="submit"
        className="px-4 py-2 bg-[#002984] text-white font-semibold rounded-md hover:bg-[#757de8] transition
        min-w-[284px] sm:min-w-[320px] lg:w-auto lg:min-w-0 lg:max-w-40"

      >
        Clear Search
      </button>
    </form>
  );
}