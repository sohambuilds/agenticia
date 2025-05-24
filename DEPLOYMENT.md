# 🚀 Deployment Guide: AI Tutor Multi-Agent System

Deploy your Multi-Agent AI Tutor system using Railway for the backend and Vercel for the frontend.

## 📋 Prerequisites

- [Railway Account](https://railway.app) (free tier available)
- [Vercel Account](https://vercel.com) (free tier available)  
- [GitHub Account](https://github.com) for repository hosting
- Google AI API Key (from Google AI Studio)

## 🗂️ Project Structure
```
StealthAI/
├── backend/          # FastAPI Python backend
├── frontend/         # Next.js TypeScript frontend
└── DEPLOYMENT.md     # This guide
```

---

## 🔧 Part 1: Backend Deployment (Railway)

### Step 1: Prepare Your Repository

1. **Push to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

### Step 2: Deploy to Railway

1. **Create Railway Account**: Go to [railway.app](https://railway.app) and sign up
2. **Connect GitHub**: Link your GitHub account to Railway
3. **Create New Project**: 
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Select the `backend` folder as the root directory

### Step 3: Configure Environment Variables

In your Railway project dashboard, go to **Variables** and add:

```bash
# Required
GOOGLE_API_KEY=your_google_ai_api_key_here

# Optional (Railway will auto-assign PORT)
PORT=8000

# Optional: Frontend URL for CORS (will be set after frontend deployment)
FRONTEND_URL=https://your-app-name.vercel.app
```

### Step 4: Configure Deployment Settings

Railway should automatically detect your Python app, but verify:

- **Root Directory**: `/backend`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 5: Deploy

1. Click **Deploy** 
2. Wait for deployment to complete (usually 2-5 minutes)
3. **Copy your Railway URL** (e.g., `https://your-app-name.railway.app`)

### Step 6: Test Backend

Visit your Railway URL to verify:
- `https://your-app-name.railway.app/` → Should show API info
- `https://your-app-name.railway.app/health` → Should return health status

---

## 🎨 Part 2: Frontend Deployment (Vercel)

### Step 1: Prepare Frontend Environment

Create `.env.local` in the `frontend` directory:
```bash
# Replace with your actual Railway URL
NEXT_PUBLIC_API_URL=https://your-backend-app.railway.app
```

### Step 2: Deploy to Vercel

#### Option A: Vercel CLI (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend directory
cd frontend

# Deploy
vercel

# Follow the prompts:
# Set up and deploy? [Y/n] → Y
# Which scope? → Select your account
# Link to existing project? [y/N] → N
# What's your project's name? → ai-tutor-frontend (or your choice)
# In which directory is your code located? → ./
```

#### Option B: Vercel Dashboard
1. Go to [vercel.com](https://vercel.com) and sign in
2. Click **New Project**
3. Import your GitHub repository
4. **Configure**:
   - Framework Preset: **Next.js**
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`

### Step 3: Configure Environment Variables in Vercel

In your Vercel project dashboard:
1. Go to **Settings** → **Environment Variables**
2. Add:
   ```
   NEXT_PUBLIC_API_URL = https://your-backend-app.railway.app
   ```

### Step 4: Update Backend CORS

1. Go back to your Railway project
2. Update the `FRONTEND_URL` environment variable:
   ```
   FRONTEND_URL=https://your-app-name.vercel.app
   ```
3. **Redeploy** your Railway backend

---

## 🔗 Part 3: Final Configuration

### Update CORS in Backend

Your backend `main.py` is already configured, but make sure to replace the placeholder in the CORS origins:

```python
allowed_origins = [
    "http://localhost:3000",  # Local development
    "https://*.vercel.app",   # Vercel preview deployments  
    "https://your-actual-app.vercel.app",  # Replace with your actual Vercel domain
]
```

### Test Full System

1. **Visit your Vercel URL**: `https://your-app-name.vercel.app`
2. **Test the chat interface**:
   - Math: "Calculate 2^8 + sqrt(144)"
   - Physics: "What is the speed of light?"
   - General: "Help me understand calculus"

---

## 🎯 Part 4: Custom Domains (Optional)

### For Vercel (Frontend)
1. **Vercel Dashboard** → **Domains**
2. Add your custom domain
3. Configure DNS records as instructed

### For Railway (Backend)  
1. **Railway Dashboard** → **Settings** → **Domains**
2. Add custom domain
3. Update CORS origins in your backend code

---

## 🔍 Troubleshooting

### Common Issues

#### ❌ CORS Errors
- **Problem**: Frontend can't connect to backend
- **Solution**: Verify `FRONTEND_URL` is set correctly in Railway, and your Vercel domain is in the CORS origins

#### ❌ Environment Variables Not Working
- **Problem**: API key not found
- **Solution**: Check Railway environment variables, make sure `GOOGLE_API_KEY` is set

#### ❌ 500 Server Errors
- **Problem**: Backend crashes
- **Solution**: Check Railway logs in the dashboard for error details

#### ❌ Build Failures
- **Frontend**: Check that `NEXT_PUBLIC_API_URL` is set in Vercel
- **Backend**: Verify all dependencies are in `requirements.txt`

### Checking Logs

**Railway Logs**:
1. Railway Dashboard → Your Project → **Deployments**
2. Click on latest deployment → **View Logs**

**Vercel Logs**:
1. Vercel Dashboard → Your Project → **Deployments**  
2. Click on deployment → **View Function Logs**

---

## 🎉 Success!

Your AI Tutor Multi-Agent System is now live! 

- **Frontend**: `https://your-app-name.vercel.app`
- **Backend**: `https://your-backend-app.railway.app`

### Features Available:
- ✅ **Multi-Agent Routing**: Automatic agent selection
- ✅ **Math Agent**: Calculator with step-by-step solutions
- ✅ **Physics Agent**: Constants, formulas, and calculations
- ✅ **Tutor Agent**: General educational assistance
- ✅ **Dark/Light Mode**: User preference persistence
- ✅ **Responsive Design**: Works on all devices
- ✅ **Real-time Chat**: Instant responses with loading states

---

## 📈 Next Steps

1. **Monitor Usage**: Check Railway and Vercel analytics
2. **Add Analytics**: Implement user tracking (optional)
3. **Custom Domain**: Set up your own domain
4. **Scale**: Upgrade plans as usage grows
5. **Add Features**: Extend with more agents or tools

## 🤝 Support

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **FastAPI Docs**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **Next.js Docs**: [nextjs.org/docs](https://nextjs.org/docs)

Happy coding! 🚀 