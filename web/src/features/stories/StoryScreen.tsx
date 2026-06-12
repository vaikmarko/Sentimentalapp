import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api, type Story } from "../../lib/api";
import { StoryCard } from "./StoryCard";

export function StoryScreen() {
  const { storyId } = useParams<{ storyId: string }>();
  const navigate = useNavigate();
  const [story, setStory] = useState<Story | null>(null);
  const [missing, setMissing] = useState(false);

  useEffect(() => {
    if (!storyId) return;
    api
      .story(storyId)
      .then(setStory)
      .catch(() => setMissing(true));
  }, [storyId]);

  return (
    <main className="mx-auto min-h-dvh max-w-md px-5 pb-12 pt-6">
      <button
        onClick={() => navigate(-1)}
        className="mb-4 p-2 text-ink-500 hover:text-ink-300"
        aria-label="Back"
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
          <path d="M19 12H5M12 19l-7-7 7-7" />
        </svg>
      </button>

      {missing ? (
        <p className="px-3 font-prose text-lg text-ink-300">This page is missing from the shelf.</p>
      ) : story ? (
        <StoryCard story={story} />
      ) : (
        <div className="flex min-h-[40dvh] items-center justify-center">
          <div className="breathe h-2 w-2 rounded-full bg-lamplight-500" aria-label="Loading" />
        </div>
      )}
    </main>
  );
}
