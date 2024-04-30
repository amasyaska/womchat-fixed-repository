# womchat backend
## API
### endpoints:
  - ```/chats/<int:chat_id>/send/```
    - POST: takes POST request from user (requires cookies) and sends message from this user to given chat_id (adds message record to InstantMessage table)
  - ```/chats/<int:chat_id>/```
    - GET: returns JSON with all messages in chat by given chat_id (requires cookies) in format: ```{"messages": [{"id": chat_id, "text": message_text, "timestamp": date_added, "username": username, "is_own": is_own}, {...}]}```
  - ```/chats/```
    - GET: returns JSON with all user chats in format: ```"{chats": [{"id": chat_id, "title": chat_title, "chat_type": chat_type, "last_message": last_message}, {...}]}```
  - ```/chats/create/```
    - POST: creates chat with user by given username with given title and chat_type
  - ```/resigstration/```
    - POST: serializes user to auth_user table (modified standard Django user model)
  - ```/login/```
    - POST: used to login user, checks data validity
  - ```/logout/```
    - POST: used to logout user
  - ```/user/delete/```
    - POST: used to deactivate logout user
  - ```/user/edit/```
    - UPDATE: takes request data, checks their validity and updates data in database and updates session hash.
    - GET: returns JSON user data in format: ```{"username": username, "email": email, "special_mode": special_mode}```.
  - ```/user/info/```
    - GET: returns JSON user data in format: ```{"username": username, "email": email, "special_mode": special_mode}```.
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

## set up SSL on Nginx
1. Change /nginx/Dockerfile:
   ```COPY ./http.conf /etc/nginx/conf.d/default.conf``` to ```COPY ./https.conf /etc/nginx/conf.d/default.conf```
2. Add your certificate to:
  ```/etc/nginx/ssl/your_cert.crt``` (! your certificate have to be named your_cert.crt)
3. Add your key to:
  ```/etc/nginx/ssl/your_key.key``` (! your key have to be named your_cert.crt)
4. Enjoy
