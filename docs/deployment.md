# Deployment Guide

## 1) Backend deployment (FastAPI)
1. Build Docker image.
2. Deploy to Render/Fly.io/AWS ECS.
3. Set env vars: `OPENAI_API_KEY`, `OPENAI_MODEL`, `MONGODB_URI`, `MONGODB_DB`.
4. Add health check route `/health`.

## 2) Frontend deployment (Vite)
1. Build static app: `npm run build`.
2. Deploy to Vercel/Netlify.
3. Set `VITE_API_BASE_URL` to backend URL.

## 3) Database
- Use MongoDB Atlas cluster.
- Configure IP access and DB user credentials.
- Enable backups + monitoring.

## 4) Production hardening
- Add API auth (JWT/session).
- Rate limiting and abuse detection.
- Centralized logging and metrics.
- CI/CD with lint/test/build gates.
