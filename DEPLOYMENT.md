# Deployment Guide: Vercel + Railway

## Prerequisites
- GitHub account (for both services)
- Railway account (https://railway.app)
- Vercel account (https://vercel.com)

## Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Krova referral system"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/referralsystem.git
git push -u origin main
```

## Step 2: Deploy Backend to Railway

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub"
4. Choose your repository
5. Railway will auto-detect it's a Python project

### Configure Environment Variables in Railway

Go to Variables tab and add:

```
GMAIL_ADDRESS=creativecreditai@gmail.com
GMAIL_APP_PASSWORD=your_app_password
FRONTEND_URL=your_vercel_url (add after frontend is deployed)
CORS_ORIGINS=your_vercel_url
```

### Add PostgreSQL Database

1. Click "New Service"
2. Select "Database"
3. Choose PostgreSQL
4. Railway automatically sets `DATABASE_URL`

## Step 3: Deploy Frontend to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Select "Other" as framework
5. Build command: `cd frontend && npm run build`
6. Output directory: `frontend/dist`
7. Root directory: `.`

### Configure Frontend Environment

In Vercel dashboard → Settings → Environment Variables:

```
VITE_API_BASE_URL=https://your-railway-backend.railway.app/api
```

## Step 4: Update Backend CORS

After Vercel deployment, add frontend URL to Railway environment:

```
CORS_ORIGINS=https://your-vercel-url.vercel.app
FRONTEND_URL=https://your-vercel-url.vercel.app
```

Redeploy backend on Railway (it will auto-trigger or you can click Deploy).

## Step 5: Test

1. Visit your Vercel frontend URL
2. Create a referral link
3. Test signup with referral link
4. Check Gmail for emails

## Production Checklist

- [ ] GitHub repo created
- [ ] Railway PostgreSQL database connected
- [ ] Railway backend deployed
- [ ] Vercel frontend deployed
- [ ] Environment variables set in both services
- [ ] CORS origins updated
- [ ] Gmail app password configured
- [ ] Tested signup flow end-to-end

## Troubleshooting

### Backend returns 400
- Check Railway logs: `railway logs`
- Verify DATABASE_URL is set
- Ensure PostgreSQL database is running

### Frontend can't reach backend
- Check VITE_API_BASE_URL in Vercel
- Verify CORS_ORIGINS in Railway includes your Vercel URL
- Check browser console for CORS errors

### Emails not sending
- Verify GMAIL_ADDRESS and GMAIL_APP_PASSWORD
- Check spam folder
- Review Railway logs for email errors

## Scaling

- Railway: Upgrade plan for more resources
- Vercel: Automatically scales, no action needed
- Database: Add read replicas if needed on Railway

## Custom Domain

### For Backend (optional)
- In Railway, go to Settings
- Add custom domain
- Update DNS records

### For Frontend (Vercel)
- In Vercel Settings → Domains
- Add your domain
- Update DNS records

## Local Development After Deployment

For local testing, keep using:
```bash
uvicorn main:app --reload  # Backend
npm run dev  # Frontend
```

Environment variables will use `.env` file locally.
