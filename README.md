```markdown
# Task 2: AI Business Assistant

AI-powered assistant that analyzes a local business using its website,
Google reviews, and competitor data — then delivers actionable recommendations.

## How It Works

```
Website URL → Scraper → Claude AI → Business Report + Action Plan
Google Reviews → Sentiment Parser ↗
Competitor URLs → Gap Analyzer ↗
```

1. **Scraper** (`scraper.py`) — extracts content from business website
2. **Reviews** (`reviews.py`) — parses Google review sentiment and themes
3. **Competitor** (`competitor.py`) — identifies gaps vs competitor websites
4. **Claude AI** (`main.py`) — synthesizes all data into a structured report
5. **Dashboard** (`frontend/index.html`) — interactive UI for inputting and viewing results

## Output

| Section | Description |
|---------|-------------|
| Health Score | 0–100 overall business score |
| Summary | AI-written business diagnosis |
| Key Findings | Specific evidence-based findings |
| Problems | Pain points identified |
| Opportunities | Growth areas detected |
| Competitor Insights | How competitors differ |
| Action Plan | 5 prioritized steps with timeline + cost |

---

## Quickstart

### 1. Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Add your API key

Create a `.env` file inside `backend/` (one already exists — just fill it in):

```
ANTHROPIC_API_KEY=your_key_here
```

### 3. Start the server

```bash
cd backend
uvicorn api:app --reload
```

### 4. Open the dashboard

The browser opens automatically at `http://127.0.0.1:8000`.
If it doesn't, open it manually.

### 5. Run an analysis

Fill in the form:
- **Website URL** — the business website to analyze
- **Business type** — e.g. local bakery, gym, restaurant
- **Google reviews summary** — paste or describe the reviews
- **Competitor URLs** — comma-separated (optional)

Click **Analyze business** — results appear below the form.

---

## Project Structure

```
task2_business_assistant/
├── backend/
│   ├── api.py           # FastAPI server (run this)
│   ├── main.py          # Core analysis engine + Gemini integration
│   ├── scraper.py       # Website content scraper
│   ├── reviews.py       # Google review parser
│   ├── competitor.py    # Competitor gap analysis
│   ├── .env             # Your API key goes here
│   └── requirements.txt
└── frontend/
    └── index.html       # Dashboard (served automatically at /)
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serves the dashboard UI |
| POST | `/analyze` | Full business analysis |
| GET | `/health` | Health check |
| GET | `/docs` | Swagger UI |

### Example request

```json
POST /analyze
{
  "website_url": "https://mybakery.com",
  "business_type": "local artisan bakery",
  "google_reviews": "3.8 stars, 142 reviews. Fresh bread praised. Complaints about long wait times.",
  "competitor_urls": ["https://competitor1.com", "https://competitor2.com"]
}
```

### Open the dashboard

After starting the FastAPI server, open the dashboard in your browser:

```text
http://127.0.0.1:8000
```

The frontend interface is served automatically by the backend application.

###  Run an analysis

Using the dashboard, enter:

* **Website URL** — the business website to analyze
* **Business Type** — e.g. local bakery, gym, restaurant
* **Google Reviews Summary** — paste or describe customer reviews
* **Competitor URLs** — comma-separated competitor websites (optional)

Click **Analyze Business**.

The application will:

1. Scrape the business website content
2. Analyze customer review sentiment
3. Compare the business against competitors
4. Generate AI-powered business insights
5. Display a complete business report with recommendations directly in the dashboard

The generated report includes:

* Health Score
* Business Summary
* Key Findings
* Problems Identified
* Opportunities
* Competitor Insights
* Prioritized Action Plan


---

## Production Extensions

- Use **Firecrawl** for JS-rendered website scraping
- Integrate **Google Places API** for live review data
- Add **SerpAPI** for competitor search rankings
- Store reports in **PostgreSQL** with history tracking
- Add **PDF export** for client reports
```
