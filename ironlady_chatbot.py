from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# === Dataset ===
PROGRAMS = [
    {
        "program_id": "P001",
        "program_name": "Leadership Essentials Program",
        "duration": "4 weeks (incl. 2 full-day sessions)",
        "mode": "Online",
        "certification": "Certificate of completion",
        "mentors_coaches": ["Program faculty", "Guest leaders / coaches"]
    },
    {
        "program_id": "P002",
        "program_name": "100 Board Members Program",
        "duration": "6 months (online cohort)",
        "mode": "Online",
        "certification": "Certificate of completion; membership benefits",
        "mentors_coaches": ["Senior leaders", "Board coaches"]
    },
    {
        "program_id": "P003",
        "program_name": "2-Day Leadership Masterclass",
        "duration": "2 days (short masterclass / workshop)",
        "mode": "Online or Live workshops (batch dependent)",
        "certification": "Certificate of participation",
        "mentors_coaches": ["Program faculty", "Guest leaders"]
    }
]

# === HTML Frontend ===
PAGE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Iron Lady FAQ Chatbot</title>
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, sans-serif;
      background: linear-gradient(135deg, #667eea, #764ba2);
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    .container {
      background: #fff;
      width: 450px;
      max-width: 90%;
      border-radius: 16px;
      box-shadow: 0 6px 20px rgba(0,0,0,0.2);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
    .header {
      background: #4c51bf;
      color: white;
      padding: 16px;
      text-align: center;
      font-size: 18px;
      font-weight: bold;
    }
    .chat {
      flex: 1;
      padding: 16px;
      overflow-y: auto;
      background: #f9f9fb;
    }
    .msg {
      margin: 10px 0;
      display: flex;
    }
    .user {
      justify-content: flex-end;
    }
    .bot {
      justify-content: flex-start;
    }
    .bubble {
      padding: 10px 14px;
      border-radius: 18px;
      max-width: 70%;
      word-wrap: break-word;
    }
    .user .bubble {
      background: #667eea;
      color: #fff;
      border-bottom-right-radius: 4px;
    }
    .bot .bubble {
      background: #e5e7eb;
      color: #111;
      border-bottom-left-radius: 4px;
    }
    .controls {
      display: flex;
      border-top: 1px solid #ddd;
    }
    input {
      flex: 1;
      padding: 14px;
      border: none;
      font-size: 15px;
      outline: none;
    }
    button {
      background: #667eea;
      color: white;
      border: none;
      padding: 14px 18px;
      cursor: pointer;
      transition: background 0.3s;
    }
    button:hover {
      background: #5a67d8;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">Iron Lady FAQ Chatbot</div>
    <div id="chat" class="chat"></div>
    <div class="controls">
      <input id="q" placeholder="Type your question...">
      <button onclick="send()">Send</button>
    </div>
  </div>

<script>
async function send(){
  const q=document.getElementById('q').value.trim();
  if(!q) return;
  addMsg(q,'user');
  document.getElementById('q').value='';
  const resp = await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({q:q})});
  const data = await resp.json();
  addMsg(data.answer,'bot');
}

function addMsg(text,who){
  const chat=document.getElementById('chat');
  const div=document.createElement('div');
  div.className='msg '+who;
  const bubble=document.createElement('div');
  bubble.className='bubble';
  bubble.innerHTML=text.replace(/\\n/g,'<br>');
  div.appendChild(bubble);
  chat.appendChild(div);
  chat.scrollTop=chat.scrollHeight;
}

// Allow pressing Enter to send
document.getElementById('q').addEventListener("keypress", function(e) {
  if(e.key==="Enter"){ send(); }
});
</script>
</body>
</html>
"""


# === Logic to answer questions ===
def find_answer(q: str) -> str:
    t = q.lower()
    if "programs" in t:
        return "\n".join([f"- {p['program_name']}" for p in PROGRAMS])
    if "duration" in t:
        return "\n".join([f"- {p['program_name']}: {p['duration']}" for p in PROGRAMS])
    if "online" in t or "offline" in t or "mode" in t:
        return "\n".join([f"- {p['program_name']}: {p['mode']}" for p in PROGRAMS])
    if "certificate" in t or "certificates" in t:
        return "\n".join([f"- {p['program_name']}: {p['certification']}" for p in PROGRAMS])
    if "mentor" in t or "coach" in t:
        return "\n".join([f"- {p['program_name']}: {', '.join(p['mentors_coaches'])}" for p in PROGRAMS])
    return "Sorry, I can only answer about programs, duration, mode, certificates, or mentors."

@app.route('/')
def index():
    return render_template_string(PAGE)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    q = data.get('q','')
    return jsonify({"answer": find_answer(q)})

if __name__ == "__main__":
    app.run(debug=True)

