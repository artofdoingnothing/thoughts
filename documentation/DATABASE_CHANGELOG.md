# Database Changelog

## 2026-02-21

- Added `additional_info` column to the `persona` table to allow storing arbitrary key-value data for personas. This supports user-defined attributes that can be carried over to derived personas.
- Cleaned up boilerplate thoughts from the database. Deleted 128 thoughts containing RSS subscription and dark mode toggle text that were inadvertently scraped from blog footers.
