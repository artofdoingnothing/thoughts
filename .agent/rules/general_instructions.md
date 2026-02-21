---
trigger: always_on
---

1. Whenever there is a change in database structure, update and rewrite the documentation in the documentations folder.
2. Maintain a changelog of the database changes in a separate file, with each log containing date, a short paragraph of what changed and why it was changed.
3. In scenarios where there is interaction needed with an llm, try to get structured responses like json instead of free text.
4. Use the documentation folder for referring to the code base domain models.
