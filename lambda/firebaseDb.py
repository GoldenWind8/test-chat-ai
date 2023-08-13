import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase app
cred = credentials.Certificate('service.json')  # Replace with your path
firebase_admin.initialize_app(cred)

db = firestore.client()


def retrieve_validate_history2(username):
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
            'history': ["Hi"]
        })
        return []


def add_messages_to_history(username, message1, message2):
    # Reference to the user document in the Firestore
    user_ref = db.collection('users').document(username)
    doc = user_ref.get()

    # If user exists, retrieve history and add messages
    if doc.exists:
        history = doc.to_dict().get('history', [])
        history.extend([message1, message2])
        user_ref.update({'history': history})

        return f"Messages added to {username}'s history."

    else:
        # If user doesn't exist, create a new user with the provided messages
        user_ref.set({'history': [message1, message2]})
        return f"User {username} created and messages added."