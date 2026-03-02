import BookingForm from "./BookingForm.jsx";

export default function DateModal({ data, onClose }) {
  return (
    <div className="fixed inset-0 z-20 flex items-center justify-center bg-black/40 px-4 py-8">
      <div className="relative w-full max-w-2xl rounded-3xl bg-white p-6 shadow-soft">
        <button
          onClick={onClose}
          className="absolute right-4 top-4 rounded-full border border-[#f2c5d1] px-3 py-1 text-xs uppercase tracking-[0.2em] text-[#c66e84]"
        >
          Close
        </button>
        <div className="mb-6">
          <p className="text-xs uppercase tracking-[0.3em] text-[#c66e84]">
            {data.dress_code}
          </p>
          <h2 className="mt-2 text-3xl font-semibold text-[#2f1b1b]">
            {data.name}
          </h2>
          <p className="mt-2 text-sm text-[#4b2f2f]">{data.date}</p>
        </div>
        <div className="grid gap-4 text-sm text-[#4b2f2f]">
          <div>
            <p className="font-semibold">Description</p>
            <p>{data.description}</p>
          </div>
          <div>
            <p className="font-semibold">Challenge</p>
            <p>{data.challenge}</p>
          </div>
        </div>
        <div className="mt-8 border-t border-[#f2c5d1] pt-6">
          <BookingForm dateId={data.id} />
        </div>
      </div>
    </div>
  );
}
