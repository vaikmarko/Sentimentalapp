/**
 * Capability interfaces — the contract between the app and the platform.
 *
 * Web implementations live alongside; Capacitor implementations are added in
 * Phase B behind the same interfaces (see docs/plan/00 and 03). Feature code
 * must depend on these types only, never on platform APIs directly.
 */

export interface MicRecording {
  blob: Blob;
  mimeType: string;
  durationMs: number;
}

export interface MicCapability {
  /** Whether recording is possible on this platform/browser. */
  isAvailable(): Promise<boolean>;
  /** Request permission and start recording. */
  start(onLevel?: (level: number) => void): Promise<void>;
  /** Stop and return the finished recording. */
  stop(): Promise<MicRecording>;
  /** Abort without returning a recording. */
  cancel(): void;
}

export interface PushCapability {
  isAvailable(): Promise<boolean>;
  requestPermission(): Promise<"granted" | "denied" | "default">;
}

export interface SharePayload {
  title?: string;
  text?: string;
  url: string;
}

export interface ShareCapability {
  isAvailable(): boolean;
  share(payload: SharePayload): Promise<boolean>;
}

export interface HapticsCapability {
  /** A short confirmation tap (e.g. on reveal). No-op where unsupported. */
  tap(): void;
}

export interface Capabilities {
  mic: MicCapability;
  push: PushCapability;
  share: ShareCapability;
  haptics: HapticsCapability;
}
