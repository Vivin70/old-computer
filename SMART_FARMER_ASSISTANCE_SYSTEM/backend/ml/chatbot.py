def farmer_chatbot(user_input):
    user_input = user_input.lower()

    if "weather" in user_input:
        return "You can check the Weather Prediction section for rainfall and climate updates."

    elif "crop disease" in user_input or "disease" in user_input:
        return "Use the Crop Disease Predictor to identify possible diseases."

    elif "contract" in user_input or "price" in user_input:
        return "Check the Contract Predictor to know if a contract is profitable."

    elif "government" in user_input or "scheme" in user_input:
        return "Visit the Government Scheme section to see eligible schemes."

    elif "fertilizer" in user_input:
        return "Use balanced fertilizers and follow soil test recommendations."

    elif "hello" in user_input or "hi" in user_input:
        return "Hello Farmer! How can I help you today?"

    else:
        return "Sorry, I could not understand your question. Please try asking about weather, crops, or schemes."
