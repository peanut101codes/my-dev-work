import SearchForm from "@/components/searchform";
import { getEarthquakes } from "@/actions/search";
import Cards from "@/components/cards";

export default async function Home() {
  const earthquakes = await getEarthquakes();

  return (
    <div
      className="bg-[url(/earthquake.jpg)] bg-contain bg-center bg-repeat md:bg-no-repeat"
      style={{ minHeight: '100vh' }}
    >
      <main className="w-[min(1440px,100%-4rem)] mx-auto" style={{ padding: '2rem' }}>
        <h1 className="text-5xl font-extrabold text-center text-red-600 drop-shadow-lg mb-8">
          Did you feel <span className="text-6xl text-black italic">It&nbsp;?</span>
        </h1>
        <SearchForm />
        <Cards earthquakes={earthquakes} />
      </main>
    </div>
  );
}
