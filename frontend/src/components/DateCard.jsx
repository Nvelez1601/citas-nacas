import {
  BoltIcon,
  CalendarIcon,
  CameraIcon,
  ChatBubbleLeftRightIcon,
  HeartIcon,
  RocketLaunchIcon,
  SunIcon,
  TrophyIcon
} from "@heroicons/react/24/outline";

const iconById = {
  1: TrophyIcon,
  2: BoltIcon,
  3: HeartIcon,
  4: CameraIcon,
  5: ChatBubbleLeftRightIcon,
  6: SunIcon,
  7: RocketLaunchIcon
};

export default function DateCard({ data, onSelect }) {
  const ActivityIcon = iconById[data.id] || TrophyIcon;

  return (
    <article className="group relative overflow-hidden rounded-3xl bg-white/80 p-6 shadow-soft transition duration-300 hover:-translate-y-1 hover:shadow-xl">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-[#c66e84]">
            {data.dress_code}
          </p>
          <h2 className="mt-2 text-2xl font-semibold text-[#2f1b1b]">
            {data.name}
          </h2>
        </div>
        <ActivityIcon className="h-8 w-8 text-[#f38ba7]" />
      </div>

      <div className="mt-6 flex items-center gap-2 text-sm text-[#4b2f2f]">
        <CalendarIcon className="h-5 w-5" />
        <span>{data.date}</span>
      </div>

      <div className="mt-6 max-h-0 overflow-hidden text-sm text-[#4b2f2f] transition-all duration-300 group-hover:max-h-40">
        <p className="mb-3 font-semibold">Description</p>
        <p className="mb-4 line-clamp-3">{data.description}</p>
        <p className="mb-2 font-semibold">Challenge</p>
        <p className="line-clamp-3">{data.challenge}</p>
      </div>

      <button
        onClick={onSelect}
        className="mt-6 inline-flex w-full items-center justify-center rounded-full bg-[#f38ba7] px-4 py-2 text-sm font-semibold text-white transition hover:bg-[#e66b8a]"
      >
        View details
      </button>
    </article>
  );
}
