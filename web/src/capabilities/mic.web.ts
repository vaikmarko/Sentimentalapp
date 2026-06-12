import type { MicCapability, MicRecording } from "./types";

/** Preferred recording formats in order; iOS Safari requires audio/mp4. */
const MIME_CANDIDATES = ["audio/webm;codecs=opus", "audio/webm", "audio/mp4"];

function pickMimeType(): string | undefined {
  if (typeof MediaRecorder === "undefined") return undefined;
  return MIME_CANDIDATES.find((m) => MediaRecorder.isTypeSupported(m));
}

export class WebMic implements MicCapability {
  private recorder: MediaRecorder | null = null;
  private chunks: Blob[] = [];
  private startedAt = 0;
  private levelTimer: number | null = null;
  private audioContext: AudioContext | null = null;
  private stream: MediaStream | null = null;

  async isAvailable(): Promise<boolean> {
    return (
      typeof MediaRecorder !== "undefined" &&
      !!navigator.mediaDevices?.getUserMedia &&
      pickMimeType() !== undefined
    );
  }

  async start(onLevel?: (level: number) => void): Promise<void> {
    this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mimeType = pickMimeType();
    this.recorder = new MediaRecorder(this.stream, mimeType ? { mimeType } : undefined);
    this.chunks = [];
    this.recorder.ondataavailable = (e) => {
      if (e.data.size > 0) this.chunks.push(e.data);
    };
    this.recorder.start(1000);
    this.startedAt = Date.now();

    if (onLevel) {
      this.audioContext = new AudioContext();
      const source = this.audioContext.createMediaStreamSource(this.stream);
      const analyser = this.audioContext.createAnalyser();
      analyser.fftSize = 256;
      source.connect(analyser);
      const data = new Uint8Array(analyser.frequencyBinCount);
      this.levelTimer = window.setInterval(() => {
        analyser.getByteTimeDomainData(data);
        let sum = 0;
        for (const v of data) sum += (v - 128) ** 2;
        onLevel(Math.min(1, Math.sqrt(sum / data.length) / 40));
      }, 50);
    }
  }

  async stop(): Promise<MicRecording> {
    const recorder = this.recorder;
    if (!recorder) throw new Error("Not recording");
    const stopped = new Promise<void>((resolve) => {
      recorder.onstop = () => resolve();
    });
    recorder.stop();
    await stopped;
    this.teardown();
    const mimeType = recorder.mimeType || "audio/webm";
    return {
      blob: new Blob(this.chunks, { type: mimeType }),
      mimeType,
      durationMs: Date.now() - this.startedAt,
    };
  }

  cancel(): void {
    this.recorder?.stop();
    this.teardown();
    this.chunks = [];
  }

  private teardown(): void {
    if (this.levelTimer !== null) window.clearInterval(this.levelTimer);
    this.levelTimer = null;
    void this.audioContext?.close();
    this.audioContext = null;
    this.stream?.getTracks().forEach((t) => t.stop());
    this.stream = null;
    this.recorder = null;
  }
}
