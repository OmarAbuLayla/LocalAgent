#!/usr/bin/env python3
import argparse
import requests


def chat_loop(base_url: str) -> None:
    print("Connected to", base_url)
    print("Type 'exit' to quit.")
    while True:
        try:
            message = input("\nYou: ").strip()
        except EOFError:
            break
        if not message:
            continue
        if message.lower() in {"exit", "quit"}:
            break
        resp = requests.post(f"{base_url}/chat", json={"message": message}, timeout=600)
        resp.raise_for_status()
        payload = resp.json()
        reply = payload.get("reply", "")
        logs = payload.get("logs", "")
        print("\nAssistant:\n", reply)
        if logs:
            print("\n--- Tool Logs ---\n", logs)


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple CLI for the DevAgent API")
    parser.add_argument("--url", required=True, help="ngrok public URL, e.g. https://xxxx.ngrok-free.app")
    args = parser.parse_args()
    base_url = args.url.rstrip("/")
    chat_loop(base_url)


if __name__ == "__main__":
    main()
