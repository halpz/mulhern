# Stephen Mulhern Chat App

Welcome to the *official* Stephen Mulhern Chat App! 🤖🎩

If you've ever wanted to chat with the legend himself (well, kind of), you've come to the right place! This app brings you *somewhat* close to the magic of Stephen Mulhern, minus the real-time audience and incredible tricks. 😎✨

---

## 👇 Features:

- **Talk to Stephen**: Send messages to Stephen and get **mysterious** responses. (Not quite the magic of TV, but we're getting there.)
- **Instant Messaging**: Like a real-time chat experience, only with a bit more... *Mulhern*.
- **Clear Chat**: Get too carried away with the conversation? Hit the "Clear Chat" button and start fresh!

---

## 💡 How to Use:

1. **Send a message**: Type your deepest thoughts into the text box (or just say "Hello!"—Stephen won't judge).
2. **Submit it**: Click *Send* or press *Enter* to send your message. 🚀
3. **Wait for a response**: Stephen will respond with his usual flair (or at least, we'll try).
4. **Clear the chat**: Hit the *Clear Chat* button when you're ready to start over. (Don't worry, Stephen will always be there for you.)



# [Live Demo](https://mulhern.paulhalpin.co.uk)


## 🖼️ The Iconic Stephen Mulhern

Of course, every great app needs a great face. Here's a sneak peek at the man himself, who doesn't just appear on TV—now he's in your app! 😄

![Stephen Mulhern](resources/mulhern.jpg)

---

## 🚀 How to Run Locally:

1. Clone this repo:
   ```bash
   git clone https://github.com/halpz/mulhern.git
   ```
2. Enter directory:
   ```bash
   cd mulhern
   ```
3. Create a python environment
   ```bash
   python3 -m venv .venv
   ```
4. Enter python environment
   ```bash
   source .venv/bin/activate
   ```
5. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
6. Export your own OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
7. Run the app:
   ```bash
   fastapi dev main.py
   ```
8. Navigate to `http://127.0.0.1:8000` in your browser
