# LearnbyYear

learnbyyear.com – England's national curriculum, one child and one year at a time.

Part of the Family Ecosphere (made by Handy Little Tools).

- `index.html` – the whole site. The curriculum data is inside it (`var DATA = …`).
- `curriculum.json` – the same data on its own, as pulled from the official documents.
- `tools/parse-curriculum.py` – how it was pulled from the text of the primary curriculum PDF.

Sources (Open Government Licence v3.0):
- The national curriculum in England: primary curriculum – https://www.gov.uk/government/publications/national-curriculum-in-england-primary-curriculum
- Early years foundation stage statutory framework (group and school-based providers, from September 2026) – https://www.gov.uk/government/publications/early-years-foundation-stage-framework--2

Deploy: Cloudflare Workers, `npx wrangler deploy`, from main.
