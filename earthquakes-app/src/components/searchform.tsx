'use client';

import { searchEarthquakes } from "@/actions/search";
import SearchButton from "./searchButton";

export default function SearchForm() {
  return (
        <form action={async (formData) => {
            const result = await searchEarthquakes(formData);
            if (result && result.error) {
                alert('Error searching earthquakes: ' + result.error);
            }
          }}
          className="flex flex-col gap-4 mb-8 items-center"
        >
            <div className="flex w-full max-w-xs gap-2 flex-col sm:flex-row sm:max-w-2xl">
              <input
              name="startYear"
              type="number"
              min="1900"
              max={new Date().getFullYear()}
              placeholder="Start year"
              required
              className="w-35 px-4 border border-red-400 rounded-md focus:outline-none focus:ring-2 focus:ring-red-400 sm:py-2"
              />
              <span className="self-center text-gray-600 hidden sm:flex">-</span>
              <input
                name="endYear"
                type="number"
                min="1900"
                max={new Date().getFullYear()}
                placeholder="End year"
                required
                className="w-35 px-4 border border-red-400 rounded-md focus:outline-none focus:ring-2 focus:ring-red-400 sm:py-2"
              />
              <input
                name="minMagnitude"
                type="number"
                min="0"
                step="0.1"
                placeholder="Min magnitude"
                required
                className="flex-1 px-4 py-2 border border-red-400 rounded-md focus:outline-none focus:ring-2 focus:ring-red-400"
              />
              <SearchButton />
            </div>
        </form>
  );
}
