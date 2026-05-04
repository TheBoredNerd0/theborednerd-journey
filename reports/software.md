# 💻 DEV BRIEFING — May 5, 2026

🔥 **Trending in dev:**
Bun 2.0's native SQLite and key-value store are turning heads — devs are replacing entire Express + SQLite stacks with a single Bun process. Meanwhile, the **Web Components revival** is real: with frameworks getting heavier (looking at you, Next.js bundle), vanilla web components + signals are back as a lean alternative for micro-frontends.

📚 **Today's topic: Web Development — Signals & Reactive Primitives**

**What are Signals?**
Signals are reactive primitives — small, self-contained state containers that automatically track dependencies and update only what needs updating. Think of them as `useState` but without React. When a signal changes, anything that reads it re-computes automatically.

**Why it matters:**
- No virtual DOM diffing — surgical DOM updates only
- Framework-agnostic: Preact, Solid, Vue, Svelte, even vanilla JS all support signals
- Way smaller bundles than full React for interactive UIs
- Fine-grained reactivity = better performance by default

**Quick example (vanilla JS with @preact/signals):**
```js
import { signal, computed } from '@preact/signals'

const count = signal(0)
const doubled = computed(() => count.value * 2)

function render() {
  document.getElementById('app').innerText =
    `${count} × 2 = ${doubled}`
}

// Auto-updates when count changes — no manual subscriber lists
document.getElementById('btn').onclick = () => count.value++
```

**vs traditional approach:**
```js
// React — whole component re-runs on state change
function Counter() {
  const [count, setCount] = useState(0)
  return (
    <div>{count * 2}</div>
    <button onClick={() => setCount(c => c + 1)} />
  )
}
```

**Exercise for you:**
Pick a small vanilla JS page (a form, a list, a counter) and rewrite the state with `@preact/signals`. Compare the bundle size and re-render behaviour in DevTools.

**Resource:**
→ https://preactjs.com/guide/signals (free, Preact signals docs — works standalone)

---

🛠️ **Repo update:**
Git status clean — no stale TODOs or broken docs in workspace source files. All source-level comments are intentional. Pending commits across report files ready to be pushed. README and agent specs are current.

---

💡 **Project idea: "Signal Board" — Real-time collaborative dashboard for teams**

**What it does:** A shared dashboard where team members can drop reactive widgets (counters, timers, polls, Kanban columns) that update in real-time across all connected browsers via WebSockets. Think "team mood ring" meets project tracker.

**Why it's a great portfolio piece:**
- Full-stack: WebSocket server + reactive frontend + persistence layer
- Shows understanding of reactive programming (signals) + real-time sync
- Concrete use case hiring managers and indie teams will immediately get
- Easy to extend: auth, drag-and-drop, widget store

**Stack:** Bun + WebSockets (native) + Preact Signals + SQLite for persistence + vanilla CSS (no framework needed for MVP).

**Start with:** One HTML file with signals for a counter that updates in two browser tabs simultaneously using `BroadcastChannel` API — zero backend needed for the prototype.
