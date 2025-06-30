import SearchForm from "@/components/searchform";
import { getEarthquakes, getSearchParams } from "@/actions/search";
import Cards from "@/components/cards";

export default async function Home() {
  const earthquakes = await getEarthquakes();
  const searchParams = await getSearchParams();

  return (
    <div
      className="bg-[url(/earthquake.jpg)] bg-contain bg-center bg-repeat"
      style={{ minHeight: '100vh' }}
    >
      <main className="w-[min(1440px,100%-4rem)] mx-auto" style={{ padding: '2rem' }}>
        <h1 className="text-5xl font-extrabold text-center text-red-600 drop-shadow-lg mb-8">
          Did you feel <span className="text-6xl text-black italic">It&nbsp;?</span>
        </h1>
        <SearchForm 
          searchParams={searchParams} 
          key={searchParams.startYear + searchParams.endYear + searchParams.minMagnitude + searchParams.orderBy} 
        />
        {Array.isArray(earthquakes) && earthquakes.length > 0 ? (
          <Cards
            earthquakes={earthquakes}
            key={new Date().toISOString()}
          />
        ) : earthquakes && Array.isArray(earthquakes) && earthquakes.length === 0 ? (
          <div className="text-center text-gray-800 mt-8 text-xl">No data found</div>
        ) : null}
      </main>
    </div>
  );
}
