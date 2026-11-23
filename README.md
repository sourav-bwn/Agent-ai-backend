# Agent AI Backend

Flask backend for the **Nexus AI Chat** assistant: a self-hosted chat app powered by OpenRouter, with per-session memory, switchable response modes, and lightweight tool use (web search and current time).

## Features

- Chat UI served at `/` (`templates/index.html`)
- Per-session conversation state, with simple memory (remembers your name when you say "my name is ...")
- Response modes, switched in chat: `/fast`, `/deep`, `/code`, `/dark`, `/normal`
- Tool use: the model can request a DuckDuckGo instant-answer lookup (`SEARCH: <query>`) or answer with the current time (`TIME`)
- Default model: `nousresearch/hermes-3-llama-3.1-405b` via OpenRouter

## Setup

```bash
pip install -r requirements.txt
export API_KEY=<your OpenRouter API key>   # https://openrouter.ai
python app.py
```

Then open http://localhost:10000 (the server binds `0.0.0.0:10000`, so other devices on your network can reach it too).

## API

| Endpoint | Method | Purpose |
| --- | --- | --- |
| `/` | GET | Chat UI |
| `/api/chat` | POST | Send `{"message": "...", "session_id": "..."}`; returns the assistant reply. Slash-commands (`/fast`, `/deep`, `/code`, `/dark`, `/normal`) switch the session's response mode. |
| `/api/sessions` | GET | List active session IDs |
| `/api/session/<session_id>` | DELETE | Delete a session |

## Tests

Offline tests mock the OpenRouter and DuckDuckGo calls - no network or API key needed:

```bash
python3 -m pytest tests
```
