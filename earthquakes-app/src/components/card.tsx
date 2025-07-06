import React from "react";
import Link from "next/link";

export type Earthquake = {
    id: string;
    properties: {
        place: string;
        mag: number;
        time: number;
    };
};


export default function Card({ eq }: { eq: Earthquake }) {
    if (!eq || !eq.properties) {
        return null;
    }
    return (
        <div
            className="border border-gray-300 rounded-lg p-4 w-[270px] md:w-[320px] bg-gray-50 shadow-lg hover:shadow-2xl transition-shadow duration-200 flex flex-col gap-2"
            style={{
                boxShadow:
                    "0 4px 16px rgba(0,0,0,0.10), 0 1.5px 6px rgba(0,0,0,0.08)",
            }}
        >
            <h2 className="text-lg font-semibold mb-2">{eq.properties.place}</h2>
            <p>
                <span className="font-medium">Magnitude:</span> {eq.properties.mag}
            </p>
            <p>
                <span className="font-medium">Time UTC:</span>{" "}
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
    );
}