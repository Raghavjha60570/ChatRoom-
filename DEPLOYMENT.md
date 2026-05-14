# ChatRoom Deployment Guide

## 🚀 Quick Start (Local)

### Prerequisites
- Python 3.7+
- pip

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

Open browser: **http://localhost:5000**

---

## 🌐 Deploy to Production

### Option 1: Railway (Easiest & Fastest)

1. **Create Railway Account**: https://railway.app
2. **Connect GitHub** or upload your files
3. **Create new project** → Select Python
4. **Upload your folder** or link GitHub repo
5. Railway auto-detects and runs it!

**Set environment variable:**
```
PORT=5000
SECRET_KEY=your-random-secret-key-here
```

### Option 2: Heroku

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create your-chatroom-app

# Add Procfile
echo "web: python app.py" > Procfile

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### Option 3: DigitalOcean (VPS)

1. Create droplet (Ubuntu 22.04)
2. SSH into server:
```bash
ssh root@your_droplet_ip

# Update system
apt update && apt upgrade -y

# Install Python & pip
apt install python3 python3-pip git -y

# Clone your repo
git clone your-repo-url
cd ChatRoom

# Install dependencies
pip install -r requirements.txt

# Install supervisor (to keep app running)
apt install supervisor -y

# Create config file
sudo nano /etc/supervisor/conf.d/chatroom.conf
```

Add to the config file:
```ini
[program:chatroom]
directory=/root/ChatRoom
command=/usr/bin/python3 /root/ChatRoom/app.py
autostart=true
autorestart=true
stderr_logfile=/var/log/chatroom.err.log
stdout_logfile=/var/log/chatroom.out.log
```

Then:
```bash
# Start supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start chatroom

# Install Nginx as reverse proxy
apt install nginx -y
```

Edit `/etc/nginx/sites-available/default`:
```nginx
server {
    listen 80 default_server;
    server_name your_domain_or_ip;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Then:
```bash
sudo systemctl restart nginx
```

### Option 4: Replit

1. Go to **https://replit.com**
2. Create new Repl → Python
3. Upload your files
4. Run button automatically starts `app.py`
5. Share public URL

---

## 🔐 Security Tips

1. **Change SECRET_KEY** in `app.py`:
```python
app.config['SECRET_KEY'] = 'use-a-random-secure-key-here'
```

2. **Use environment variables**:
```python
import os
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-key')
```

3. **Add rate limiting** (optional)

4. **Enable HTTPS** on production

---

## 📊 Scaling

- For many users, add Redis for session management
- Use message queues (Celery) for heavy loads
- Configure database to persist messages

---

## 🐛 Troubleshooting

**WebSocket not connecting?**
- Check CORS settings in `app.py`
- Ensure firewall allows WebSocket ports

**Port already in use?**
```bash
lsof -i :5000  # Find what's using port
kill -9 PID    # Kill the process
```

**App crashes after deploy?**
- Check logs: `heroku logs --tail`
- Verify all dependencies in `requirements.txt`

---

Made with ❤️ - Enjoy your chat app!
