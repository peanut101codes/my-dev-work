'use server';

import { revalidatePath } from "next/cache";

type Earthquake = {
    id: string;
    properties: {
        place: string;
        mag: number;
        sig: number;
        time: number;
    };
};

let earthquakes: Earthquake[] | null = null;
let selectedParams: { startYear: string; endYear: string; minMagnitude: string; orderBy: string } = {
    startYear: '',
    endYear: '',
    minMagnitude: '',
    orderBy: ''
};

export const getEarthquakes = async (): Promise<Earthquake[] | null> => {
  await new Promise((resolve) => setTimeout(resolve, 250));
  return Promise.resolve(earthquakes);
};

export const clearEarthquakes = async (): Promise<void> => {
    earthquakes = null;
    selectedParams = { startYear: '', endYear: '', minMagnitude: '', orderBy: '' };
    revalidatePath('/');
}

export const getSearchParams = async (): Promise<{ startYear: string; endYear: string; minMagnitude: string; orderBy: string }> => {
    return Promise.resolve(selectedParams);
}

export async function searchEarthquakes(formData: FormData): Promise<void | { error: unknown }> {
    const startYear = formData.get('startYear') as string;
    const endYear = formData.get('endYear') as string;
    const minMagnitude = formData.get('minMagnitude') as string;
    const orderBy = formData.get('orderby') as string || 'time-asc';
    selectedParams = { startYear, endYear, minMagnitude, orderBy };

    const baseUrl = 'https://earthquake.usgs.gov/fdsnws/event/1/query';
    const params = new URLSearchParams({ format: 'geojson', limit: '84' });

    if (startYear && String(startYear).trim() !== '') {
        params.append('starttime', `${startYear}-01-01`);
    }
    if (endYear && String(endYear).trim() !== '') {
        params.append('endtime', `${endYear}-12-31`);
    }
    if (minMagnitude && String(minMagnitude).trim() !== '') {
        params.append('minmagnitude', minMagnitude);
    }
    if (orderBy && String(orderBy).trim() !== '') {
        params.append('orderby', orderBy);
    }

    const url = `${baseUrl}?${params.toString()}`;

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Failed to search earthquake data');
        }
        const data = await response.json();
        const earthquakesData = data.features || [];
        earthquakes = [];
        /* eslint-disable @typescript-eslint/no-explicit-any */
        earthquakesData.forEach((feature: any) => {
            const earthquake: Earthquake = {
                id: feature.id,
                properties: {
                    place: feature.properties.place,
                    mag: feature.properties.mag,
                    sig: feature.properties.sig,
                    time: feature.properties.time,
                },
            };
            if (!earthquakes?.some(eq => eq.id === earthquake.id)) {
                earthquakes?.push(earthquake);
            }
        });
    } catch (error) {
        return { error: error };
    }
    revalidatePath('/');
} 
