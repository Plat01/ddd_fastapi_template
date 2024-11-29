# DDD oAuth2.0
It is jjust example of project with oAuth2.0 on DDD architecture.

## Crate ssl cert
```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ./ssl/key.pem -out ./ssl/cert.pem
```

## start app
```
cp .env.example .env
docker compose up --build
```
