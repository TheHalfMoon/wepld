// Modified by WePLD on 2026-08-23: deterministic Pictorial rebrand/path integration from the pinned upstream source.
// Reference output for agent/human review — not executed by tests.
// After the append-string CSP patch is applied, nuxt.config.ts should look
// like this.

// Dev-only allowance so pictorial live mode can load. Empty string in any
// non-development environment.
const __pictorialLiveDev =
  process.env.NODE_ENV === 'development' ? ' http://localhost:8400' : '';

export default defineNuxtConfig({
  compatibilityDate: '2025-01-01',
  devtools: { enabled: true },
  routeRules: {
    '/**': {
      headers: {
        'Content-Security-Policy':
          "default-src 'self'; " +
          `script-src 'self' 'unsafe-inline' 'unsafe-eval'${__pictorialLiveDev}; ` +
          "style-src 'self' 'unsafe-inline'; " +
          "img-src 'self' data: blob:; " +
          `connect-src 'self'${__pictorialLiveDev}; ` +
          "frame-ancestors 'self';",
        'X-Frame-Options': 'SAMEORIGIN',
      },
    },
  },
});
