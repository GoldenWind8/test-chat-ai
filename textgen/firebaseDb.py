import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase app
cred = credentials.Certificate('textgen/service.json')  # Replace with your path
firebase_admin.initialize_app(cred)
db = firestore.client()


def getHistory(username):
    # Reference to the user document in the Firestore
    user_ref = db.collection('users').document(username)
    doc = user_ref.get()

    # If user exists, retrieve history
    if doc.exists:
        history = doc.to_dict().get('history', [])
        return history
    else:
        # If user doesn't exist, create a new user with empty history
        user_ref.set({
            'history': []
        })
        return []


def addMessageAndResponse(username, message, response):
    # Reference to the user document in the Firestore
    user_ref = db.collection('users').document(username)
    doc = user_ref.get()

    # If user exists, retrieve history and add messages
    if doc.exists:
        history = doc.to_dict().get('history', [])
        history.extend([message, response])
        user_ref.update({'history': history})

        return f"Messages added to {username}'s history."

    else:
        # If user doesn't exist, create a new user with the provided messages
        user_ref.set({'history': [message, response]})
        return f"User {username} created and messages added."


def clear_history(username):
    # Reference to the user document in the Firestore
    user_ref = db.collection('users').document(username)
    doc = user_ref.get()
    startmessage = """Reiko: *Every day, {{user}} has to deal with his older sisteer's clumsiness which causes many sexual accidents; today is also no exception.*
    *Reiko runs into {{user}} as she walks down the stairs.* "{{user}}-kun? Already back from scho-" *She trips over her feet and falls down at him.*"""

    # If user exists, clear history
    if doc.exists:
        # Update the user's history in Firestore to an empty list
        user_ref.update({'history': [startmessage]})
        return f"History cleared for {username}."

    else:
        # If user doesn't exist, notify accordingly
        return f"User {username} does not exist. No history to clear."


def addCredits(username, amount):
    user_ref = db.collection('users').document(username)
    doc = user_ref.get()

    # If user exists, add credits to their account
    if doc.exists:
        current_credits = doc.to_dict().get('credits', 0)
        new_credits = current_credits + amount
        user_ref.update({'credits': new_credits})
        return True

    else:
        return False


def getBalance(username):
    # Reference to the user document in the Firestore
    user_ref = db.collection('users').document(username)
    doc = user_ref.get()

    # If user exists, return their credit balance
    if doc.exists:
        current_credits = doc.to_dict().get('credits', 0)
        return current_credits

    else:
        # If user doesn't exist, notify accordingly
        return -20



