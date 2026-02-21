---
trigger: always_on
---

- When verifying the implementation, always run it via Docker and NOT on the local environment.
- If a new script is needed for debugging an issue place it in the scripts folder.
- Tests are always run on the local environment.
- When testing on the docker containers, only build them if needed. If there is a docker container already running use it.
