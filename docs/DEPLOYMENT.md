# TerraNexus Production Deployment Guide

This guide details deploying TerraNexus to production environments using **Gunicorn**, **Nginx**, and **MySQL 8.0+** with HTTPS.

---

## 1. System Requirements

- **OS**: Ubuntu 22.04 LTS / Debian 12 / Rocky Linux 9
- **Python**: 3.10+ (Python 3.12 recommended)
- **Database**: MySQL 8.0+
- **Reverse Proxy**: Nginx
- **WSGI Server**: Gunicorn

---

## 2. Server Setup

```bash
# Update and install system dependencies
sudo apt update && sudo apt install -y python3-pip python3-venv nginx mysql-server certbot python3-certbot-nginx

# Clone repository
git clone https://github.com/msunil06/TerraNexus.git /var/www/terranexus
cd /var/www/terranexus

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

---

## 3. Production Configuration

Create `/var/www/terranexus/.env`:

```ini
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=generate_a_secure_random_hex_key_here
MYSQL_USER=terranexus_user
MYSQL_PASSWORD=StrongProductionPassword123!
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DB=terranexus_db
DATABASE_URL=mysql+pymysql://terranexus_user:StrongProductionPassword123!@127.0.0.1:3306/terranexus_db?charset=utf8mb4
SESSION_COOKIE_SECURE=True
```

Initialize database tables and seed:

```bash
python database/seed_data.py
```

---

## 4. Systemd Service

Create `/etc/systemd/system/terranexus.service`:

```ini
[Unit]
Description=TerraNexus Flask Gunicorn Service
After=network.target mysql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/terranexus
Environment="PATH=/var/www/terranexus/venv/bin"
ExecStart=/var/www/terranexus/venv/bin/gunicorn --workers 4 --bind unix:/var/www/terranexus/terranexus.sock -m 007 "app:create_app()"
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable terranexus
sudo systemctl start terranexus
```

---

## 5. Nginx Configuration

Create `/etc/nginx/sites-available/terranexus`:

```nginx
server {
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /var/www/terranexus;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/terranexus/terranexus.sock;
    }
}
```

Enable the site and obtain SSL with Let's Encrypt:

```bash
sudo ln -s /etc/nginx/sites-available/terranexus /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```
