"""Static public UI shell for CivicBoards v0.1.1."""

from __future__ import annotations


def render_public_lookup_page() -> str:
    """Render the public-facing CivicBoards sample page."""

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CivicBoards Board and Commission Support</title>
<style>
  :root { --ink:#17202a; --muted:#586470; --paper:#f7fbff; --blue:#244f73; --green:#2f654c; --gold:#d8ad48; --line:#c9d5df; }
  * { box-sizing: border-box; }
  body { margin:0; color:var(--ink); font-family:"Aptos","Segoe UI",sans-serif; background:linear-gradient(135deg,#f6fbff,#f5f8eb); }
  .skip-link { position:absolute; left:1rem; top:-4rem; background:var(--ink); color:white; padding:.7rem 1rem; border-radius:999px; }
  .skip-link:focus { top:1rem; }
  header, main, footer { width:min(1120px, calc(100% - 32px)); margin:0 auto; }
  header { padding:48px 0 24px; }
  .eyebrow { color:var(--blue); text-transform:uppercase; letter-spacing:.18em; font-weight:800; font-size:.78rem; }
  h1 { max-width:980px; margin:0; font-family:Georgia,"Times New Roman",serif; font-size:clamp(2.5rem,7vw,5.4rem); line-height:.98; letter-spacing:-.05em; }
  .lede { max-width:840px; font-size:clamp(1.1rem,2.4vw,1.45rem); line-height:1.55; color:#31404a; }
  .badge { display:inline-flex; width:fit-content; padding:.45rem .75rem; border-radius:999px; background:var(--green); color:white; font-weight:900; }
  .grid { display:grid; grid-template-columns:repeat(12,1fr); gap:18px; }
  .card { grid-column:span 6; min-width:0; padding:24px; border:1px solid var(--line); border-radius:28px; background:rgba(255,255,255,.92); box-shadow:0 18px 40px rgba(35,43,50,.10); }
  .card.large { grid-column:span 12; }
  h2,h3 { font-family:Georgia,"Times New Roman",serif; letter-spacing:-.03em; }
  h2 { margin:0 0 14px; font-size:clamp(1.8rem,4vw,3rem); }
  p, li { line-height:1.65; }
  textarea, button { width:100%; border:1px solid #b9c6cc; border-radius:16px; padding:.85rem 1rem; font:inherit; }
  textarea { background:#f7f8fb; color:var(--ink); }
  button { width:fit-content; min-width:190px; border:0; background:var(--blue); color:white; font-weight:900; cursor:default; }
  .result { margin-top:18px; padding:18px; border-left:6px solid var(--green); border-radius:18px; background:white; }
  .warning { border-left-color:#b2603f; background:#fff8f4; }
  .kicker { color:var(--muted); font-size:.86rem; font-weight:900; letter-spacing:.08em; text-transform:uppercase; }
  footer { padding:38px 0 56px; color:var(--muted); }
  :focus-visible { outline:4px solid var(--gold); outline-offset:3px; }
  @media (max-width:760px) { header,main,footer{margin:0;max-width:390px;width:100%;padding-left:24px;padding-right:24px}header{padding-top:34px}h1{font-size:clamp(2.2rem,11vw,3rem)}.card{grid-column:span 12;padding:20px;border-radius:22px}button{width:100%} }
</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header>
  <p class="eyebrow">CivicSuite / CivicBoards public sample</p>
  <h1>Board rosters, terms, and vacancies without spreadsheet drift.</h1>
  <p class="lede">CivicBoards demonstrates board and commission administration support: roster stubs, term reminders, vacancy checklists, attendance review, and public-records-aware exports without making appointments or legal determinations.</p>
  <p><span class="badge">v0.1.1 board administration foundation</span></p>
</header>
<main id="main" tabindex="-1">
  <section class="grid" aria-labelledby="lookup-title">
    <article class="card large">
      <p class="kicker">Sample board roster</p>
      <h2 id="lookup-title">Planning Commission</h2>
      <textarea aria-label="Sample board notes" rows="4">Seven-member board, staggered terms, monthly meetings, clerk liaison, public vacancy notices, and attendance tracking.</textarea>
      <button type="button">Draft sample board file</button>
      <div class="result" role="status" aria-live="polite">
        <h3>Staff review packet</h3>
        <ul><li>Confirm enabling authority, appointment body, term length, quorum rule, and vacancy rule.</li><li>Track upcoming term ends and public vacancy notices.</li><li>Preserve agendas, packets, minutes, attendance, and appointment records.</li></ul>
      </div>
    </article>
    <article class="card"><p class="kicker">Terms</p><h2>Reminders, not reappointments</h2><div class="result"><p>CivicBoards surfaces term-end deadlines; staff decide eligibility and appointment timing.</p></div></article>
    <article class="card"><p class="kicker">Vacancies</p><h2>Public notice ready</h2><div class="result"><p>Vacancy helpers collect seat, term, authority, application-window, and notice-review context.</p></div></article>
    <article class="card"><p class="kicker">Attendance</p><h2>Review flags</h2><div class="result"><p>Attendance summaries flag review needs without removing or replacing members.</p></div></article>
    <article class="card large"><p class="kicker">Boundary</p><h2>No appointment decisions</h2><div class="result warning"><p>CivicBoards does not appoint members, remove members, make legal determinations, call live LLMs, publish official notices, or replace the clerk's board system of record.</p></div></article>
  </section>
</main>
<footer><p>CivicBoards is part of the Apache 2.0 CivicSuite open-source municipal AI project.</p></footer>
</body>
</html>
"""


def render_staff_page() -> str:
    """Render the staff-facing CivicBoards roster and review queue page."""

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CivicBoards Staff Workspace</title>
<style>
  :root { --ink:#17202a; --muted:#586470; --paper:#f7fbff; --blue:#244f73; --green:#2f654c; --gold:#d8ad48; --line:#c9d5df; --warn:#9c4e32; }
  * { box-sizing:border-box; }
  body { margin:0; color:var(--ink); font-family:"Aptos","Segoe UI",sans-serif; background:#f4f8fb; }
  .skip-link { position:absolute; left:1rem; top:-4rem; background:var(--ink); color:white; padding:.7rem 1rem; border-radius:999px; }
  .skip-link:focus { top:1rem; }
  header, main, footer { width:min(1180px, calc(100% - 32px)); margin:0 auto; }
  header { padding:34px 0 18px; }
  .eyebrow { color:var(--blue); text-transform:uppercase; letter-spacing:.14em; font-weight:800; font-size:.78rem; }
  h1 { margin:.2rem 0 .6rem; font-family:Georgia,"Times New Roman",serif; font-size:clamp(2.1rem,5vw,4.6rem); line-height:1; }
  .lede { max-width:860px; color:#31404a; font-size:1.08rem; line-height:1.55; }
  .grid { display:grid; grid-template-columns:390px minmax(0,1fr); gap:18px; align-items:start; }
  .panel { min-width:0; padding:22px; border:1px solid var(--line); border-radius:8px; background:var(--paper); box-shadow:0 12px 32px rgba(35,43,50,.08); }
  h2 { margin:0 0 14px; font-size:1.35rem; }
  label { display:block; margin:.85rem 0 .35rem; font-weight:800; }
  input, textarea, button { width:100%; border:1px solid #b8c6c0; border-radius:8px; padding:.78rem .9rem; font:inherit; }
  textarea { min-height:90px; resize:vertical; }
  button { margin-top:14px; border:0; background:var(--blue); color:white; font-weight:900; cursor:pointer; }
  button.secondary { background:var(--green); }
  button:disabled { opacity:.65; cursor:wait; }
  .status { margin-top:14px; padding:14px; border-left:5px solid var(--green); background:white; border-radius:8px; line-height:1.55; }
  .warning { border-left-color:var(--warn); background:#fff8f4; }
  .review-list { display:grid; gap:12px; }
  .review { padding:14px; border:1px solid var(--line); border-radius:8px; background:white; }
  .meta { color:var(--muted); font-size:.9rem; }
  footer { padding:32px 0 48px; color:var(--muted); }
  :focus-visible { outline:4px solid var(--gold); outline-offset:3px; }
  @media (max-width:820px) { header,main,footer{width:100%;padding-left:20px;padding-right:20px}.grid{grid-template-columns:1fr}.panel{padding:18px} }
</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header>
  <p class="eyebrow">CivicSuite / CivicBoards staff</p>
  <h1>Board roster review</h1>
  <p class="lede">Create local board roster records, attendance reviews, and staff queue items before appointments, removals, vacancy notices, minutes, or records export work.</p>
</header>
<main id="main" tabindex="-1">
  <section class="grid" aria-label="CivicBoards staff workspace">
    <form id="board-form" class="panel">
      <h2>Board review intake</h2>
      <label for="staff-key">Staff API key</label>
      <input id="staff-key" type="password" autocomplete="off">
      <label for="board-id">Board ID</label>
      <input id="board-id" value="pc-001">
      <label for="board-name">Board name</label>
      <input id="board-name" value="Planning Commission">
      <label for="liaison">Liaison</label>
      <input id="liaison" value="clerk@example.gov">
      <label for="review-reason">Review reason</label>
      <textarea id="review-reason">Confirm terms, vacancy notice needs, attendance review, and public records export context.</textarea>
      <button id="create-button" type="submit">Save board and queue review</button>
      <button id="attendance-button" class="secondary" type="button">Create attendance review</button>
      <button id="load-button" class="secondary" type="button">Load review queue</button>
      <div id="form-status" class="status" role="status" aria-live="polite">Ready.</div>
    </form>
    <section class="panel" aria-labelledby="queue-title">
      <h2 id="queue-title">Open board reviews</h2>
      <div id="queue" class="review-list" aria-live="polite"></div>
    </section>
  </section>
</main>
<footer><p>CivicBoards keeps roster and review work local. Staff remain responsible for appointments, removals, vacancy notices, meeting records, and legal compliance.</p></footer>
<script>
  const form = document.querySelector("#board-form");
  const keyInput = document.querySelector("#staff-key");
  const createButton = document.querySelector("#create-button");
  const attendanceButton = document.querySelector("#attendance-button");
  const loadButton = document.querySelector("#load-button");
  const statusBox = document.querySelector("#form-status");
  const queue = document.querySelector("#queue");

  function setStatus(kind, message) {
    statusBox.className = `status ${kind}`;
    statusBox.textContent = message;
  }

  function headers() {
    return {
      "Content-Type": "application/json",
      "X-CivicBoards-Role": "staff",
      "X-CivicBoards-Staff-Key": keyInput.value.trim()
    };
  }

  function field(id) {
    return document.querySelector(id).value.trim();
  }

  function renderQueue(items) {
    queue.replaceChildren();
    if (!items.length) {
      const empty = document.createElement("p");
      empty.textContent = "No board review items yet.";
      queue.appendChild(empty);
      return;
    }
    for (const item of items) {
      const card = document.createElement("article");
      card.className = "review";
      const title = document.createElement("h3");
      title.textContent = item.title || "Untitled board review";
      const reason = document.createElement("p");
      reason.textContent = item.reason || "Review required.";
      const meta = document.createElement("p");
      meta.className = "meta";
      meta.textContent = `${item.status || "open"} / ${item.board_id || "no board id"} / ${item.review_id || "no review id"}`;
      card.append(title, reason, meta);
      queue.appendChild(card);
    }
  }

  async function loadQueue() {
    setStatus("", "Loading staff queue.");
    const response = await fetch("/api/v1/civicboards/staff/reviews", { headers: headers() });
    const payload = await response.json();
    if (!response.ok) {
      const detail = payload.detail || {};
      setStatus("warning", detail.fix || detail.message || "Queue load failed.");
      return;
    }
    renderQueue(Array.isArray(payload.items) ? payload.items : []);
    setStatus("", "Staff queue loaded.");
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    createButton.disabled = true;
    setStatus("", "Saving board roster and queueing staff review.");
    try {
      const boardResponse = await fetch("/api/v1/civicboards/registry", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ board_id: field("#board-id"), board_name: field("#board-name"), liaison: field("#liaison") })
      });
      const boardPayload = await boardResponse.json();
      if (!boardResponse.ok) {
        const detail = boardPayload.detail || {};
        setStatus("warning", detail.fix || detail.message || "Board save failed.");
        return;
      }
      const reviewResponse = await fetch("/api/v1/civicboards/staff/reviews", {
        method: "POST",
        headers: headers(),
        body: JSON.stringify({ board_id: field("#board-id"), title: `${field("#board-name")} review`, reason: field("#review-reason") })
      });
      const reviewPayload = await reviewResponse.json();
      if (!reviewResponse.ok) {
        const detail = reviewPayload.detail || {};
        setStatus("warning", detail.fix || detail.message || "Staff review queue failed.");
        return;
      }
      setStatus("", `Saved ${boardPayload.board_name || "board"} and queued review ${reviewPayload.review_id || "pending"}.`);
      await loadQueue();
    } catch {
      setStatus("warning", "The local CivicBoards API did not respond. Check service logs and retry.");
    } finally {
      createButton.disabled = false;
    }
  });

  attendanceButton.addEventListener("click", async () => {
    attendanceButton.disabled = true;
    setStatus("", "Creating attendance review.");
    try {
      const response = await fetch("/api/v1/civicboards/attendance", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ member_name: "Avery Patel", meetings_attended: 2, meetings_held: 5 })
      });
      const payload = await response.json();
      if (!response.ok) {
        const detail = payload.detail || {};
        setStatus("warning", detail.fix || detail.message || "Attendance review failed.");
        return;
      }
      setStatus("", `Created attendance review ${payload.attendance_id || "pending"} with status ${payload.attendance_status || "pending"}.`);
      await loadQueue();
    } catch {
      setStatus("warning", "The local CivicBoards API did not respond. Check service logs and retry.");
    } finally {
      attendanceButton.disabled = false;
    }
  });

  loadButton.addEventListener("click", () => {
    loadQueue().catch(() => setStatus("warning", "The local CivicBoards API did not respond."));
  });
</script>
</body>
</html>
"""
