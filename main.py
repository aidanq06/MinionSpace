# Importing the OpenAI library and initializing the client
import openai
from openai import OpenAI
from rich import print
from rich.panel import Panel

# API key for authentication with OpenAI API
API_KEY = "HSZNPCSJAYWDXOSFV5MAHCUK3YQ6RINDVZTKIJNNKKO22B655QW24OS6OBC7WFHZ"


# Initialize OpenAI client with the base URL (customized for your use case)
client = openai.OpenAI(api_key=API_KEY, base_url="http://jamsapi.hackclub.dev/openai/")
# Initial game context and instructions for the AI to simulate the game
contextList = [
    "Welcome to the minion game! You are stuck on the moon after a failed rocketship from the minion space agency. You only have supplies for 7 days. However, Gru is trying to steal the moon and you need to stop him. Each turn is one day.\n", 
    "We are simulating a game for the minions movie. Here's the plot: I am stuck on the moon after a failed rocketship from the minion space agency. We only have supplies that can let us live up to 7 days. Each turn is a day. Gru is trying to steal the moon and we need to stop him. Simulate a game where you give the user scenarios and ask what he does. Phrase it like this: Today: (situation). [gives them options]. What do you do? Provide all responses in just text format, do not use any symbols under any circumstance. At the beginning of each turn, list the resources, and the amount of days it would last the player. The player starts with 7 days of oxygen, food, water, and no shelter. Having no shelter can lead to unpredictable circumstances. Also there are aliens on the moon, some are friendly, some are not. Keep the text brief by just listing what went on on the day the chat is on. Make sure to give the options the user has every single time and list the resources every single time and subtract the most previous resources by 1. Make it you vs yourself, dealing with internal challenges."
]

# Main function to handle the game loop
def prompt_engineering_game():
    # Display the initial game introduction
    print(contextList[0])

    # Initial API call to OpenAI to set the game context
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Specify the AI model to use
        messages=[{"role": "user", "content": contextList[1]}],  
        max_tokens=100,  # Limit the response length
        temperature=1.7  # Increase randomness for creative responses
    )

    # Extract and display the AI's initial response
    ai_response = response.choices[0].message.content
    contextList.append(f"AI Response: {ai_response}")  # Save response to context list for continuity
   
    print(ai_response)

    # Continuous game loop
    while True:
        # Get user input for their choice
        user_prompt = input("Response: \n")
        contextList.append(f"User Response: {user_prompt}")  # Append user response to context list

        try:
            # Combine all previous interactions to maintain context for the AI
            contextString = str()
            for i in contextList:
                contextString += i 

            # Send updated context to OpenAI for the next turn
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Specify the AI model to use
                messages=[{
                    "role": "user",
                    "content": f"{contextString}"  # Pass the entire game history
                }],
                max_tokens=100,  # Limit the response length
                temperature=1.7  # Maintain creative randomness
            )

            # Extract and display the AI's response for the current turn
            ai_response = response.choices[0].message.content
            print("\nAI Response:")
            print(ai_response)
            contextList.append(f"AI Response: {ai_response}")

        except Exception as e:
            # Handle any errors during the API call
            print(f"An error occurred: {e}")
            break

# Entry point for the game
if __name__ == "__main__":
    # Start the game loop
    prompt_engineering_game()
