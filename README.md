Step by step

1) projectni github dan yuklab olamiz

    1. **public** project bolsa -
    ```git
    git clone https://github.com/xolmomin/django_cicd_project.git project1
    ```

    2. **private** project bolsa - git config qilish kk

git config qilish uchun

```git
git config --global user.name "Botir"
git config --global user.email="botir@mail.ru"
```

git config qilganimizni tekshirish uchun

```git
ssh -T git@github.com
```

2) project _**/var/www**_ papka ichida bolishi kerak project uchun _service_ va _nginx_ fayllarini yozish kk

`/etc/systemd/system/project1.service` ichida quyidagilar kodni yozamiz.

```
[Unit]
Description=Django CI/CD project daemon
After=network.target

[Service]
WorkingDirectory=/var/www/project1/backend
ExecStart=/var/www/project1/backend/.venv/bin/gunicorn --workers 1 --bind unix:/var/www/project1/backend/backend.sock root.wsgi:application

[Install]
WantedBy=multi-user.target

```

service ni ishga tushirish

`systemctl enable project1.service`

`systemctl start project1.service`

service ni tekshirish

`systemctl status project1.service`

service ni qayta ishga tushirish

`systemctl restart project1.service`

nginx faylni birinchi available papka ichida yaratamiz, keyin uni enabled ga soft link qilamiz

`ln -s /etc/nginx/sites-available/project1 /etc/nginx/sites-enabled/`

`/etc/nginx/sites-available/project1` fayl ichidagi kodlar

```nginx configuration
server {
    listen       8003;
    server_name  146.190.85.59;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root /var/www/project1/backend;
    }

    location /media/ {
        root /var/www/project1/backend;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/project1/backend/backend.sock;
    }
}
```

nginx fayllarini test qilish
`nginx -t`

va oxirida

`systemctl restart nginx.service`

3) ssh-key generate qilish

```shell
ssh-keygen -t rsa -b 4096 -C "test@gmail.com"
```

generate qilganimizdan keyin 2ta fayl yaratiladi, manzili (/root/.ssh/id_rsa)

**id_rsa.pub** - bu public key

**id_rsa** - bu secret key

Agar ssh-key ni generate qilganimizda, o'zimiz nom bersak (ya'ni id_rsa defaultdagi nom bo'lmasa)

`~/.ssh/config` faylga shu kodni qo'shish kerak

```config
Host github.com
HostName github.com
User git
IdentityFile ~/.ssh/id_custom_rsa
IdentityFile ~/.ssh/id_custom2_rsa
```

4) github actionda appleboy/ssh-action@v0.1.10 dan foydalanamiz, va server hostini, username va passwordini githubdagi
   project **_settings_** ->  **_Secrets and variables_** -> **_Actions_** shu yerga qoshamiz

Agar project githubda private turgan bo'lsa, serverdagi ssh-key bilan generate qilingan **.pub** keyni githubdagi  *
*_settings_** ->  **_Deploy keys_** -> shu yerga qoshamiz 

```github actions
host: ${{ secrets.HOST }}
username: ${{ secrets.USERNAME }}
password: ${{ secrets.PASSWORD }}
```
