# -*- coding: utf-8 -*-
from flow import create_joke_flow

def main():
    """Main function to run the joke generator application."""
    print("Welcome to the Command-Line Joke Generator!")

    shared = {
        "topic": None,
        "current_joke": None,
        "disliked_jokes": [],
        "user_feedback": None
    }

#     main()     joke_flow = create_joke_flow()
    joke_flow.run(shared)

    print("\nThanks for using the Joke Generator!")

if __name__ == "__main__":

