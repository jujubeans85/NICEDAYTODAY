# Unified Projects Monorepo (NICEDAYTODAY)

This repository consolidates multiple small projects into a single monorepo.

Structure
- apps/ - each original project lives in its own subfolder (apps/<project>)
- packages/ - shared Python libraries
- docs/ - migration notes and docs
- .github/workflows/ - CI definition

Quickstart
1. Clone:
   git clone <repo-url>
2. Create & activate venv:
   python -m venv .venv
   source .venv/bin/activate
3. Install dev deps:
   pip install -r requirements-dev.txt
4. Render or generate all apps:
   make render
   make generate

Per-app run instructions are in apps/<app>/README.md