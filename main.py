"""
main.py
-------
Command-line entry point for the SafeX FAQ Chatbot.

Run with:
    python main.py
"""

from chatbot import SafeXFAQChatbot


def main():
    bot = SafeXFAQChatbot()
    print("SafeX Solutions FAQ Chatbot (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ("exit", "quit"):
            print("Bot: Thanks for chatting! Goodbye.")
            break

        result = bot.get_response(user_input)
        print(f"Bot: {result['answer']}")
        if result["matched_question"]:
            print(f"     (matched: \"{result['matched_question']}\" | confidence: {result['confidence']})")
        print()


if __name__ == "__main__":
    main()
