# Fact Resolution

The Fact Resolution system is responsible for extracting, comparing, and validating information across the website.

## Fact Representation
Facts are stored as structured observations:
- **Fact Type**: (e.g., Brand Name, Price, Contact Info)
- **Value**: The observed data
- **Source**: URL and specific location (e.g., JSON-LD, Visible Text)
- **Timestamp**: When the observation was made or the content's stated date

## Resolution States
When facts are compared across the site, they resolve to one of four states:
1. **RESOLVED**: Fact is consistent and corroborated across multiple sources/pages.
2. **PROBABLE**: Fact appears valid but lacks strong corroboration (e.g., appears only once).
3. **UNRESOLVED**: Direct contradiction between sources (e.g., Page A says $10, Page B says $15) with no deterministic way to resolve.
4. **INSUFFICIENT_EVIDENCE**: The fact cannot be reliably extracted or understood.

## Contradiction Handling
Contradictions yield findings. The system must preserve the conflicting evidence (e.g., citing both sources) rather than guessing the "correct" value.
