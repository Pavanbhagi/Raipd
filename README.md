# Python_series

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Swiftly. | Pavanbhagi</title>
    
    <!-- PWA & SEO -->
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#0071E3">
    
    <!-- External Libraries -->
    <script src="https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/codemirror.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/theme/neo.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/codemirror.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/mode/python/python.min.js"></script>

    <style>
        :root {
            --apple-bg: #F5F5F7;
            --apple-glass: rgba(255, 255, 255, 0.75);
            --apple-border: rgba(0, 0, 0, 0.08);
            --apple-text: #1D1D1F;
            --apple-blue: #0071E3;
            --apple-green: #34C759;
            --apple-red: #FF3B30;
            --apple-dim: #86868b;
        }

        body {
            margin: 0; font-family: -apple-system, sans-serif;
            background-color: var(--apple-bg); color: var(--apple-text);
            scroll-behavior: smooth; overflow-x: hidden;
        }

        #progress-container { position: fixed; top: 0; width: 100%; height: 4px; background: rgba(0,0,0,0.05); z-index: 2001; }
        #progress-bar { width: 0%; height: 100%; background: var(--apple-blue); transition: 0.4s ease; }

        .dock-wrapper { position: fixed; left: 20px; top: 120px; bottom: 40px; width: 70px; z-index: 1000; }
        .dock-container { background: var(--apple-glass); backdrop-filter: blur(30px); border: 1px solid var(--apple-border); border-radius: 22px; padding: 10px; display: flex; flex-direction: column; gap: 12px; overflow-y: auto; max-height: 100%; scrollbar-width: none; }
        .dock-icon { width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-weight: 700; cursor: pointer; transition: 0.3s; background: rgba(0,0,0,0.03); }
        .dock-icon.completed { border: 2px solid var(--apple-blue); background: white; }

        .main-content { margin-left: 140px; max-width: 900px; padding: 0 40px 100px; }

        .apple-card { background: white; border: 1px solid var(--apple-border); border-radius: 24px; padding: 30px; margin-bottom: 40px; box-shadow: 0 4px 24px rgba(0,0,0,0.02); }
        
        /* Agent Console Styles */
        #agent-console { position: sticky; top: 20px; z-index: 100; border: 2px solid var(--apple-blue); transition: border-color 0.3s; }
        #agent-chat-history { max-height: 150px; overflow-y: auto; margin-bottom: 15px; font-size: 0.9rem; color: var(--apple-dim); padding: 10px; background: #FBFBFD; border-radius: 12px; }

        .editor-container { margin-top: 20px; border-radius: 16px; overflow: hidden; border: 1px solid var(--apple-border); }
        .terminal { background: #1c1c1e; color: var(--apple-green); padding: 20px; border-radius: 0 0 16px 16px; font-family: monospace; display: none; }
        
        .apple-btn { background: var(--apple-blue); color: white; border: none; padding: 10px 24px; border-radius: 50px; font-weight: 600; cursor: pointer; transition: 0.3s; }
        .pulse { animation: pulse-animation 2s infinite; }
        @keyframes pulse-animation { 0% { box-shadow: 0 0 0 0px rgba(0, 113, 227, 0.4); } 100% { box-shadow: 0 0 0 15px rgba(0, 113, 227, 0); } }
    </style>
</head>
<body>

<div id="progress-container"><div id="progress-bar"></div></div>

<div class="dock-wrapper">
    <nav class="dock-container" id="side-dock"></nav>
</div>

<main class="main-content">
    <header style="padding: 100px 0 40px;">
        <h1 style="font-size: 3.5rem; margin: 0; letter-spacing: -2px;">Code Swiftly.</h1>
        <p id="engine-status" style="color: var(--apple-dim);">Initializing Python Engine...</p>
    </header>

    <!-- Agentic Assistant Console -->
    <div id="agent-console" class="apple-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <h3 style="margin:0;">Agentic Assistant</h3>
            <span id="agent-status" style="font-size: 0.8rem; font-weight: 600; color: var(--apple-blue);">LISTENING</span>
        </div>
        <div id="agent-chat-history">
            <p><em>"Hello Pavan. I'm monitoring your IDE. If a module crashes, I'll provide a fix here."</em></p>
        </div>
        <div style="display: flex; gap: 10px;">
            <input type="text" id="agent-input" placeholder="Type 'Fix code' or ask a question..." 
                   style="flex-grow: 1; padding: 12px 20px; border-radius: 50px; border: 1px solid var(--apple-border); outline: none;">
            <button class="apple-btn" onclick="askAgent()">Send</button>
        </div>
    </div>

    <div id="master-flow"></div>
</main>

<script>
    // Global State for Agent to monitor
    let globalSystemState = {
        lastError: null,
        currentModuleId: null
    };

    const pythonModules = [
        { id: 1, name: "Introduction", code: "print('Welcome to Code Swiftly.')\nprint('Python is running natively.')" },
        { id: 2, name: "Variable Logic", code: "name = 'Swift'\nprint(f'{name} active.')" },
        // ... (Include Days 3-33 here)
        { id: 33, name: "Parallel Agent Logic", code: "import asyncio\nasync def t1():\n    print('Task started...')\n    await asyncio.sleep(0.5)\nawait t1()" },
        { id: 34, name: "Self-Healing Test", code: "# Try to run this to see the Agent in action\nprint(undefined_variable)" }
    ];

    let pyodide;
    const editors = {};
    const completedModules = new Set();

    async function init() {
        try {
            pyodide = await loadPyodide();
            document.getElementById('engine-status').innerText = "Python 3.11 Wasm Engine Ready";
            document.getElementById('engine-status').style.color = "var(--apple-green)";
            render();
            gsap.from(".apple-card", { opacity: 0, y: 30, duration: 0.8, stagger: 0.1 });
        } catch (e) { document.getElementById('engine-status').innerText = "Engine Load Failed."; }
    }

    function render() {
        const dock = document.getElementById('side-dock');
        const flow = document.getElementById('master-flow');

        pythonModules.forEach(m => {
            const icon = document.createElement('div');
            icon.className = 'dock-icon';
            icon.id = `icon-${m.id}`;
            icon.innerText = m.id;
            icon.onclick = () => document.getElementById(`day-${m.id}`).scrollIntoView({ behavior: 'smooth', block: 'center' });
            dock.appendChild(icon);

            const card = document.createElement('div');
            card.className = 'apple-card';
            card.id = `day-${m.id}`;
            card.innerHTML = `
                <h2 style="margin:0;">Day ${m.id}: ${m.name}</h2>
                <div class="editor-container">
                    <textarea id="edit-${m.id}">${m.code}</textarea>
                    <div style="padding: 12px; background: #fbfbfd; border-top: 1px solid var(--apple-border); text-align: right;">
                        <button class="apple-btn" onclick="runCode(${m.id})">Run Code</button>
                    </div>
                    <div class="terminal" id="term-${m.id}"></div>
                </div>
            `;
            flow.appendChild(card);
            editors[m.id] = CodeMirror.fromTextArea(document.getElementById(`edit-${m.id}`), {
                mode: "python", theme: "neo", lineNumbers: true
            });
        });
    }

    async function runCode(id) {
        const term = document.getElementById(`term-${id}`);
        term.style.display = "block";
        term.innerText = "Running...";
        term.style.color = "var(--apple-green)";
        
        try {
            await pyodide.runPythonAsync(`import sys, io\nsys.stdout = io.StringIO()`);
            await pyodide.runPythonAsync(editors[id].getValue());
            const output = pyodide.runPython("sys.stdout.getvalue()");
            term.innerText = output || "Success: No output.";
            
            completedModules.add(id);
            document.getElementById(`icon-${id}`).classList.add('completed');
            document.getElementById('progress-bar').style.width = (completedModules.size / pythonModules.length * 100) + "%";
            
            // Clear global error if successful
            globalSystemState.lastError = null;
        } catch (e) {
            term.style.color = "var(--apple-red)";
            term.innerText = "Error: " + e.message;
            
            // CAPTURE ERROR FOR AGENT
            globalSystemState.lastError = e.message;
            globalSystemState.currentModuleId = id;
            
            // Trigger Agent UI
            const history = document.getElementById('agent-chat-history');
            history.innerHTML += `<p style="color: var(--apple-red);"><strong>Alert:</strong> Crash detected in Day ${id}. I have a fix ready.</p>`;
            document.getElementById('agent-console').classList.add('pulse');
            history.scrollTop = history.scrollHeight;
        }
    }

    async function askAgent() {
        const input = document.getElementById('agent-input');
        const history = document.getElementById('agent-chat-history');
        const query = input.value.trim().toLowerCase();
        
        if (query === "" && !globalSystemState.lastError) return;

        history.innerHTML += `<p style="color: var(--apple-text);"><strong>You:</strong> ${query || "Fix current error"}</p>`;
        
        // Agent Reasoning Logic
        setTimeout(() => {
            let response = "";
            if (globalSystemState.lastError) {
                if (globalSystemState.lastError.includes("is not defined")) {
                    response = "Reasoning: NameError found. You are using a variable before defining it. Ensure all variables are assigned values first.";
                } else if (globalSystemState.lastError.includes("syntax")) {
                    response = "Reasoning: SyntaxError found. Check for missing colons (:) or mismatched parentheses.";
                } else {
                    response = "Reasoning: I've analyzed the Traceback. Check the logic in the active module.";
                }
                document.getElementById('agent-console').classList.remove('pulse');
                globalSystemState.lastError = null; // Reset after fix
            } else {
                response = "I am monitoring the system. No active errors to fix. How can I help with your Python modules?";
            }
            
            history.innerHTML += `<p style="color: var(--apple-blue);"><strong>Agent:</strong> ${response}</p>`;
            history.scrollTop = history.scrollHeight;
        }, 600);
        
        input.value = '';
    }

    inti()
</script>
</body>
</html>