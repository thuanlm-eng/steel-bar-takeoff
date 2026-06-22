# Steel Bar Takeoff

Extract steel reinforcement (rebar) quantities automatically from PDF shop drawings, using AI (Claude). Upload a PDF, the app reads the bar callouts and bending schedules, and produces quantities, lengths and weights — then exports to Excel.

> 🇻🇳 Hướng dẫn sử dụng bằng tiếng Việt: [HUONG-DAN-SU-DUNG.md](HUONG-DAN-SU-DUNG.md)

## Features

- **PDF text + OCR extraction** — reads digital PDFs with pdf.js, falls back to Tesseract.js OCR for scanned/image drawings.
- **AI parsing** — sends the drawing text to Claude (`claude-opus-4-8`) which returns structured bar data.
- **Understands standard rebar callouts** — e.g. `⑮ 18Ø14a200 L=4320` → mark 15, 18 bars, Ø14 mm, spacing 200 mm, length 4320 mm.
- **Automatic weight calc** — `kg/m = (dia² × π/4) × 7850 / 1,000,000`, matching standard rebar unit weights.
- **Dashboard** — filter-aware totals, a weight summary table per diameter (with subtotals + %), and a detailed table that groups identical bar marks.
- **Export** — one-click `.xlsx` (two sheets: *Bar takeoff* + *Summary by diameter*) or copy as CSV.
- Clean, flat UI with dark mode.

## How it works

The app runs as a single HTML page served by a tiny local Python server. The server also **relays the API request to Claude server-side**, which avoids the browser CORS / "Failed to fetch" errors you get when calling the API directly. Your API key is read from the request and forwarded straight to Anthropic — it is never stored or logged.

```
Browser (localhost:8765)  →  server.py (local relay)  →  Claude API
```

## Requirements

- **Python 3** ([download](https://www.python.org/downloads/)) — uses the standard library only, no `pip install` needed.
- **A Claude API key with credits** — create one at [console.anthropic.com](https://console.anthropic.com) → API Keys, then add credits under Plans & Billing. (API billing is separate from a Claude.ai subscription.)

## Usage

1. Double-click **`start-takeoff.bat`** (Windows). It starts the server and opens your browser at `http://localhost:8765`.
   - On macOS/Linux, run `python server.py` instead.
2. Drag in your PDF shop drawing.
3. Paste your Claude API key (`sk-ant-...`).
4. Click **Extract bars**.
5. Review the dashboard, filter by diameter/zone, then **Download Excel**.

> ⚠️ Open the app through `http://localhost:8765`, not by double-clicking the `.html` file directly — the direct-file path is blocked by the browser.

## Files

| File | Role |
|------|------|
| `steel-bar-takeoff.html` | The app (UI + logic) |
| `server.py` | Local server + Claude API relay |
| `start-takeoff.bat` | One-click launcher (Windows) |
| `HUONG-DAN-SU-DUNG.md` | User guide (Vietnamese) |
| `PROMPT-PROJECT.md` | One-prompt project summary |

## Notes

- The app sends roughly the first 18,000 characters of the PDF to Claude. For very long documents, split out the sheet containing the bar schedule.
- Client drawings (`*.pdf`) and exports (`*.xlsx`, `*.csv`) are git-ignored by default so they aren't committed.
