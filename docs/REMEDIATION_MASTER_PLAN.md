# Remediation Master Plan — AI Finance System

**Project objective (17 October 2026):** Finish every previously identified weakness to a defensible, demonstrable academic-prototype standard; only then consider optional additions. Compare the original student repository and this fork **after remediation is complete**, provide an explicit change-by-change handover, then write the final university report from the frozen tested revision, and teach the student to explain it.

**Branches and custody:** Work exclusively on `Abhijith513/AI-Finance-System` branch `rescue/submission-critical-fixes`. Do not mutate `Layana7592/AI-Finance-System` or merge the fork's `main` before final review. Preserve the original dataset, results and academic limitations, documenting any revised experiment separately.

## Evidence-based gates

Statuses must be updated only from **actual tests, screenshots, benchmark artifacts, or source inspection**. A commit is implementation evidence, not completion evidence. A synthetic result is not a real-world fraud claim. An external Gemini call requires a real configured API key (never published). Report preparation is **after** the final technical freeze.

| ID | Problem to resolve | Concrete acceptance criteria | Current state |
|---|---|---|---|
| C1 | No normal login/logout | Presenter signs in with a password, backend verifies identity; sign-out prevents reuse of the active browser session; unauthorized accounts denied; integration tests and browser screenshot | VERIFIED on code revision 3ef32e1: real presenter login, server-side token deletion, old-token HTTP 401, fresh sign-in; 5/5 presenter tests in browser CI 39021961537. The guided presenter uses Admin permissions; general role-specific UI belongs to H9 |
| C2 | No end-to-end browser evidence | Clean DB + real Django + React + Chromium; 8/8 transaction/dashboard/report checks; screenshots and timing; separate analytics screen verified; no browser exceptions | VERIFIED: fresh 50k PostgreSQL+Django+React+Chromium run 8/8 steps in 9.5 s; full dashboard screenshot, report fallback, sign-out and revoked-token rejection. Browser run 39021961537; original PNG artifact is attached to run |
| C3 | Stale README results | Main README contains current **verified seed-42** numbers and provenance, with original experiment preserved unchanged and old counts clearly archived | VERIFIED by source review: README uses clean seed-42 metrics with provenance; original research numbers preserved separately in docs/HISTORICAL_README_RESULTS.md. New experiments must update source evidence independently. |
| C4 | No genuine figures in academic report | Screenshots and reproducible architecture/ER diagrams match *frozen* source; no fabricated views | VERIFIED in STAGED working draft: 8 actual Chromium screenshot figures plus code-derived architecture figure, in Appendix B and Chapter 3 respectively, visually rendered (38 A4 pages), full figure list and page references. Browser run 39021961537; final report after code freeze still pending. ER diagram/M13 not complete. |
| H5 | No held-out Isolation Forest evaluation | Time-separated training/test; no leakage; freeze threshold from training; complete precision/recall/F1/CM and class prevalence | Open |
| H6 | Unrealistic anomaly generator | Separate explicitly labelled behavioural-only anomaly cases (without gross-amount shortcuts); deterministic seed and label rationale; retain original 50k experiment unchanged | Open |
| H7 | Non-paired SARIMA validation | Same timestamps for both model metrics, including explicit SARIMA failures; error metrics only on matched successful windows plus failure coverage | Open |
| H8 | No model-error analysis | Case studies of FP/FN and missed anomalies, feature-level explanation, and residual/forecast-failure analysis; tables reproducible from code | Open |
| H9 | Limited operational UI | Authenticated read/write/read-back for synthetic transactions, fraud alerts, audit entries and investigation/resolution as authorized; branch boundaries; e2e evidence | Partial — guided presenter read-back exists |
| H10 | Expensive dashboard computation | Benchmark request latency; cache/version expensive model evaluations; invalidate on changing research data; live dashboard never retrains all 50k per navigation | Open |
| H11 | Unverified Gemini | Valid API/model with real key tested, numerical claims compared to Python truth, disclosure and deterministic fallback test; never claim live external AI when fallback is used | Open — fallback only |
| M12 | No explicit research hypotheses | Written hypothesis table about statistical baseline vs IF, synthetic-design sensitivity, and seasonal naive vs SARIMA with clearly defined validity and decision criteria | Open |
| M13 | Missing diagrams | Reproducible logical architecture, ER relations/cardinalities, dataflow and role/workflow security diagram; agree with actual code | Open |
| M14 | No timed performance benchmarking | Record median/p95 from repeated actual requests (login, new transaction, fraud read-back, dashboards, report/fallback); controlled data size and machine recorded | Partial — one timed walkthrough |
| M15 | No forecast uncertainty | Explain and evaluate calibrated interval method on held-out monthly data or explicitly document inadequacy with available 24 months; do not present arbitrary intervals as scientifically validated | Open |
| M16 | Incomplete ledger/reconciliation | Limit scope to a **synthetic accounting simulator**: explicit balanced journal entries, atomic posting, reconciliation tests, correction/reversal semantics, consistency under retries; do not claim core-banking certification | Open |

## Critical four: verified evidence ledger (17 October 2026)

- **C1 — Authentication:** `finance.test_presenter_demo` passed 5/5 in a real PostgreSQL CI job. Chromium logged in, ran all steps, called POST /api/logout/, and proved the previously presented token returned HTTP 401 for /api/me/. Re-login with a new token was also tested.
- **C2 — Browser acceptance:** GitHub Actions [run 39021961537](https://github.com/Abhijith513/AI-Finance-System/actions/runs/39021961537) completed all eight direct backend steps in **9.5 seconds** on the seeded **50,000 synthetic transactions**, rendered the analytics dashboard and fallback report, captured six genuine browser screenshots, and verified sign-out. The performance measurement is a single timed run, **not** median/p95 benchmarking (M14).
- **C3 — Source provenance:** [README](../README.md) contains recomputed seed-42 anomaly and forecasting findings with benchmark limitations. [Historical README Results](HISTORICAL_README_RESULTS.md) preserves the original metrics without replacing them. The clean benchmark should not be mixed with post-demo dashboard values.
- **C4 — Working report evidence:** A new, separately downloadable 38-page `Layana_Report_Stage1_Verified_Browser_Evidence.docx` has eight true screenshot figures, one source-grounded architecture diagram, actual captions and page references, and an explicit disclaimer about the demo-added 2026 transaction. The Word/PDF evidence bundle is retained in the user's conversation workspace; **not** a signed or frozen final manuscript. The original unmodified PNGs are in the 39021961537 GitHub Actions artifact.
- **Cross-check:** [CI run 39021961552](https://github.com/Abhijith513/AI-Finance-System/actions/runs/39021961552) passed **63/63 complete Django tests**, targeted regressions, React production build and lint on the verified code snapshot `3ef32e16734d4c902bf163076f5495c4934ec33d`.

No handover or final university report has been authorized; ten high/medium remediation areas remain under this master plan.

## Execution order — no new features until remediation gates are closed

1. **Baseline and live proof:** stabilize latest browser builds and 8/8 evidence, fix dashboard errors, provenance/README, add current CI test gates. Archive the original experiment.
2. **Research integrity:** H5–H8 then M12 and M15. Preserve original experiment unchanged; new datasets and matched-window evaluation are separate artifacts, not substitutions. Record model failures honestly.
3. **Operational reliability:** H9–H11 and M16. Server-side auth lifecycle, branch-scope tests, transaction/alert resolution and synthetic double-entry reconciliation; safe cached analytic API and measured latency M14.
4. **Documentation/visual evidence:** code-derived diagrams M13, genuine screenshots C4, reproducibility instructions, measured system specs. No invented model accuracy or clinical/financial impact claims.
5. **Freeze and external review:** exact commit, full suite, real browser acceptance, synthetic benchmark artifact, no secrets, threat/permission review. Then inspect **both** Layana's original and the fork; compare every material change.
6. **Handover to Layana:** share working fork and reviewed revision, commit/PR, exact setup, tests, screenshots, reasoning for every change, original experiment limitations, independent work she must understand; never silently overwrite her repository.
7. **Final university report and teaching:** build only from the frozen version and measured figures; apply exact Kannur University PGDDSA format, insert verified visuals/certifications, teach complete functionality and prepare a viva with practical exercises.

## Scope constraints and risk

- The October 21 report deadline is real. Implementing **all 16** issues (particularly a ledger engine, new research experiments, uncertainty calibration and a live third-party Gemini check) may exceed that date. Do not fabricate completed milestones to claim a deadline has been met. Escalate actual schedule risks openly.
- Banking transactions stay synthetic. H11 needs an external API key and may entail costs; no credentials or personal bank/customer data belong in this repository.
- Deliver functionality with tests, not speculative features; user decides any additional scope after remediation.
- No final report content or university submission claim is to be authored as complete until a frozen revision and evidence exist.
