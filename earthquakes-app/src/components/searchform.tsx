'use client';

import { searchEarthquakes } from "@/actions/search";
import SearchButton from "./searchButton";

export interface SearchFormProps {
  searchParams: {
    startYear: string;
    endYear: string;
    minMagnitude: string;
    orderBy: string;
  };
}

export default function SearchForm({ searchParams }: SearchFormProps) {
  return (
        <form action={async (formData) => {
            const startYear = formData.get('startYear');
            if (!startYear || isNaN(Number(startYear))) {
              const input = document.querySelector('input[name="startYear"]') as HTMLInputElement | null;
              if (input) {
                formData.set('startYear', input.placeholder);
              }
            }
            const endYear = formData.get('endYear');
            if (!endYear || isNaN(Number(endYear))) {
              const input = document.querySelector('input[name="endYear"]') as HTMLInputElement | null;
              if (input) {
                formData.set('endYear', input.placeholder);
              }
            }
            const minMagnitude = formData.get('minMagnitude');
            if (!minMagnitude || isNaN(Number(minMagnitude))) {
              const input = document.querySelector('input[name="minMagnitude"]') as HTMLInputElement | null;
              if (input) {
                formData.set('minMagnitude', input.placeholder);
              }
            }
            const result = await searchEarthquakes(formData);
            if (result && result.error) {
                alert('Error searching earthquakes: ' + result.error);
            }
          }}
          className="flex flex-col gap-4 mb-8 items-center"
        >
            <div className="flex w-full max-w-xs gap-2 flex-col md:flex-row md:max-w-2xl">
              <input
              name="startYear"
              type="number"
              min="1900"
              max={new Date().getFullYear()}
              placeholder={searchParams.startYear || "Start year"}
              required={!searchParams.startYear}
              className="px-2 border border-red-400 rounded-md focus:outline-none focus:ring-2 focus:ring-red-400"
              style={{ minWidth: '110px' }}
              />
              <span className="self-center text-gray-600 hidden md:flex">-</span>
              <input
              name="endYear"
              type="number"
              min="1900"
              max={new Date().getFullYear()}
              placeholder={searchParams.endYear || "End year"}
              required={!searchParams.endYear}
              className="px-2 border border-red-400 rounded-md focus:outline-none focus:ring-2 focus:ring-red-400"
              style={{ minWidth: '110px' }}
              />
              <input
              name="minMagnitude"
              type="number"
              min="0"
              max="9"
              step="0.1"
              placeholder={searchParams.minMagnitude || "Min magnitude"}
              required={!searchParams.minMagnitude}
              className="flex-1 px-2 border border-red-400 rounded-md focus:outline-none focus:ring-2 focus:ring-red-400"
              style={{ minWidth: '150px' }}
              />
                <select
                name="orderby"
                className="flex-1 px-2 border border-red-400 rounded-md focus:outline-none focus:ring-2 focus:ring-red-400 mb-2 md:mb-0"
                defaultValue={searchParams.orderBy || 'time-asc'}
                >
                <option value="">Order by ...</option>
                <option value="time">Time (Newest)</option>
                <option value="time-asc">Time (Oldest)</option>
                <option value="magnitude">Magnitude (Highest)</option>
                <option value="magnitude-asc">Magnitude (Lowest)</option>
                </select>
              <SearchButton />
            </div>
        </form>
  );
}
