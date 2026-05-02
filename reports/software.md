# 💻 DEV BRIEFING — 2026-05-03

## 🔥 Trending in Dev
React 19 is now stable with Server Components baked in by default — full-stack React is the new norm, not the exception. Meanwhile, Bun has hit 2.0 with native Jest replacement and a bundler that rivals esbuild in speed. The shift toward unified JS runtimes (Bun/Node/Deno) outside the browser is accelerating fast.

## 📚 Today's Topic: Web Development — React Server Components & API Patterns

**Server Components** change how you think about data fetching. Instead of `useEffect` + loading spinners, you `await` data directly in components:

```jsx
// app/users/page.jsx (Next.js App Router)
async function UsersPage() {
  const users = await db.query('SELECT * FROM users LIMIT 20');
  return <UserList users={users} />;
}
```

No client-side fetch, no loading state — the component itself is async. Combined with React's `use()` hook for streaming Suspense boundaries, you get progressive HTML without the complexity.

**Key patterns to know:**
- `use client` directive = interactive, runs in browser
- Default (no directive) = server component, runs at build/request time
- Mix both in one file by separating into `.client.js` and `.server.js`
- Streaming: wrap slow sections in `<Suspense fallback={<Spinner />}>` and the page paints immediately

**Quick exercise:** Take any existing React `useEffect(() => { fetch('/api/data')... }, [])` pattern and convert it to a server component with `await`. Compare the code reduction.

**Resources:**
- [React 19 Beta Docs — Server Components](https://react.dev/blog/category/react-19)
- [Next.js App Router Guide](https://nextjs.org/docs/app)

---

## 🛠️ Repo Update
**Staged reports need committing.** 6 modified report files sitting unstaged:
- `reports/business.md`
- `reports/content.md`
- `reports/cyber.md`
- `reports/law.md`
- `reports/music.md`
- `reports/software.md` ← (this file, refreshed now)

No broken docs, no stale TODOs in workspace source files (only `node_modules/` noise). All clean beyond the pending commit above.

---

## 💡 Project Idea: API Proxy + Rate Limiter Dashboard

**What it does:** A self-hosted dashboard where you add your API keys (OpenAI, Pexels, etc.), and it routes requests through your proxy — logging usage, enforcing rate limits per key, and showing cost analytics.

**Why it's a strong portfolio piece:**
- Proves you understand middleware, auth, and observability
- Solves a real pain point for developers managing multiple API keys
- Has clear extensibility (add new API adapters, alerting thresholds)
- Tech stack: Express + React dashboard + simple SQLite + rate-limiter middleware

**Weekend scope:** A single Express server with one proxy endpoint per API, in-memory rate limiting, and a React dashboard showing a usage table. MVP in ~8 hours of focused work.
