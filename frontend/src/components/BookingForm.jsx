import { useMemo, useState } from "react";

import { bookDate } from "../services/api.js";

const EMAIL_REGEX = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

export default function BookingForm({ dateId }) {
  const [email, setEmail] = useState("");
  const [comments, setComments] = useState("");
  const [status, setStatus] = useState("idle");
  const [message, setMessage] = useState("");

  const isValidEmail = useMemo(() => EMAIL_REGEX.test(email), [email]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setStatus("loading");
    setMessage("");

    try {
      await bookDate({ email, comments, date_id: dateId });
      setStatus("success");
      setMessage("Booking confirmed. Check your email soon.");
      setEmail("");
      setComments("");
    } catch (error) {
      setStatus("error");
      setMessage("Booking failed. Please try again.");
    }
  };

  return (
    <form className="grid gap-4" onSubmit={handleSubmit}>
      <div className="grid gap-2">
        <label className="text-sm font-semibold text-[#4b2f2f]" htmlFor="email">
          Email
        </label>
        <input
          id="email"
          type="email"
          required
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          placeholder="you@gmail.com"
          className="w-full rounded-2xl border border-[#f2c5d1] bg-white px-4 py-3 text-sm focus:border-[#f38ba7] focus:outline-none"
        />
      </div>

      <div className="grid gap-2">
        <label className="text-sm font-semibold text-[#4b2f2f]" htmlFor="comments">
          Comments (optional)
        </label>
        <textarea
          id="comments"
          rows="3"
          value={comments}
          onChange={(event) => setComments(event.target.value)}
          placeholder="Add anything you want me to know"
          className="w-full resize-none rounded-2xl border border-[#f2c5d1] bg-white px-4 py-3 text-sm focus:border-[#f38ba7] focus:outline-none"
        />
      </div>

      <button
        type="submit"
        disabled={!isValidEmail || status === "loading"}
        className="mt-2 inline-flex items-center justify-center rounded-full bg-[#f38ba7] px-5 py-3 text-sm font-semibold text-white transition hover:bg-[#e66b8a] disabled:cursor-not-allowed disabled:opacity-60"
      >
        {status === "loading" ? "Scheduling..." : "Schedule date"}
      </button>

      {message && (
        <div
          className={`rounded-2xl px-4 py-3 text-sm ${
            status === "success"
              ? "bg-[#fbeef1] text-[#2f1b1b]"
              : "bg-[#fff1f3] text-[#7a2f3a]"
          }`}
        >
          {message}
        </div>
      )}
    </form>
  );
}
