# Argue With My Data

Most AI data analysts give you an answer. Argue With My Data tries to prove itself wrong first.

When a business metric changes, it generates competing explanations, writes down what evidence would support or reject each one, runs deterministic tests, and only then reports which explanations hold up.

**The LLM proposes. Code tests. The critic challenges. Evidence decides.**

## Run it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then add your GEMINI_API_KEY and GEMINI_MODEL
streamlit run app.py
```

## Team

The team plan, roles and timeline are in [docs/team/PLAN.md](docs/team/PLAN.md).
