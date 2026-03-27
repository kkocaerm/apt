# Apartment SaaS MVP

Tek servis deploy:
- FastAPI backend
- Next.js frontend
- Render PostgreSQL
- JWT auth
- Daire / gider / ödeme / davet akışı
- Excel/PDF export

## Hızlı başlangıç

1. `cp .env.example .env`
2. `cp frontend/.env.local.example frontend/.env.local`
3. PostgreSQL bağlantını `.env` içinde ayarla
4. Lokal:
   - `./start_local.sh`

## Render
- `render.yaml` ile deploy et
- Tek web service + ayrı Postgres kullanır

## İlk kurulum
- `/login` ekranında **İlk Kurulum** ile admin oluştur
- Sonra daire ekle, gider gir, ödeme kaydet, davet linki üret
