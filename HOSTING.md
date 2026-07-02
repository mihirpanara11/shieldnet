# ShieldNet Free Hosting Guide

## Step 1: GitHub Pages — Dashboard ✅ (Already Set Up)

1. Go to https://github.com/mihirpanara11/shieldnet/settings/pages
2. Under **Source**, select **GitHub Actions**
3. Done — after each push to `main`, your dashboard deploys to:
   **https://mihirpanara11.github.io/shieldnet/**

---

## Step 2: Supabase — Database (5 min)

1. Go to https://supabase.com → **Start your project**
2. Sign in with GitHub
3. Click **New project**
   - Name: `shieldnet`
   - Database Password: create and **save it**
   - Region: pick the closest
   - Pricing Plan: **Free**
4. Wait ~2 min for provisioning
5. Go to **SQL Editor** → **New query**
6. Copy-paste the entire content of `supabase/schema.sql` from your repo
7. Click **Run**
8. Go to **Project Settings → Database → Connection string → URI**
   - Copy this: `postgresql://postgres:YOUR_PASSWORD@db.xxxx.supabase.co:5432/postgres`
   - This is your `DATABASE_URL`

---

## Step 3: Fly.io — SOC API (10 min)

Fly.io gives 3 free always-on VMs. We'll deploy the SOC API there.

### 3a. Install Fly CLI

**Windows (PowerShell):**
```powershell
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

**Mac/Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

### 3b. Sign up and launch

```bash
# Login (opens browser)
fly auth signup

# Navigate to project
cd C:\Users\ASUS\Desktop\ShieldNet1

# Launch SOC API
fly launch --name shieldnet-soc-api --region ord --no-deploy

# Set secrets (use your Supabase password)
fly secrets set DATABASE_URL="postgresql://postgres:YOUR_PASSWORD@db.xxxx.supabase.co:5432/postgres"

# Deploy
fly deploy
```

Your SOC API is now live at: `https://shieldnet-soc-api.fly.dev`

### 3c. Update dashboard to use it

In your GitHub repo, go to **Settings → Secrets and variables → Actions → New repository secret**:

- Name: `VITE_API_URL`
- Value: `https://shieldnet-soc-api.fly.dev/api/v1`

Then the CI workflow will inject this into the dashboard build.

---

## Step 4: Render — Agent API (optional, 5 min)

1. Go to https://render.com → Sign up with GitHub
2. Click **New + → Web Service**
3. Connect your GitHub repo: `mihirpanara11/shieldnet`
4. Configure:
   - **Name:** `shieldnet-agent-api`
   - **Runtime:** `Python 3.11`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn agent_api.main:app --host 0.0.0.0 --port 10000`
   - **Plan:** **Free**
5. Add Environment Variable:
   - `JWT_SECRET`: `choose-a-random-string`
6. Click **Create Web Service**
7. URL: `https://shieldnet-agent-api.onrender.com`

---

## Final Architecture

```
Browser ─→ https://mihirpanara11.github.io/shieldnet/  (GitHub Pages)
                │
                ▼
        https://shieldnet-soc-api.fly.dev/api/v1        (Fly.io — always-on)
                │
                ▼
        postgresql://...@db.xxxx.supabase.co:5432       (Supabase — free Postgres)
```

**Total cost: $0/month**
- GitHub Pages: free, always-on
- Fly.io: free, always-on (no sleeping)
- Supabase: free, always-on (500MB)
- Render: free (sleeps after 15 min — fine for edge agent)
