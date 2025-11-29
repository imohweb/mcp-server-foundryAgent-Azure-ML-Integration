# Pre-Presentation Checklist

## ✅ Before Your Tech Talk

### 24 Hours Before
- [ ] Test the MCP server on your presentation machine
- [ ] Verify all demo curl commands work
- [ ] Take screenshots of key screens (in case of network issues)
- [ ] Prepare backup slides with code snippets
- [ ] Test your microphone and screen sharing

### 1 Hour Before
- [ ] Start the MCP server (`python server.py`)
- [ ] Open browser tabs:
  - [ ] http://localhost:8000/
  - [ ] http://localhost:8000/tools
  - [ ] http://localhost:8000/docs
- [ ] Open VS Code with key files:
  - [ ] `src/mcp_server/main.py`
  - [ ] `src/mcp_server/tools/azure_ml_tools.py`
  - [ ] `src/foundry_agent/bridge.py`
- [ ] Have terminal ready with curl commands
- [ ] Test your screen resolution/zoom level

### Key Files to Have Open
1. Architecture diagram (`docs/diagrams/mcp-foundry-azureml-integration.jpeg`)
2. Implementation guide (`docs/IMPLEMENTATION_GUIDE.md`)
3. Presentation guide (`docs/PRESENTATION_GUIDE.md`)

---

## 🎯 Demo Commands Ready to Copy-Paste

### Test 1: Greet Tool
```bash
curl -X POST http://localhost:8000/mcp/call \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "greet", "parameters": {"name": "Azure NG Community"}}'
```

### Test 2: Add Numbers Tool
```bash
curl -X POST http://localhost:8000/mcp/call \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "add_numbers", "parameters": {"a": 42, "b": 58}}'
```

### Test 3: List Tools
```bash
curl http://localhost:8000/tools
```

---

## 📊 Key Stats to Remember

- **3 Layers**: Intelligence, Integration, Execution
- **5 Tools**: 2 demo + 3 production Azure ML
- **Port 8000**: MCP Server runs here
- **FastAPI**: Powers the HTTP endpoints
- **Python 3.9+**: Minimum version required

---

## 🎤 Opening Lines (Choose One)

**Option 1 (Problem-First):**
"Imagine you're a data scientist, and you want to tell an AI agent: 'Run my ML pipeline with batch size 100.' Sounds simple, right? But how does the agent actually DO that? How does it securely connect to Azure ML? How do we prevent it from doing something dangerous? That's what we're solving today."

**Option 2 (Solution-First):**
"Today I'm going to show you how we built a bridge between Microsoft Foundry Agents and Azure Machine Learning using something called the Model Context Protocol. By the end of this talk, you'll see AI agents triggering real ML workflows with natural language - safely, securely, and at scale."

**Option 3 (Story-Based):**
"Last month, our team was frustrated. We had powerful AI agents, we had enterprise ML systems, but connecting them safely was a nightmare. Custom APIs, security concerns, maintenance headaches. Then we discovered MCP - the Model Context Protocol. Let me show you what we built."

---

## 🎬 Flow Outline

1. **The Problem** (2 min)
   - AI agents can't safely call enterprise systems
   - Custom integrations don't scale
   - Security and governance concerns

2. **The Solution** (3 min)
   - Model Context Protocol (MCP)
   - 3-layer architecture
   - Show architecture diagram

3. **Live Demo** (7 min)
   - Server running at localhost:8000
   - Test demo tools (greet, add_numbers)
   - Show interactive docs
   - Explain Azure ML tools

4. **Code Walkthrough** (5 min)
   - FastAPI server setup
   - Tool routing logic
   - Azure ML bridge
   - Authentication approach

5. **Real-World Impact** (3 min)
   - Use cases
   - Benefits
   - Next steps

6. **Q&A** (10 min)

---

## 🚨 Backup Plans

### If Internet Fails
- Show screenshots of working demos
- Walk through code without running
- Focus on architecture and design decisions

### If Server Won't Start
- Show pre-recorded terminal session
- Use FastAPI docs screenshots
- Focus on code explanation

### If Time Runs Short
- Skip demo tools (greet, add_numbers)
- Focus on Azure ML integration
- Provide GitHub link for details

### If Time Runs Long
- Add more code walkthrough
- Deep dive into authentication
- Discuss deployment strategies

---

## 💬 Engagement Tips

- **Ask Questions**: "How many of you work with ML workflows?"
- **Interactive**: "Let's see what happens when we call this tool..."
- **Relatable**: "We've all had this problem..."
- **Clear Transitions**: "Now that we've seen the demo, let's look at the code..."
- **Visual Aids**: Point to diagram often

---

## 📸 Screenshots to Have Ready (Just in Case)

1. MCP Server homepage (localhost:8000)
2. /tools endpoint response
3. /docs interactive API page
4. Successful greet tool response
5. Azure ML pipeline YAML
6. Architecture diagram

---

## 🎓 Key Takeaways to Emphasize

1. **MCP is a standard protocol** - not vendor-specific
2. **3-layer architecture** - separation of concerns
3. **Security by design** - validated tool boundaries
4. **Production-ready** - real code you can use
5. **Open source** - available on GitHub

---

## ✨ Closing Strong

"So to recap: We've built a secure bridge from Foundry Agents to Azure ML using MCP. We have 3 layers - Intelligence, Integration, and Execution. The code is production-ready, open source, and you can start using it today. I've shared the GitHub repo in the chat. Star it, fork it, customize it for your needs. And if you build something cool with this, please share it back with the community. Thank you!"

---

## 📧 Follow-Up Materials to Share

- GitHub repo link
- Implementation guide link
- Your contact info
- Azure NG Community links
- Related resources

---

## 🎉 You've Got This!

Remember:
- Breathe
- Speak slowly and clearly
- Pause for questions
- Enjoy sharing your work
- The community is supportive!

**Good luck! 🚀**
