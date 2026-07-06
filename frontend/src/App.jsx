import { useState } from "react";

const API_URL = "http://localhost:5245/api/search"; //just for the moment

function SearchBar({ onSearch, isLoading }) {
  const [query, setQuery] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) onSearch(query);
  };

  return (
    //flexible row, small space between input bow and button, makes the search bar strech to 100%, a stopper on how wide it can get
    <form onSubmit={handleSubmit} className="flex gap-2 w-full max-w-2xl">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="e.g. sword wielding hero with a tragic past..."
        //dynamic resize, adds padding, rounds sharp corners
        className="flex-1 px-4 py-3 rounded-lg bg-zinc-800 border border-zinc-700 text-white placeholder-zinc-500 focus:outline-none focus:border-indigo-500 transition-colors"
      />
      <button
        type="submit"
        disabled={isLoading}
        className="px-6 py-3 bg-indigo-600 hover:bg-indigo-500 disabled:bg-zinc-700 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-colors"
      >
        {isLoading ? "Searching..." : "Search"}
      </button>
    </form>
  );
}

function AnimeCard({ anime }) {
  // convert 0-1 cosine similarity score to a readable percentage
  const matchPercent = Math.round(anime.score * 100);

  return (
    <div className="bg-zinc-800 border border-zinc-700 rounded-xl p-5 flex flex-col gap-3 hover:border-indigo-500 transition-colors">
      <div className="flex items-start justify-between gap-4">
        <h2 className="text-white font-bold text-lg leading-tight">
          {anime.title}
        </h2>
        <span className="shrink-0 text-sm font-semibold px-2 py-1 rounded-full bg-indigo-900 text-indigo-300">
          {matchPercent}% match
        </span>
      </div>

      <div className="flex flex-wrap gap-2">
        {anime.genres.map((genre) => (
          <span
            key={genre}
            className="text-xs px-2 py-1 rounded-full bg-zinc-700 text-zinc-300"
          >
            {genre}
          </span>
        ))}
      </div>

      <p className="text-zinc-400 text-sm leading-relaxed line-clamp-3">
        {anime.synopsis}
      </p>
    </div>
  );
}

export default function App() {
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (query) => {
    setIsLoading(true);
    setError(null);
    setHasSearched(true);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) throw new Error(`API error: ${response.status}`);

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError("Something went wrong. Make sure the API is running.");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-zinc-900 text-white">
      <div className="max-w-3xl mx-auto px-4 py-16 flex flex-col items-center gap-8">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-4xl font-bold text-white mb-2">Anime Search</h1>
          <p className="text-zinc-400">
            Search by meaning, not keywords. Try{" "}
            <span className="text-indigo-400 italic">
              "a slow-burn romance set in feudal Japan"
            </span>
          </p>
        </div>

        {/* Search bar */}
        <SearchBar onSearch={handleSearch} isLoading={isLoading} />

        {/* Results */}
        {isLoading && (
          <p className="text-zinc-500 animate-pulse">Finding matches...</p>
        )}

        {error && <p className="text-red-400">{error}</p>}

        {!isLoading && hasSearched && results.length === 0 && !error && (
          <p className="text-zinc-500">No results found.</p>
        )}

        {!isLoading && results.length > 0 && (
          <div className="w-full flex flex-col gap-4">
            <p className="text-zinc-500 text-sm">{results.length} results</p>
            {results.map((anime) => (
              <AnimeCard key={anime.title} anime={anime} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
