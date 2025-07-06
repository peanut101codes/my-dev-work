import SearchForm from "@/components/searchform";
import { getEarthquakes, getSearchParams } from "@/actions/search";
import Cards from "@/components/cards";
import MobileCards from "@/components/mobileCards";
import RevalidateButton from "@/components/revalidateButton";

export default async function Home() {
  const earthquakes = await getEarthquakes();
  const searchParams = await getSearchParams();

  return (
    <div
      className="bg-[url(/earthquake.jpg)] bg-contain bg-center bg-repeat"
      style={{ minHeight: '100vh' }}
    >
      <main className="w-[min(1440px,100%-4rem)] mx-auto" style={{ padding: '2rem' }}>
        <h1 className="text-4xl font-extrabold text-center text-red-600 drop-shadow-lg mb-8">
          Did you feel <span className="text-5xl text-black italic">It&nbsp;?</span>
        </h1>
        <div className="flex flex-col gap-2 lg:flex-row lg:justify-center lg:items-center mb-8">
          <SearchForm 
            searchParams={searchParams} 
            key={searchParams.startYear + searchParams.endYear + searchParams.minMagnitude + searchParams.orderBy} 
          />
          {(Array.isArray(earthquakes) && earthquakes.length > 0 
              || (searchParams.startYear !== '' || searchParams.endYear !== '' || searchParams.minMagnitude !== '' || searchParams.orderBy !== ''))
              && <RevalidateButton />
          }
        </div>
        {Array.isArray(earthquakes) && earthquakes.length > 0 ? (
          <>
            <div className="block md:hidden">
              <MobileCards earthquakes={earthquakes} key={new Date().toISOString()} />
            </div>
            <div className="hidden md:block">
              <Cards earthquakes={earthquakes} key={new Date().toISOString()} />
            </div>
          </>
        ) : earthquakes && Array.isArray(earthquakes) && earthquakes.length === 0 ? (
          <div className="text-center bg-gray-300 mt-8 text-xl">No data found. Try lower your min magnitude.</div>
        ) : null}
      </main>
    </div>
  );
}
