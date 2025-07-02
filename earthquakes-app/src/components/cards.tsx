
'use client';
import { useEffect, useState } from 'react';
import BasicPagination from './pagination';
import Card from './card';
import { Earthquake } from './card'

export type CardsProps = {
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
                    <Card key={eq.id} eq={eq} />
                ))}
            </div>
            <BasicPagination
                cardsPerPage={CARDS_PER_PAGE}
                totalCards={earthquakes?.length || 0}
                page={page}
                setPage={setPage}
            />
        </div>
    );
}
