🍾 Bottle Game — Social Message Game API (Django REST Framework)

A fun social messaging game built with Django REST Framework.
Players send secret messages, collect random bottles, make friends, and use coins to unlock new features.

🚀 Features
👤 User System

Each player has a UserProfile linked to Django’s User

Players have:

coins 💰 (in-game currency)

is_active, is_ban, and ban_until fields

Admins can ban users temporarily or permanently using a dedicated API

💌 Message System

Players can send messages into the “sea” 🌊

Sending a message costs 10 coins

Messages are anonymous until purchased

🏝️ Sea (Bottle Mechanic)

Each message floats in the “sea” until a random player finds it

Players can “pick up” a random message — one they didn’t send

The message becomes marked as is_read=True and assigned to a receiver

🪙 Message Purchase

Players can spend 30 coins to discover who sent a message

Once purchased, the sender’s username becomes visible

👯 Friend System

Players can:

Add friends (costs 50 coins)

Remove friends

View their friend list

Each user has a personal FriendList

🔔 Notifications

Notifications are created when messages are sent or purchased

Includes sender, receiver, and related message

🧑‍💼 Admin Controls

Admins can ban users for a specific number of days or permanently

Supports:

⛔ Permanent ban

⏳ Temporary ban (by days)

✅ Unban

🧠 Game Logic Flow

1️⃣ User sends a message

Costs 10 coins

Message enters the “sea” (unassigned)

2️⃣ Another user picks a bottle

Receives a random message from the sea

Message becomes is_read=True and receiver is assigned

3️⃣ User buys sender info

Costs 30 coins

Reveals who the sender was

4️⃣ User adds a friend

Costs 50 coins

Adds the other player to their friend list

5️⃣ Admin can ban/unban users

Temporary or permanent

Ban logic handled through /admin/ban/ endpoint

🧰 API Endpoints
Method	Endpoint	Description	Permission
GET	/users/	List all users	Admin
POST	/messages/	Send a message (cost: 10 coins)	Authenticated
GET	/sea/	Pick a random message from the sea	Authenticated
POST	/message/<id>/purchase/	Reveal sender info (cost: 30 coins)	Authenticated
POST	/friends/add/	Add a friend (cost: 50 coins)	Authenticated
POST	/friends/remove/	Remove a friend	Authenticated
POST	/admin/ban/	Ban, unban, or permanently ban a user	Admin
🔐 Example Requests
📩 Send a message
{
  "text_message": "Hello from the sea!"
}

🌊 Pick a random bottle

Response:

{
  "id": 5,
  "sender": "Anonymous",
  "text_message": "Hey there!"
}

💰 Purchase sender info

Response:

{
  "receiver": "ramin_user"
}

👯 Add a friend
{
  "username": "alex_dev"
}

🧰 Tech Stack
Tool	Purpose
🐍 Python	Backend
🦄 Django	Web Framework
⚙️ Django REST Framework	API
🗃️ SQLite	Database
🧪 Postman	API Testing
