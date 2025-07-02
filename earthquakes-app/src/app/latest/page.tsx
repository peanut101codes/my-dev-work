
import Cards from "@/components/cards";

async function fetchEarthquakeData() {
    try {
        const response = await fetch(
            'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&limit=12&orderby=time&minsig=600'
        );
        if (!response.ok) {
            throw new Error('Failed to fetch earthquake data');
        }
        return await response.json();
    } catch (error) {
        return { error: error };
    }
}

export default async function Latest() {
    const data = await fetchEarthquakeData();
    if(data.error) {
        return (
            <div className="flex items-center justify-center h-64">
                <p className="text-yellow-600">Error fetching data: {data.error.message}</p>
            </div>
        ); 
    }
    const earthquakes = data.features || [];

    return (
        <main className="w-[min(1440px,100%-4rem)] mx-auto" style={{ padding: '2rem' }}>
            <h1 className="p-4 text-xl font-bold text-center">Latest (Significance &gt; 600)</h1>
            <p className="mb-6 text-gray-700 text-sm max-w-2xl mx-auto">
                <strong>What is a &quot;significant&quot; earthquake?</strong><br />
                <code>significance = max(magnitude, PAGER alert) + &#39;Did you feel it?&#39;</code><br />
            </p>
            <Cards earthquakes={earthquakes} />
        </main>
    );
}
