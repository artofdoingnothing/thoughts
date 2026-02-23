# Database Changelog

## 2026-02-21

- Added `additional_info` column to the `persona` table to allow storing arbitrary key-value data for personas. This supports user-defined attributes that can be carried over to derived personas.
- Cleaned up boilerplate thoughts from the database. Deleted 128 thoughts containing RSS subscription and dark mode toggle text that were inadvertently scraped from blog footers.

## 2026-02-23

- Added `origin_description` column to the `persona` table. This field stores a string representing the source of movie-generated personas (e.g., 'character from movie(year)(rating)'). This change allows users to track the origin of derived identities in exports and UI views.
