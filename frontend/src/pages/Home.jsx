import { useEffect, useState } from "react";

import DateCard from "../components/DateCard.jsx";
import DateModal from "../components/DateModal.jsx";
import { fetchDates } from "../services/api.js";

const DEFAULT_ERROR = "Unable to load dates right now.";

export default function Home() {
  const [dates, setDates] = useState([]);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let isMounted = true;
    fetchDates()
      .then((data) => {
        if (isMounted) {
          setDates(data);
          setLoading(false);
        }
      })
      .catch(() => {
        if (isMounted) {
          setError(DEFAULT_ERROR);
          setLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <main className="mx-auto flex max-w-6xl flex-col gap-10 px-6 pb-16 pt-14">
      <header className="flex flex-col gap-4">
        <p className="text-sm uppercase tracking-[0.4em] text-[#c66e84]">
          Catalogo de experiencias
        </p>
        <h1 className="text-4xl font-semibold md:text-5xl">
          Escoge la cita que quieres vivir
        </h1>
        <p className="max-w-2xl text-base text-[#4b2f2f] md:text-lg">
          Cada plan tiene su propio ritual. Explora los retos y reserva tu cita en
          segundos.
        </p>
      </header>

      {loading && (
        <div className="rounded-2xl bg-white/70 p-8 text-center shadow-soft">
          Loading dates...
        </div>
      )}

      {!loading && error && (
        <div className="rounded-2xl bg-white/70 p-8 text-center shadow-soft">
          {error}
        </div>
      )}

      {!loading && !error && (
        <section className="grid gap-6 md:grid-cols-2">
          {dates.map((date) => (
            <DateCard key={date.id} data={date} onSelect={() => setSelected(date)} />
          ))}
        </section>
      )}

      {selected && (
        <DateModal data={selected} onClose={() => setSelected(null)} />
      )}
    </main>
  );
}
