import { Navigate, Route, Routes } from "react-router-dom";
import { useAuth } from "../features/auth/AuthProvider";
import { SignIn } from "../features/auth/SignIn";
import { Shell } from "./Shell";
import { Tonight } from "./tabs/Tonight";
import { Chronicle } from "./tabs/Chronicle";
import { Create } from "./tabs/Create";
import { Resonance } from "./tabs/Resonance";
import { You } from "./tabs/You";

export function App() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <main className="flex min-h-dvh items-center justify-center">
        <div className="breathe h-2 w-2 rounded-full bg-lamplight-500" aria-label="Loading" />
      </main>
    );
  }

  if (!user) return <SignIn />;

  return (
    <Routes>
      <Route element={<Shell />}>
        <Route path="/" element={<Tonight />} />
        <Route path="/chronicle" element={<Chronicle />} />
        <Route path="/create" element={<Create />} />
        <Route path="/resonance" element={<Resonance />} />
        <Route path="/you" element={<You />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
