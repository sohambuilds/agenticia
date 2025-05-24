# 🚀 Quick Deployment Checklist

## Before Deployment
- [ ] Push code to GitHub
- [ ] Have Google AI API key ready
- [ ] Create Railway account
- [ ] Create Vercel account

## Backend (Railway)
- [ ] Connect GitHub to Railway
- [ ] Create new project from repository
- [ ] Set root directory to `/backend`  
- [ ] Add environment variables:
  - [ ] `GOOGLE_API_KEY=your_api_key`
  - [ ] `FRONTEND_URL=https://your-app.vercel.app` (add after frontend deployment)
- [ ] Deploy and copy Railway URL
- [ ] Test endpoints: `/` and `/health`

## Frontend (Vercel)
- [ ] Create `.env.local` with `NEXT_PUBLIC_API_URL=https://your-app.railway.app`
- [ ] Deploy via CLI (`vercel`) or Dashboard
- [ ] Set root directory to `/frontend`
- [ ] Add environment variable in Vercel dashboard:
  - [ ] `NEXT_PUBLIC_API_URL=https://your-backend.railway.app`
- [ ] Copy Vercel URL

## Final Steps
- [ ] Update Railway `FRONTEND_URL` with Vercel URL
- [ ] Update `main.py` CORS origins with actual Vercel domain
- [ ] Redeploy Railway backend
- [ ] Test full system functionality

## Test Scenarios
- [ ] Math: "Calculate 2^8 + sqrt(144)"
- [ ] Physics: "What is the speed of light?"
- [ ] General: "Help me understand calculus"
- [ ] Dark/Light mode toggle
- [ ] Responsive design on mobile

## URLs to Save
- **Frontend**: https://your-app.vercel.app
- **Backend**: https://your-backend.railway.app
- **Railway Dashboard**: https://railway.app/dashboard
- **Vercel Dashboard**: https://vercel.com/dashboard 