"""Static public UI shell for CivicBoards v0.1.0."""

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
  @media (max-width:760px) { header{padding-top:34px}.card{grid-column:span 12;padding:20px;border-radius:22px}button{width:100%} }
</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header>
  <p class="eyebrow">CivicSuite / CivicBoards public sample</p>
  <h1>Board rosters, terms, and vacancies without spreadsheet drift.</h1>
  <p class="lede">CivicBoards demonstrates board and commission administration support: roster stubs, term reminders, vacancy checklists, attendance review, and public-records-aware exports without making appointments or legal determinations.</p>
  <p><span class="badge">v0.1.0 board administration foundation</span></p>
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
