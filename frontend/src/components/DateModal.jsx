import BookingForm from "./BookingForm.jsx";

export default function DateModal({ data, onClose }) {
  return (
    <div className="fixed inset-0 z-20 flex items-center justify-center bg-black/40 px-3 py-6 sm:px-4 sm:py-8">
      <div className="relative flex max-h-[90vh] w-full max-w-2xl flex-col overflow-y-auto rounded-3xl bg-white p-5 shadow-soft sm:p-6">
        <button
          onClick={onClose}
          aria-label="Close"
          className="absolute right-4 top-4 inline-flex h-8 w-8 items-center justify-center rounded-full border border-[#f2c5d1] text-sm text-[#c66e84] hover:bg-[#fdf2f5]"
        >
          ×
        </button>
        <div className="mb-6 mt-2 sm:mt-0">
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
        <div className="mt-6 border-t border-[#f2c5d1] pt-5 sm:mt-8 sm:pt-6">
          <BookingForm dateId={data.id} />
        </div>
      </div>
    </div>
  );
}
