
import Cards from "@/components/cards";

async function fetchEarthquakeData() {
    const response = await fetch(
        'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&limit=12&orderby=time&minsig=600',
        { cache: 'no-store' }
    );
    if (!response.ok) {
        throw new Error('Failed to fetch earthquake data');
    }
    return await response.json();
}

export default async function Latest() {
    const data = await fetchEarthquakeData();
    const earthquakes = data.features || [];

    return (
        <main className="w-[min(1440px,100%-4rem)] mx-auto" style={{ padding: '2rem' }}>
            <h1 className="p-4 text-xl font-bold text-red-600 text-center">Latest (Significance &gt; 600)</h1>
            <p className="mb-6 text-gray-700 text-sm max-w-2xl mx-auto">
                <strong>What is a &quot;significant&quot; earthquake?</strong><br />
                <code>significance = max(magnitude, PAGER alert) + &#39;Did you feel it?&#39;</code><br />
            </p>
            <Cards earthquakes={earthquakes} />
        </main>
    );
}
