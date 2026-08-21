# 06 — Chatbot Interfaces & Streaming Outputs

## What You'll Learn
- `gr.ChatInterface` for instant conversational UIs
- Message history formats and how Gradio manages multi-turn state
- Streaming responses token-by-token using Python generators
- Building a chatbot with `gr.Blocks` for full control

---

## The Scenario

PyRail wants a **customer-support chatbot**: "When does the next train to Delhi leave?", "Can I get a refund on ticket PYR004?" It needs to feel responsive (streaming text, like ChatGPT) rather than waiting several seconds for a full reply to appear at once.

---

## Logic: `gr.ChatInterface` — The Fast Path

```python
import gradio as gr

def pyrail_bot(message, history):
    if "refund" in message.lower():
        return "Refunds are processed at 90% of fare if cancelled 7+ days before travel."
    if "delhi" in message.lower():
        return "The next train to Delhi (12951 Rajdhani) departs at 16:25 daily."
    return "I can help with bookings, cancellations, and schedules. Could you rephrase that?"

demo = gr.ChatInterface(
    fn=pyrail_bot,
    title="PyRail Support Bot",
    examples=["When's the next train to Delhi?", "How do refunds work?"],
)

demo.launch()
```

### Logic Behind the Code

- `gr.ChatInterface` is a **specialized wrapper** (like `gr.Interface`, but purpose-built for chat) — it auto-generates the entire chat UI: message bubbles, a text input, a send button, and automatic scrolling, and it manages conversation history for you.
- Your function receives **two** arguments automatically: `message` (the latest user input) and `history` (the full conversation so far, as a list) — you don't manually append to history yourself; `ChatInterface` handles storing and re-supplying it on every call, similar to how `gr.State` persists data (Module 04), but built specifically for the chat message-list shape.
- The function's **return value becomes the bot's next message** — no need to manage a "who said what" data structure yourself unless you drop down to raw `Blocks` (shown below).

---

## Using Conversation History for Context

```python
def pyrail_bot(message, history):
    # history is a list of {"role": ..., "content": ...} dicts (or (user, bot) tuples, depending on type=)
    previous_topics = [turn["content"] for turn in history if turn["role"] == "user"]

    if "refund" in message.lower() and any("ticket" in t.lower() for t in previous_topics):
        return "Since you mentioned a ticket earlier, I'll check its specific refund eligibility."
    return "How can I help with your PyRail booking today?"
```

- Because `history` is handed to you fresh on every call, you can implement **any** context-aware logic — keyword matching (as above), or passing the whole history into an LLM API call for a real conversational model.

---

## Streaming Responses

For a real LLM backend (or any slow-to-generate response), returning the full text only after it's complete feels sluggish. Gradio supports **streaming** via Python generators — `yield` partial results instead of `return`-ing once.

```python
import time
import gradio as gr

def pyrail_bot_streaming(message, history):
    full_response = "Thanks for reaching out! The next train to Delhi departs at 16:25 daily from Platform 3."
    partial = ""
    for word in full_response.split():
        partial += word + " "
        time.sleep(0.05)   # simulate token-by-token generation
        yield partial

demo = gr.ChatInterface(fn=pyrail_bot_streaming, title="🚆 PyRail Support Bot (Streaming)")
demo.launch()
```

### Logic Behind the Code

- Simply **changing `return` to `yield`, called repeatedly inside a loop**, is enough for Gradio to detect the function is a generator and switch into streaming mode automatically — each `yield`ed value **replaces** the previously displayed partial message in the chat bubble, building up the illusion of live typing.
- This is the same pattern used to stream real LLM API responses (e.g., OpenAI's or Anthropic's streaming APIs) — instead of `time.sleep` + hardcoded text, you'd iterate over the API's streamed chunks and `yield` the accumulated text so far after each chunk arrives.

---

## Full Control: Chat UI Built with `gr.Blocks`

```python
import gradio as gr

def respond(message, chat_history):
    bot_message = f"You said: {message}"
    chat_history.append({"role": "user", "content": message})
    chat_history.append({"role": "assistant", "content": bot_message})
    return "", chat_history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(type="messages", label="PyRail Support")
    msg = gr.Textbox(label="Your message", placeholder="Ask about bookings, refunds, schedules...")
    clear = gr.Button("Clear")

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: [], None, chatbot)

demo.launch()
```

### Logic Behind the Code

- Dropping to raw `gr.Blocks` for chat (instead of `ChatInterface`) is the move once you need things `ChatInterface` doesn't offer out of the box — e.g., a sidebar of conversation history, custom buttons next to the input, or multiple chat panels on one page (echoing the `Interface` → `Blocks` progression from Module 03).
- `gr.Chatbot(type="messages")` expects and displays a list of `{"role": "user"/"assistant", "content": ...}` dicts — this newer format aligns directly with the message format used by most LLM chat APIs (OpenAI, Anthropic), making it trivial to pass `chat_history` straight into an API call.
- `msg.submit(respond, [msg, chatbot], [msg, chatbot])`: the **outputs** list re-targets `msg` itself, back to an empty string (`""`) — this is the standard trick to **clear the textbox** after sending, since the function's first return value overwrites the input box's own displayed value.
- `clear.click(lambda: [], None, chatbot)`: a trivial inline `lambda` with no inputs (`None`) that returns an empty list, wired to overwrite `chatbot`'s value — a quick, readable way to implement small one-off logic without defining a named function.

---

## Try It Yourself

1. Extend `pyrail_bot` (non-streaming version) with at least 3 more keyword-based intents (e.g., "baggage," "platform," "seat change").
2. Convert your extended bot to streaming by changing it into a generator, `yield`ing word-by-word.
3. Rebuild the `Blocks`-based chat UI with an added `gr.Dropdown` above the chat that lets the user pick a "support category" (Booking / Refunds / General), and have `respond` prepend a system-style note into the conversation based on the selection.

**Next up:** `07_custom_theming_and_auth.md` — theming, custom CSS, and adding authentication to your Gradio app.
