# ShieldNet + Supabase Setup

## 1. Create Supabase Project

1. Go to https://supabase.com → **Start new project**
2. Name: `shieldnet`
3. Database password: save this securely
4. Region: closest to you
5. Wait for provisioning (~2 min)

## 2. Run Schema

1. Go to **SQL Editor** → **New query**
2. Paste the contents of `supabase/schema.sql`
3. Click **Run** — this creates all tables, indexes, and views

## 3. Connect SOC API to Supabase

Get your connection string from **Project Settings → Database → Connection string → URI**
It looks like: `postgresql://postgres:YOUR_PASSWORD@db.xxxx.supabase.co:5432/postgres`

Set this as `DATABASE_URL` when running the SOC API.

## 4. Use Supabase REST API (optional, no SOC API needed)

Go to **Project Settings → API** and note:
- **Project URL**: `https://xxxx.supabase.co`
- **anon public key**: `eyJhbGciOiJIUzI1NiIs...`

Then in the dashboard, set `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY`
to query data directly from Supabase.

## 5. Architecture Options

```
Option A (recommended):                       Option B (simpler):
┌─────────────┐    ┌──────────┐              ┌─────────────┐
│ GitHub Pages │───→│ SOC API  │──→ Supabase  │ GitHub Pages │──→ Supabase REST
│ (Dashboard)  │    │ (Render) │   (Postgres)  │ (Dashboard)  │   API
└─────────────┘    └──────────┘              └─────────────┘
```

**Option A** needs a free Render service for the Python SOC API.
**Option B** works with just GitHub Pages + Supabase (no Python needed for reads),
but you lose AIRO, ML inference, and WebSocket alerts.
