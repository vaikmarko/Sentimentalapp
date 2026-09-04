import type { ReactNode } from "react";
import { Link } from "react-router-dom";

/** Contact for privacy requests. Change here and it updates everywhere on the page. */
export const PRIVACY_CONTACT = "hello@sentimentalapp.com";
const LAST_UPDATED = "4 September 2026";

function H2({ children }: { children: string }) {
  return <h2 className="mt-10 font-prose text-xl font-light text-ink-100">{children}</h2>;
}

function P({ children }: { children: ReactNode }) {
  return <p className="mt-3 text-[15px] leading-relaxed text-ink-300">{children}</p>;
}

export function Privacy() {
  return (
    <main className="mx-auto min-h-dvh max-w-md px-6 pb-16 pt-8">
      <Link to="/" className="text-sm text-ink-500 underline-offset-4 hover:text-ink-300 hover:underline">
        ← Back
      </Link>

      <p className="mt-10 text-xs font-medium uppercase tracking-[0.2em] text-ink-500">Privacy</p>
      <h1 className="mt-4 font-prose text-3xl font-light leading-snug text-ink-100">
        Your reflections are yours.
      </h1>
      <P>
        This page says plainly what Sentimental collects, why, who processes it, and how
        you delete it. Last updated {LAST_UPDATED}.
      </P>

      <H2>Who is responsible</H2>
      <P>
        Sentimental (sentimentalapp.com) is the data controller. For anything about your
        data, write to{" "}
        <a href={`mailto:${PRIVACY_CONTACT}`} className="text-lamplight-400">
          {PRIVACY_CONTACT}
        </a>
        .
      </P>

      <H2>What we collect</H2>
      <P>
        <strong className="font-medium text-ink-100">Account.</strong> When you sign in with
        Google we receive your name, email address and a Google user ID. We use them to
        keep your stories yours and to show your name in the app.
      </P>
      <P>
        <strong className="font-medium text-ink-100">What you tell us.</strong> Your voice
        recordings, the text you type instead, the transcripts made from recordings, and
        the stories written from them, including their tone, themes and the people you
        named. This is the whole point of the product, and it is private to you.
      </P>
      <P>
        <strong className="font-medium text-ink-100">Technical.</strong> Standard server
        request logs (IP address, timestamps, errors), kept for security and debugging.
      </P>
      <P>
        <strong className="font-medium text-ink-100">Usage.</strong> We count a handful of
        anonymous events — app opened, recording started, story revealed, story kept — using
        Plausible, which is cookieless and stores no personal identifiers. That is why
        there is no cookie banner.
      </P>

      <H2>What we do with it</H2>
      <P>
        Only what is needed to turn what you said into a story and show it back to you.
        We do not sell your data, do not show it to other users, and do not use it to
        advertise. Nothing leaves the vault unless you yourself choose to publish it —
        and today there is no publish button.
      </P>
      <P>
        Each transcript is also screened automatically for signs that you may be in
        crisis, so we can show a helpline. Only a yes/no flag is stored; it is never
        shared.
      </P>

      <H2>Who processes it for us</H2>
      <P>
        <strong className="font-medium text-ink-100">Google Cloud / Firebase</strong> —
        sign-in, database, file storage and servers, in the EU region (Belgium). Google
        sign-in itself may process data globally under Google's terms.
      </P>
      <P>
        <strong className="font-medium text-ink-100">OpenAI</strong> — your recording is
        transcribed and the transcript is turned into a story by OpenAI's API. Under
        OpenAI's API terms this data is not used to train their models and is deleted
        within 30 days.
      </P>
      <P>
        <strong className="font-medium text-ink-100">Plausible Analytics</strong> — the
        anonymous usage counts above, hosted in the EU.
      </P>

      <H2>Legal basis</H2>
      <P>
        Providing the service you asked for (contract), keeping it secure and understanding
        whether it works in aggregate (legitimate interest), and your explicit permission
        for the microphone (consent, which you can withdraw in your browser at any time).
      </P>

      <H2>How long we keep it</H2>
      <P>
        Until you delete it. Deleting your account removes your recordings, transcripts,
        stories and sign-in record right away; copies in backups and logs are gone within
        30 days.
      </P>

      <H2>Your rights</H2>
      <P>
        You can see, correct, export or erase your data, and object to how it is used.
        Deletion is a button in the app under <em>You</em>. For everything else, write to{" "}
        <a href={`mailto:${PRIVACY_CONTACT}`} className="text-lamplight-400">
          {PRIVACY_CONTACT}
        </a>{" "}
        and we will answer within a month. If you feel we got it wrong, you may complain
        to the Estonian Data Protection Inspectorate (Andmekaitse Inspektsioon) or your
        local authority.
      </P>

      <H2>Age</H2>
      <P>Sentimental is not meant for people under 16.</P>

      <H2>Changes</H2>
      <P>
        If this page changes in a way that matters, we will say so in the app before it
        takes effect.
      </P>
    </main>
  );
}
