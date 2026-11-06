# AX Explained

An interactive, wire-protocol tutorial and 3D isometric architecture visualization for **[Google AX](https://github.com/google/ax)** (`ax.io/v1alpha1`) and **[Agent Substrate](https://github.com/agent-substrate/substrate)** (`v1.0`), inspired by [mcp-explained.com](https://mcp-explained.com/).

Traces every `ax` CLI command, `ax.v1alpha1.AX` gRPC RPC, PostgreSQL token lease (`locks` table), Agent Substrate `ateapi.v1.Control` actor RPC, `atenet-router` mTLS hop (`ate-target-actor`), and in-sandbox `ax-task-runner` (`PID 1`) / loopback metadata (`127.0.0.1:8099`) / guest `ProcessService` interaction step by step.

## Repository Structure

```text
ax-explained/
├── index.html          # Self-contained production HTML bundle (zero runtime dependencies)
├── ax-explained.html   # Symlink to index.html for backward-compatible deep links
├── favicon.svg         # Official Axel axolotl SVG favicon
├── vercel.json         # Vercel static deployment & rewrite configuration
├── package.json        # Build & local dev scripts
├── assets/
│   ├── axel.svg        # Official AX mascot source SVG
│   └── fonts.css       # Embedded Geist, Geist Mono & Fragment Mono woff2 fonts
└── scripts/
    └── build.py        # Deterministic generator that compiles index.html and favicon.svg
```

## Deploy to Vercel

This repository is ready to deploy directly to Vercel with **zero external build dependencies** (`index.html` is pre-built and committed at the root):

### Option 1: Vercel CLI
```bash
cd ~/src/ax-explained
npx vercel          # Deploy preview URL
npx vercel --prod   # Deploy production URL
```

### Option 2: GitHub + Vercel Integration
1. Push this repository to GitHub:
   ```bash
   git remote add origin <your-git-remote-url>
   git push -u origin main
   ```
2. Import the repository at [vercel.com/new](https://vercel.com/new) (Framework Preset: **Other**, Output Directory: `.`).

## Local Development & Rebuilding

### Preview Locally
```bash
python3 -m http.server 3000
# or: npm run dev
```

### Rebuild `index.html` from `scripts/build.py`
After editing lessons, isometric models, or styles in `scripts/build.py`:
```bash
python3 scripts/build.py
# or: npm run build
```
