# Risks

**Objective:** ODFW wildlife experts can view and edit Oregon species range and habitat maps, from USGS GAP models and machine-learning sources, in a tool that is easy to download, run and use.

**How to read this:** L/I is likelihood/impact (High, Medium, Low), with the reason. Each risk reads as *condition → consequence*. Reviewed by the Project Manager at every sprint planning; a risk whose trigger fires becomes a GitHub issue.

**Last reviewed:** 2026-10-31, commit `144fb25`.

## Open risks

| ID | Risk | Type | L/I (why) | Owner | Response | Trigger |
|----|------|------|-----------|-------|----------|---------|
| R-1 | Stack not chosen → a heavy stack means experts can't easily install the tool | Tech | H/H (no decision yet; ease of install is the objective) | Julie | Mitigate: score RFC options on install steps and admin rights; ADR after team vote | No stack ADR by end of Sprint 3 |
| R-2 | Data paths hard-coded to one PC → the script only runs after editing code | Tech | H/H (true now; blocks every new user) | Kathryn | Mitigate: move paths to a config file | Clean clone can't run without editing `script.py` |
| R-3 | No tests; hydrography classes unconfirmed → wrong maps go unnoticed | Tech | H/H (nothing checks output; ODFW decides from it) | Jae | Mitigate: unit tests in CI; compare kit fox to the USGS map | No test job in CI by Sprint 3 review |
| R-4 | Scope beyond the starter script unconfirmed → team builds the wrong features | Business | M/H (goal known, details not; costs terms) | Julie | Mitigate: written questions to ODFW; answers go in `requirements.md` | No answer 2 weeks after asking |
| R-5 | ODFW install rules unknown → staff may be unable to run the tool | Business | M/H (state PCs often restricted; blocks the objective) | Julie | Mitigate: ask ODFW; feed answer into R-1 | No answer 2 weeks after asking |
| R-6 | Public repo, no place for partner data → partner data reaches git or an AI tool | Business | M/H (no storage agreed; breaks charter and trust) | Jae | Mitigate: agree storage with ODFW; ignore it in git; restate the rule in `CONTRIBUTING.md` | Partner data arrives before storage is agreed |
| R-7 | CI only checks out the repo → PRs pass the required check without being tested | Tech | M/M (placeholder workflow; recoverable) | Adison | Mitigate: add a CI job that installs dependencies and imports the script; make it a required check | No real CI job by Sprint 3 review |
| R-8 | All roles rotate at end of fall → setup knowledge is lost at handoff | Team | M/M (rotation certain; costs 1–2 weeks) | Kathryn | Mitigate: each role writes a handoff note | A note is missing at last fall sprint review |
| R-9 | Manual data downloads into exact folders → setup fails with unclear errors | Tech | M/M (3 large downloads; costs hours) | Kathryn | Mitigate: startup check naming missing folders | A tester needs help with data setup |
| R-10 | Public iNaturalist CSV with names, mixed licenses, unverified rows → license or accuracy problems | Business | M/M (public now; costs a takedown) | Jae | Mitigate: trim columns, research grade only, attribute | Map shared before data is trimmed |
| R-11 | No `.gitignore` → large rasters get committed and pushes fail | Tech | M/M (data sits in repo tree; slow to undo) | Adison | Mitigate: add `.gitignore` for data and figures | A push is rejected for file size |
| R-12 | Finals week before the checkpoint → planned work slips | Team | M/L (certain; costs days) | Julie | Mitigate: merge the week before finals | Checkpoint issues open at start of finals |
| R-13 | GAP data dates from 2001 → map misses land-use change | Business | L/M (current published models; local errors) | Julie | Accept: it's the source model; ML maps cover newer data. *Contingency:* propose newer land cover | ODFW asks about current land use |
| R-14 | Script still runs the Southwest region, which has no water data → wasted work outside Oregon | Tech | L/L (outside Oregon) | Jae | Eliminate: run Northwest only; close in that PR | Closes when the change merges |

## External prerequisites

| Waiting on | For | From | Asked |
|------------|-----|------|-------|
| Feedback on architecture options | R-1 | ODFW partner | 10/21 meeting; partner asked for more research |
| Scope: features, species, data sources, output format | R-4 | ODFW partner | Start by 11/4 meeting |
| What staff can install | R-5 | ODFW partner / IT | Start by 11/4 meeting |
| Remaining 8 data sources and ML maps | R-4 | ODFW partner | Start by 11/4 meeting |
| Partner-data storage; repo stays public? | R-6 | ODFW partner | Before any partner data is shared |
| Biologist review of first kit fox map | R-3 | ODFW partner | Start by 11/18 |
| Repository license | Handoff | ODFW partner, course IP terms | Start by 11/18 |
| Approval of any scope change | R-4 | Instructional team | Only if scope changes |

When something is asked, replace the start-by date with who asked and when.

## Closed

- **R-15 Repository access:** settled at the 10/14 partner meeting.
- **R-16 Only one person could make a map:** everyone ran the script in Sprint 1.
- **R-17 No branch protection on `main`:** enabled 10/30; PRs now need 2 approvals.
