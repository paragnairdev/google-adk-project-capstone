# 🏏 VR Cricket Coach - Getting Started

## Quick Launch (3 Seconds)

```bash
./launch_web_ui.sh
```

Open your browser: **http://localhost:8000**

That's it! You now have a ChatGPT-like interface for your cricket coach.

---

## What You Can Do

### 1. Get Personalized Stats
```
You: Hi, I'm Karthik
Coach: Welcome Karthik! Here are your stats...
```

### 2. Get Toss Decisions
```
You: Should I bat or bowl against Sid if I win the toss?
Coach: Based on your data... [recommendation]
```

### 3. Calculate Safe Targets
```
You: What's a safe target against Ragz when batting first?
Coach: Par score: 120, Competitive: 135, Safe: 150...
```

---

## Three Ways to Use It

| Mode | Command | Interface | Best For |
|------|---------|-----------|----------|
| **Web UI** 🌐 | `./launch_web_ui.sh` | Browser chat | Demos, End users |
| **Terminal** 💻 | `python vr_cricket_coach.py --interactive` | Command line | Development |
| **Demo** 📋 | `python vr_cricket_coach.py` | Scripted | Learning |

---

## First Time Setup

1. **Check your virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Verify your API key:**
   ```bash
   cat .env
   # Should show: GOOGLE_API_KEY=...
   ```

3. **Launch:**
   ```bash
   ./launch_web_ui.sh
   ```

---

## Documentation Guide

| File | Purpose | Read When |
|------|---------|-----------|
| **QUICK_START_WEB_UI.md** | Fast reference | You want to launch now |
| **WEB_UI_FIX.md** | Fix details | Had ModuleNotFoundError? Fixed! |
| **WEB_UI_INTEGRATION.md** | Complete overview | You want to understand everything |
| **WEB_UI_GUIDE.md** | Detailed guide | You need configuration/troubleshooting |
| **VR_CRICKET_COACH_GUIDE.md** | Agent architecture | You want to understand the agents |
| **README.md** | Project overview | You want the big picture |

---

## Troubleshooting

### Can't start the web UI?
```bash
# Check if port is in use
lsof -i :8000

# Kill if needed
kill -9 <PID>
```

### API key issues?
```bash
# Create .env file
echo "GOOGLE_API_KEY=your-key-here" > .env
```

### Module errors?
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## What Makes This Special?

✅ **Multi-Agent System**: 4 specialized agents working together  
✅ **Data-Driven**: Real match statistics, not generic advice  
✅ **Memory**: Remembers context across conversations  
✅ **Three Interfaces**: Web, terminal, and demo modes  
✅ **Session Management**: Handles multiple concurrent users  
✅ **Percentile Analysis**: Smart target calculations  

---

## Quick Test

After launching the web UI, try this conversation:

```
You: Hi, I'm Karthik
Coach: [Shows your stats]

You: I'm playing Sid tomorrow. Should I bat or bowl if I win the toss?
Coach: [Analyzes your history vs Sid and provides recommendation]

You: What if I'm batting first? What's a safe target?
Coach: [Calculates percentile-based targets from opponent data]
```

---

## Your System at a Glance

```
You (Browser) → Web UI → Multi-Agent System → Gemini API
                          ├─ Identity Agent
                          ├─ Intent Router
                          ├─ Toss Strategy Agent
                          └─ Root Orchestrator
```

---

## Ready to Go!

**Launch command:**
```bash
./launch_web_ui.sh
```

**URL:**
```
http://localhost:8000
```

**First message:**
```
Hi, I'm [Your Name]
```

---

**Questions?** Check WEB_UI_GUIDE.md or VR_CRICKET_COACH_GUIDE.md

