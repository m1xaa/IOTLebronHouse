(window as any).global = window;

// Optional, but often prevents follow-up crashes
(window as any).process = (window as any).process ?? { env: {} };
