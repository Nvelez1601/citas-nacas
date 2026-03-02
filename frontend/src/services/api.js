const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function fetchDates() {
  const response = await fetch(`${API_BASE}/api/dates`);
  if (!response.ok) {
    throw new Error("Failed to load dates");
  }
  return response.json();
}

export async function bookDate(payload) {
  const response = await fetch(`${API_BASE}/api/book`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error("Booking failed");
  }

  return response.json();
}
