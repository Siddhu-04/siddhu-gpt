# siddhu-gpt 

> Multi-provider AI CLI assistant. Stream responses from Groq or Ollama right in your terminal.

## Install

```bash

Run:-
siddhu-gpt chat
siddhu-gpt providers
siddhu-gpt sessions

or

pip install siddhu-gpt

or

uv run siddhu-gpt --help
uv run siddhu-gpt chat
uv run siddhu-gpt providers
uv run siddhu-gpt sessions

May require api key.It's free BTW, just login to their website and get api key. Use it, It's that simple.
```

## Setup

```bash
export GROQ_API_KEY=your_key_here
```

## Usage

```bash
siddhu-gpt chat                          # default groq session
siddhu-gpt chat --session-id work        # named session
siddhu-gpt chat --provider ollama        # local Ollama
siddhu-gpt sessions                      # list past sessions
siddhu-gpt summary work                  # summarize a session
siddhu-gpt providers                     # check available providers
```

## Features

- Streaming responses with live Markdown rendering
- Persistent sessions (JSON, stored in `~/.siddhu-gpt/`)
- Multi-provider: Groq (cloud, free) + Ollama (local)
- Session summary via LLM
