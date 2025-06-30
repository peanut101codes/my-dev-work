
'use client';
import { useEffect, useState } from 'react';
import BasicPagination from './pagination';
import Link from "next/link";

type Earthquake = {
    id: string;
    properties: {
        place: string;
        mag: number;
        sig: number;
        time: number;
    };
};

type CardsProps = {
    earthquakes: Earthquake[] | null;
};

const CARDS_PER_PAGE = 12;

export default function Cards({ earthquakes}: CardsProps) {
    const [page, setPage] = useState(1);
    const [earthQuakesLocal, setEarthQuakesLocal] = useState<Earthquake[] | null>(earthquakes);

   useEffect(() => {
       const startIndex = (page - 1) * CARDS_PER_PAGE;
       const endIndex = startIndex + CARDS_PER_PAGE;
       setEarthQuakesLocal(earthquakes?.slice(startIndex, endIndex) || null);
   }, [page, earthquakes]);

    return (
        <div className='flex flex-col gap-y-8 items-center justify-center'>
            <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 justify-items-center">
                {earthQuakesLocal?.map((eq) => (
                    <div
                        key={eq.id}
                        className="border border-gray-300 rounded-lg p-4 w-[280px] xl:w-[310px] bg-gray-50 shadow-lg hover:shadow-2xl transition-shadow duration-200 flex flex-col gap-2"
                        style={{ boxShadow: '0 4px 16px rgba(0,0,0,0.10), 0 1.5px 6px rgba(0,0,0,0.08)' }}
                    >
                        <h2 className="text-lg font-semibold mb-2">{eq.properties.place}</h2>
                        <p>
                            <span className="font-medium">Magnitude:</span> {eq.properties.mag}
                        </p>
                        <p>
                            <span className="font-medium">Time:</span>{' '}
                            {new Date(eq.properties.time).toLocaleString()}
                        </p>
                        <Link
                            href={`/details/${eq.id}`}
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:underline mt-2"
                        >
                            Details
                        </Link>
                    </div>
                ))}
            </div>
            <BasicPagination
                cardsPerPage={12}
                totalCards={earthquakes?.length || 0}
                page={page}
                setPage={setPage}
            />
        </div>
    );
}
