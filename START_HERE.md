# 🏏 VR Cricket Strategist - Getting Started

## Quick Launch (Web UI)

```bash
./launch_web_ui.sh
```

Open your browser: **http://localhost:8000**

The `adk web` interface will show all available agents in the `agents/` directory.

---

## Setup

1. **Activate your virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Verify your API key:**
   ```bash
   cat .env
   # Should show: GOOGLE_API_KEY=...
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## What You Can Do

### 1. Analyze Pitch Conditions
```
Query: "Analyze a green pitch with overcast conditions for a Test match"
Strategist: [Provides detailed pitch analysis and strategy recommendations]
```

### 2. Get Bowling Change Recommendations
```
Query: "It's the death overs in a T20. Opposition needs 45 runs from 24 balls. What bowling changes should we use?"
Strategist: [Recommends bowling rotations based on match situation]
```

### 3. Calculate DLS Targets
```
Query: "Calculate DLS target if we need to chase 180 in 15 overs instead of 20"
Strategist: [Provides revised target using DLS calculations]
```

---

## Usage

### Web UI (Recommended)
Launch the ADK web interface:
```bash
./launch_web_ui.sh
# Or directly:
python launch_web_ui.py
```
Then open http://localhost:8000 in your browser.

### Run Demo Mode
```bash
python -m agents.vr_cricket_strategist.agent
```

### Run Tests
```bash
pytest agents/vr_cricket_strategist/tests/
```

### Run Tests with Coverage
```bash
pytest agents/vr_cricket_strategist/tests/ --cov=agents/vr_cricket_strategist --cov-report=html
```

---

## Documentation Guide

| File | Purpose |
|------|---------|
| **START_HERE.md** | Quick start guide (you are here) |
| **README.md** | Project overview |
| **agents/vr_cricket_strategist/TEST_SUMMARY.md** | Test coverage and status |

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

### Tests failing?
```bash
# Run tests with verbose output
pytest agents/vr_cricket_strategist/tests/ -v
```

---

## What Makes This Special?

✅ **Web UI**: Modern chat interface with `adk web`  
✅ **Data-Driven**: Uses real match statistics for analysis  
✅ **Comprehensive Tools**: Pitch analysis, DLS calculations, bowling changes  
✅ **Well-Tested**: High test coverage with pytest  
✅ **Flexible**: Works for Test, ODI, and T20 formats  
✅ **Easy to Extend**: Modular architecture for adding new features  

---

## Quick Test

Try running the tests to verify everything is working:

```bash
pytest agents/vr_cricket_strategist/tests/ -v
```

You should see all tests passing with coverage information.

---

## Ready to Go!

**Launch web UI:**
```bash
./launch_web_ui.sh
```

**Open in browser:**
```
http://localhost:8000
```

**Or run tests:**
```bash
pytest agents/vr_cricket_strategist/tests/
```

---

**Questions?** Check README.md or the test files in `agents/vr_cricket_strategist/tests/`

