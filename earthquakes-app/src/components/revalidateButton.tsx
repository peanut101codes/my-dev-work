'use client';

import FormSubmitButton from './formButton';
import { clearEarthquakes } from '@/actions/search';


export default function RevalidateButton() {
  return (
    <form action={async () => {
        await clearEarthquakes();
      }}
      className="flex flex-col gap-4 items-center"
    >
      <div className="flex gap-2 flex-col lg:flex-row w-full max-w-xs lg:max-w-3xl">
        <FormSubmitButton
          idleText="Clear Search"
          pendingText="Clearing..."
        />
      </div>

    </form>
  );
}