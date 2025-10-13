# Test Data for Chatbot
# This file contains various test inputs to help you test your chatbot manually

# Greeting Test Cases
greeting_inputs = [
    "hi",
    "hello", 
    "hey",
    "Hi there!",
    "Hello world",
    "Hey buddy",
    "HELLO",
    "HI",
    "HEY THERE",
    "hi chatbot",
    "hello there",
    "hey how's it going",
]

# How are you Test Cases  
how_are_you_inputs = [
    "how are you",
    "how are you?",
    "How are you doing?",
    "HOW ARE YOU",
    "how are you today",
    "how are you feeling",
    "how's it going",
    "how are things",
]

# Unknown/Random Test Cases
unknown_inputs = [
    "what's your name",
    "tell me a joke",
    "what time is it",
    "help me",
    "goodbye",
    "see you later",
    "thanks",
    "what can you do",
    "random text",
    "123456",
    "programming",
    "weather",
    "food",
    "",  # empty input
    "   ",  # whitespace only
]

# Edge Cases
edge_cases = [
    "exit",  # should end the chat
    "EXIT",
    "Exit",
    "hi exit hello",  # contains both greeting and exit
    "how are you exit",  # contains both question and exit
]

# Mixed Case and Punctuation
mixed_cases = [
    "Hi!",
    "Hello.",
    "Hey?",
    "How Are You???",
    "hi...",
    "HELLO!!!",
    "hey there buddy!",
]

# All test data combined
all_test_data = {
    "greetings": greeting_inputs,
    "how_are_you": how_are_you_inputs, 
    "unknown": unknown_inputs,
    "edge_cases": edge_cases,
    "mixed_cases": mixed_cases,
}

# Function to print all test data
def print_test_data():
    for category, inputs in all_test_data.items():
        print(f"\n{category.upper()} TEST CASES:")
        print("-" * 30)
        for i, test_input in enumerate(inputs, 1):
            print(f"{i:2d}. '{test_input}'")

if __name__ == "__main__":
    print("CHATBOT TEST DATA")
    print("=" * 40)
    print_test_data()
    print(f"\nTotal test cases: {sum(len(inputs) for inputs in all_test_data.values())}")