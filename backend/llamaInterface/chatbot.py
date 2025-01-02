from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = """
These inputs have been chosen by the user. Use them to generate a plot synopsis for a "Curb Your Enthusiasm" episode Plot.
Here are the inputs:
1. Cameo Character: {cameo_char}
2. New Location: {new_loc}
3. Chosen Event: {new_event}

The synopsis should be no more than 6 sentences long, and should include all of the inputs that the user has entered. 
It should also include familiar characters, locations and events from other episodes in the show.
The cameo character should get into an argument with Larry David.
Only return the plot synopsis, no introductory sentence.
"""

model = OllamaLLM(model="llama3")
prompt =  ChatPromptTemplate.from_template(template)
chain = prompt | model

def handle_conversation():
    context = ""
    print("Welcome to generate-your-enthusiasm")
    while True:
        user_input = input("You:")
        if user_input.lower() == "exit":
            break

        result = chain.invoke({"context": context, "question": user_input})
        print("Larry: ", result)
        context += f"\n {user_input}\nAI: {result}"

def handle_user_inputs():
    print(f"Welcome to generate-your-enthusiasm! \nLarry David is completely out of ideas and needs some help with ideas for the show.\nHelp a poor old jew out and give him some suggestions for new characters, events and locations.")

    cameo_char = input("Choose a new character: ")
    new_loc = input("Choose a new location: ")
    new_event = input("Choose an event to send Larry to: ")

    variables = {
        "cameo_char": cameo_char,
        "new_loc": new_loc,
        "new_event": new_event,
        }
    result = chain.invoke(variables)
    
    print("\nYour Episode:\n")
    print(result)

if __name__ == "__main__":
    handle_user_inputs()

