import { useEffect } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import { useAuth } from "../features/auth/AuthProvider";
import { SignIn } from "../features/auth/SignIn";
import { Privacy } from "../features/legal/Privacy";
import { SpeakScreen } from "../features/speak/SpeakScreen";
import { RevealScreen } from "../features/reveal/RevealScreen";
import { StoryScreen } from "../features/stories/StoryScreen";
import { track } from "../lib/analytics";
import { Shell } from "./Shell";
import { Tonight } from "./tabs/Tonight";
import { Chronicle } from "./tabs/Chronicle";
import { You } from "./tabs/You";

export function App() {
  const { user, loading } = useAuth();

  useEffect(() => {
    track("pageview");
  }, []);

  if (loading) {
    return (
      <main className="flex min-h-dvh items-center justify-center">
        <div className="breathe h-2 w-2 rounded-full bg-lamplight-500" aria-label="Loading" />
      </main>
    );
  }

  if (!user) {
    return (
      <Routes>
        <Route path="/privacy" element={<Privacy />} />
        <Route path="*" element={<SignIn />} />
      </Routes>
    );
  }

  return (
    <Routes>
      {/* Full-screen surfaces (no tab bar): the Booth, the Darkroom, the page */}
      <Route path="/speak" element={<SpeakScreen />} />
      <Route path="/entry/:entryId" element={<RevealScreen />} />
      <Route path="/story/:storyId" element={<StoryScreen />} />
      <Route path="/privacy" element={<Privacy />} />

      <Route element={<Shell />}>
        <Route path="/" element={<Tonight />} />
        <Route path="/chronicle" element={<Chronicle />} />
        <Route path="/you" element={<You />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
