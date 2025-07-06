'use client';

import { useState } from 'react';
import { searchEarthquakes } from "@/actions/search";
import FormSubmitButton from './formButton';

export interface SearchFormProps {
  searchParams: {
    startYear: string;
    endYear: string;
    minMagnitude: string;
    orderBy: string;
  };
}

export default function SearchForm({ searchParams }: SearchFormProps) {
  const [inputStartYear, setInputStartYear] = useState(searchParams.startYear || '');
  const [inputEndYear, setInputEndYear] = useState(searchParams.endYear || '');
  const [inputMinMagnitude, setInputMinMagnitude] = useState(searchParams.minMagnitude || ''); 
  const [inputOrderBy, setInputOrderBy] = useState(searchParams.orderBy || 'time-asc');

  return (
        <form action={async (formData) => {
            const startYear = Number(formData.get('startYear'));
            const endYear = Number(formData.get('endYear'));
            if (endYear < startYear) {
              alert('End-year cannot be earlier than start-year.');
              return;
            }
            const result = await searchEarthquakes(formData);
            if (result && result.error) {
                alert('Error searching earthquakes: ' + result.error);
            }
          }}
          className="flex flex-col gap-4 items-center"
        >
            <div className="flex gap-2 flex-col lg:flex-row w-full max-w-xs lg:max-w-3xl">
              <input
              name="startYear"
              type="number"
              min="1900"
              max={new Date().getFullYear()}
              placeholder={searchParams.startYear || "Start year"}
              required={!searchParams.startYear}
              value={inputStartYear}
              onChange={(event) => setInputStartYear(event.target.value)}
              className="px-2 border border-red-400 rounded-md focus:outline-none focus:ring-2 focus:ring-red-400 bg-gray-300"
              style={{ minWidth: '110px' }}
              />
              <input
              name="endYear"
              type="number"
              min="1900"
              max={new Date().getFullYear()}
              placeholder={searchParams.endYear || "End year"}
              required={!searchParams.endYear}
              value={inputEndYear}
              onChange={(event) => setInputEndYear(event.target.value)}
              className="px-2 border border-red-400 rounded-md focus:outline-none focus:ring-2 focus:ring-red-400 bg-gray-300"
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
              value={inputMinMagnitude}
              onChange={(event) => setInputMinMagnitude(event.target.value)}
              className="flex-1 px-2 border border-red-400 rounded-md focus:outline-none focus:ring-2 focus:ring-red-400 bg-gray-300"
              style={{ minWidth: '150px' }}
              />
              <select
              name="orderby"
              className="flex-1 px-2 border border-red-400 rounded-md focus:outline-none focus:ring-2 focus:ring-red-400 bg-gray-300 mb-2 md:mb-0"
              value={inputOrderBy}
              onChange={(event) => setInputOrderBy(event.target.value)}
              >
              <option value="">Order by ...</option>
              <option value="time">Time (Newest)</option>
              <option value="time-asc">Time (Oldest)</option>
              <option value="magnitude">Magnitude (Highest)</option>
              <option value="magnitude-asc">Magnitude (Lowest)</option>
              </select>
              <FormSubmitButton
                  idleText="Search"
                  pendingText="Searching..."
              />
            </div>
        </form>
  );
}
