# The AI Scientist

set environment

```bash
export OPENAI_API_KEY="xxxx"
export OPENAI_BASE_URL="xxxx"
export OPENAI_API_BASE="xxxx"
```
modify the `docker-compose.yml` command:

```yml
  command: ["--model", "openai/gpt-4o-mini-2024-07-18", "--project-name", "manuscript"]
```

run it

```bash
docker compose up
```