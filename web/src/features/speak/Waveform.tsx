import { useEffect, useRef } from "react";

/**
 * The amber thread (docs/plan/02): a level-meter that thickens and flares
 * with the voice. Bars scroll left as time passes.
 */
export function Waveform({ level }: { level: number }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const barsRef = useRef<number[]>([]);
  const levelRef = useRef(0);
  levelRef.current = level;

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const dpr = window.devicePixelRatio || 1;
    canvas.width = canvas.clientWidth * dpr;
    canvas.height = canvas.clientHeight * dpr;
    ctx.scale(dpr, dpr);

    let raf = 0;
    let lastSample = 0;
    const draw = (now: number) => {
      if (now - lastSample > 60) {
        barsRef.current.push(levelRef.current);
        const maxBars = Math.floor(canvas.clientWidth / 5);
        if (barsRef.current.length > maxBars) barsRef.current.shift();
        lastSample = now;
      }
      const w = canvas.clientWidth;
      const h = canvas.clientHeight;
      ctx.clearRect(0, 0, w, h);
      barsRef.current.forEach((v, i) => {
        const x = w - (barsRef.current.length - i) * 5;
        const barH = Math.max(2, v * h * 0.9);
        const glow = Math.min(1, 0.35 + v * 1.2);
        ctx.fillStyle = `rgba(232, 168, 73, ${glow})`;
        ctx.beginPath();
        ctx.roundRect(x, (h - barH) / 2, 3, barH, 2);
        ctx.fill();
      });
      raf = requestAnimationFrame(draw);
    };
    raf = requestAnimationFrame(draw);
    return () => cancelAnimationFrame(raf);
  }, []);

  return <canvas ref={canvasRef} className="h-24 w-full" aria-hidden />;
}
