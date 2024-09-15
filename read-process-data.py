from pymongo import MongoClient
import openai
import os
import json

try:
    uri = "mongodb+srv://username:password@database-url.mongodb.net/?retryWrites=true&w=majority&appName=app"
    # Create a new client and connect to the server
    client = MongoClient(uri)
    print('Connected to MongoDB server successfully.')
    
    openai.api_key = ""

    db = client['amazon-product-reviews']
    collection = db['reviews']
    print('Selected database and collection successfully.')
    
    # Filtering documents
    # for doc in collection.find({'ProfileName': 'delmartian'}):
        # print(doc)
        
    # Query for full-text search
    query = "what was the quality of canned dog and how many people loved it? Is there a better nutritional value in it compared to other products?"
    results = collection.find({"$text": {"$search": query}})
    # print(len(results))
    context = ""
    # Print results
    for doc in results:
        doc_str = f"ProfileName: {doc['ProfileName']}\nSummary: {doc['Summary']}\nReview: {doc['Text']}\n\n"
        context += doc_str
        # print(result['Summary'], result['Text'])
        # found.append()
    
    print(context)
    
    prompt = f"""
    You're a product review assistant. Answer the user QUESTION based on CONTEXT - the documents retrieved from our FAQ database. 
    Only use the facts from the CONTEXT. If the CONTEXT doesn't contain the answer, return "Review Not Found"

    QUESTION: {query}

    CONTEXT:

    {context}
    """.strip()
    
    assistant = openai.beta.assistants.create(
    name="Product Reviewer",
    instructions="You are an amazon product reviewer. Answer the user QUESTION based on CONTEXT - the documents retrieved from our reviews database. Only use the facts from the CONTEXT. If the CONTEXT doesn't contain the answer, return Reviews Not Found",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o-mini",
    )
    thread = openai.beta.threads.create()
    message = openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=query
    )
    run = openai.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Please address the user as Jane Doe. The user has a premium account."
    )
    if run.status == 'completed': 
        messages = openai.beta.threads.messages.list(
            thread_id=thread.id
        )
        # print(messages)
        # Assuming your response is in an object like 'SyncCursorPage[Message]'
        # Step 1: Convert the object to a dictionary or JSON string
        # Using a hypothetical `to_dict()` method, or manually accessing attributes if necessary.
        # Replace the next line with how your object provides data
        response_dict = messages.to_dict()  # Or use to_dict() if available

        # Step 2: Dump the dict into a JSON string to simulate the JSON structure
        response_json = json.dumps(response_dict)

        # Step 3: Load the JSON string back into a dictionary
        response = json.loads(response_json)
        
        for message in response['data']:
            if message['role'] == 'assistant':
                content = message['content'][0]['text']['value']
                print("Extracted Response:\n", content)
    else:
        print(run.status)
    # response = openai.beta.threads.messages.list(
    # thread_id=my_thread_id
    # )
    # print(response['choices'][0]['message']['content'])
    # print(message)
    
except Exception as e:
    print("exception" , e)
