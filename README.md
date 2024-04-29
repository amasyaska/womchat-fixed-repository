# womchat backend
## API
### endpoints:
  - ```/send/<int:chat_id>```
    - POST: takes POST request from user (requires cookies) and sends message from this user to given chat_id (adds message record to InstantMessage talbe)
  - ```/chat/<int:chat_id>```
    - GET: returns JSON with all messages in chat by given chat_id (requires cookies) in format: ```{"messages": [message_id, user_id, message_text, date_added]}```
  - ```/chats```
    - GET: returns JSON with all user chats in format: ```{chat_id1: [chat_title, last_message_text], chat_id2: [...}```
  - ```/chats/create_chat/<str:username>```
    - POST: creates chat with user by username
  - ```/resigstration```
    - POST: serializes user to auth_user table (modified standard Django user model)
  - ```/login```
    - POST: used to login user, checks data validity
  - ```/logout```
    - POST: used to logout user
  - ```/delete_user```
    - POST: used to deactivate logout user
  - ```/edit_user```
    - UPDATE: takes request data, checks their validity and updates data in database and updates session hash.
    - GET: returns JSON user data.
## Server setup
### Project scheme:
Client ---> Nginx (reverse proxy) -> Gunicorn (WSGI) -> Django (Application).

## setting up your VPS to run this project
We use Nginx as a reverse proxy, Gunicorn as WSGI, Django as an application server.
1. Install Nginx
```
sudo apt install nginx
```
2. Clone this repository
```
git clone https://github.com/CrazyDuck192/hackathon-project.git
```
3. Set up your virtual environment
```
cd hackathon-project
mkdir .venv
python3 -m venv ./.venv
source ./.venv/bin/activate
pip install -r requirements.txt
```
4. Set up Gunicorn
```
gunicorn -c conf/gunicorn_config.py api.wsgi
```

to be continued...
