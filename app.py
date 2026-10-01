from flask import Flask, render_template, request, jsonify
from datetime import datetime
import threading, time, uuid

app = Flask(__name__)

AGENTS = [
    {"id":"anies","name":"Anies","role":"Studio Manager","icon":"🧠"},
    {"id":"luhut","name":"Luhut","role":"Project Coordinator","icon":"📅"},
    {"id":"bahlil","name":"Bahlil","role":"Economic Research","icon":"📈"},
    {"id":"gibran","name":"Gibran","role":"Design Trend Scout","icon":"🔭"},
    {"id":"purbaya","name":"Purbaya","role":"Design × Business","icon":"💰"},
    {"id":"kdm","name":"KDM","role":"Reference Curator","icon":"🖼️"},
    {"id":"megachan","name":"Mega-chan","role":"Wild Card Creative","icon":"✨"},
    {"id":"jonan","name":"Jonan","role":"Technical Director","icon":"📐"},
    {"id":"prabowo","name":"Prabowo","role":"Devil's Advocate","icon":"❓"},
    {"id":"jokowi","name":"Jokowi","role":"Presentation Director","icon":"🎬"},
]

state = {
    "project": None,
    "phase": "IDLE",
    "progress": 0,
    "agents": {a["id"]:{"status":"IDLE","task":"Waiting for project"} for a in AGENTS},
    "logs": [],
    "outputs": {},
    "approval_required": False,
    "approved": False,
}
lock = threading.Lock()

def log(msg):
    with lock:
        state["logs"].append({"time":datetime.now().strftime("%H:%M:%S"),"message":msg})
        state["logs"] = state["logs"][-80:]

def set_agent(aid,status,task):
    with lock:
        state["agents"][aid] = {"status":status,"task":task}

def fake_work(aid, task, seconds, output):
    set_agent(aid,"WORKING",task); log(f"{aid.title()} started: {task}")
    time.sleep(seconds)
    with lock: state["outputs"][aid] = output
    set_agent(aid,"DONE",task); log(f"{aid.title()} completed its assignment")

def run_project(brief):
    with lock:
        state["phase"]="PLANNING"; state["progress"]=5
    fake_work("luhut","Break brief into workstreams",1.5,
              "Research → synthesis → creative/technical review → challenge → principal approval → presentation")
    with lock: state["progress"]=15; state["phase"]="RESEARCH"

    jobs = [
      ("bahlil","Find relevant economic/customer context",2.3,"Economic context mapped to customer demand and spending behaviour."),
      ("gibran","Scan current design and retail trends",2.8,"Trend scan: experiential retail, adaptable displays, tactile interaction and hybrid physical/digital storytelling."),
      ("purbaya","Map design decisions to business value",2.5,"Value map: attention → dwell time → interaction → conversion; test CAPEX against commercial purpose."),
      ("kdm","Curate reference directions",2.0,"Reference buckets: installation, hospitality-style retail, modular display, art-led product staging."),
    ]
    threads=[]
    for args in jobs:
        t=threading.Thread(target=fake_work,args=args); t.start(); threads.append(t)
    for t in threads: t.join()
    with lock: state["progress"]=48; state["phase"]="SYNTHESIS"

    fake_work("anies","Synthesize research into design intelligence",2.2,
              "Design Intelligence: create a destination, make products understandable in context, preserve operational clarity, and give every visual move a business reason.")
    with lock: state["progress"]=60; state["phase"]="DESIGN REVIEW"

    t1=threading.Thread(target=fake_work,args=("megachan","Generate an unexpected design angle",2.2,"Wild-card direction: treat the showcase as a changing scene/event rather than a static product display."))
    t2=threading.Thread(target=fake_work,args=("jonan","Check technical feasibility and detailing implications",2.4,"Technical review: prioritize modular build-up, service access, realistic spans, lighting maintenance and repeatable details."))
    t1.start();t2.start();t1.join();t2.join()
    with lock: state["progress"]=75

    fake_work("prabowo","Challenge assumptions with basic but uncomfortable questions",1.8,
              "Challenge: Why should someone stop? Why enter? What changes if the hero feature disappears? Which assumption is supported by evidence?")
    fake_work("anies","Reconcile conflicts and prepare principal decision",1.5,
              "Recommendation package prepared: aligned evidence, creative opportunity, technical constraints and unresolved decisions.")
    with lock:
        state["phase"]="PRINCIPAL APPROVAL"; state["progress"]=88; state["approval_required"]=True
    log("Office is waiting for Principal approval")

    while True:
        time.sleep(.5)
        with lock:
            if state["approved"]: break
    with lock: state["approval_required"]=False; state["phase"]="PRESENTATION"
    fake_work("jokowi","Turn approved direction into presentation scenario",2.4,
              "Presentation arc: Problem → Opportunity → Big Idea → Customer Scenario → Design System → Technical Logic → Business Value → Next Decision.")
    with lock: state["progress"]=100; state["phase"]="DONE"
    log("Project cycle completed")

@app.route('/')
def index(): return render_template('index.html', agents=AGENTS)

@app.route('/api/state')
def get_state():
    with lock: return jsonify(state)

@app.route('/api/start',methods=['POST'])
def start():
    brief=request.json.get('brief','').strip()
    if not brief: return jsonify({"error":"Brief required"}),400
    with lock:
        state.update({"project":{"id":str(uuid.uuid4())[:8],"brief":brief},"phase":"STARTING","progress":1,"logs":[],"outputs":{},"approval_required":False,"approved":False})
        state["agents"]={a["id"]:{"status":"IDLE","task":"Waiting for assignment"} for a in AGENTS}
    log("Principal submitted a new project brief")
    threading.Thread(target=run_project,args=(brief,),daemon=True).start()
    return jsonify({"ok":True})

@app.route('/api/approve',methods=['POST'])
def approve():
    with lock: state["approved"]=True
    log("Principal approved the direction")
    return jsonify({"ok":True})

if __name__=='__main__': app.run(debug=True, port=5050, threaded=True)
