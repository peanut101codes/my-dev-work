import { notFound } from "next/navigation";
import Link from "next/link";

interface EarthquakeDetail {
    id: string;
    title: string;
    magnitude: number;
    significance: number;
    location: string;
    longitude: number;
    latitude: number;
    time: string;
    alert: string;
    tsunami: number;
    felt: number | null;
    /* eslint-disable @typescript-eslint/no-explicit-any */
    [key: string]: any;
}

async function fetchEarthquakeDetail(id: string): Promise<EarthquakeDetail | null> {
    try {
        const res = await fetch(`https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=${id}&format=geojson`);
        if (!res.ok) return null;
        return await res.json();
    } catch {
        return null;
    }
}

export default async function EarthquakeDetailPage({ params }: { params: Promise<{ id: string }> }) {
    const { id } = await params;
    const detail = await fetchEarthquakeDetail(id);

    if (!detail) return notFound();

    return (
        <main className="w-[min(960px,100%-4rem)] mx-auto" style={{ padding: '2rem' }}>                        
            <h1 className="pt-8 pb-8 text-xl font-bold text-red-600">{detail.properties.title}</h1>
            <ul className="space-y-4">
                <li><strong>ID:</strong> {detail?.id}</li>
                <li><strong>Magnitude:</strong> {detail.properties.mag}</li>
                <li><strong>Significance:</strong> {detail.properties.sig}</li>
                <li><strong>Location:</strong> {detail.properties.place}</li>
                <li>
                    <strong>Latitude:</strong>{" "}
                    {detail.geometry?.coordinates?.[1] ??
                        detail.properties?.latitude ??
                        detail.properties?.products?.dyfi?.[0]?.properties?.latitude ??
                        detail.properties?.products?.groundFailure?.[0]?.properties?.latitude ??
                        "N/A"}
                </li>
                <li>
                    <strong>Longitude:</strong>{" "}
                    {detail.geometry?.coordinates?.[0] ??
                        detail.properties?.longitude ??
                        detail.properties?.products?.dyfi?.[0]?.properties?.longitude ??
                        detail.properties?.products?.groundFailure?.[0]?.properties?.longitude ??
                        "N/A"}
                </li>
                <li><strong>Tsunami:</strong> {detail.properties.tsunami == 0 ? "No" : "Yes"}</li>
                <li><strong>Felt:</strong> {detail.properties.felt}</li>
                <li><strong>Alert:</strong> {detail.properties.alert}</li>
                <li><strong>Time:</strong> {new Date(detail.properties.time).toLocaleString()}</li>
            </ul>
            <Link
                href={"/"}
                className="text-blue-600 hover:underline mt-8 inline-block"
            >
                Search Other Earthquakes
            </Link>
        </main>
    );
}
