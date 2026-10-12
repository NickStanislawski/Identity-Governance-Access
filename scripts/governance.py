"""Synthetic identity governance lab. Python standard library only."""
import argparse, csv, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

def stamp(): return datetime.now(timezone.utc).isoformat()
def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2), encoding='utf-8')
def load(path): return json.loads(path.read_text(encoding='utf-8'))
def digest(value): return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()

def fixture():
    departments=['Finance','HR','IT','Sales','Operations']
    apps=['Ledger','People','Directory','CRM','ServiceDesk']
    identities=[dict(id=f'U{i:03}',department=departments[(i-1)%5],manager=f'M{(i-1)%5}',active=i!=60,last_login_days=120 if i==59 else 10) for i in range(1,61)]
    entitlements=[dict(id=f'{app}:{role}',application=app,role=role,owner=f'M{j}',privileged=role=='admin') for j,app in enumerate(apps) for role in ['reader','editor','requester','approver','admin']]
    assignments=[dict(id=f'A{i:03}',identity=f'U{i:03}',entitlement=f'{apps[(i-1)%5]}:reader') for i in range(1,61)]
    for uid,ent in [('U001','Ledger:requester'),('U001','Ledger:approver'),('U002','Directory:admin'),('U999','CRM:reader')]:
        assignments.append(dict(id=f'A{len(assignments)+1:03}',identity=uid,entitlement=ent))
    return dict(identities=identities,entitlements=entitlements,assignments=assignments)

def validate(snapshot):
    for key in ['identities','entitlements','assignments']:
        rows=snapshot[key]
        if len({r['id'] for r in rows})!=len(rows): raise ValueError(f'Duplicate {key} ID')
    ents={e['id'] for e in snapshot['entitlements']}
    if any(a['entitlement'] not in ents for a in snapshot['assignments']): raise ValueError('Unknown entitlement')

def detect(s):
    validate(s); identities={i['id']:i for i in s['identities']}; ents={e['id']:e for e in s['entitlements']}; findings=[]
    for a in s['assignments']:
        i=identities.get(a['identity']); e=ents[a['entitlement']]; reasons=[]
        if i is None: reasons.append(('orphan',90))
        elif not i['active']: reasons.append(('inactive',80))
        elif i['last_login_days']>=90: reasons.append(('stale',50))
        if e['privileged']: reasons.append(('privileged',70))
        if i and i['department']!='IT' and e['privileged']: reasons.append(('excessive',85))
        peers={x['entitlement'] for x in s['assignments'] if x['identity']==a['identity']}
        if e['application']== 'Ledger' and e['role'] in ['requester','approver'] and {'Ledger:requester','Ledger:approver'}<=peers: reasons.append(('sod',95))
        for kind,score in reasons: findings.append(dict(assignment=a['id'],identity=a['identity'],kind=kind,score=score,reviewer=e['owner']))
    return sorted(findings,key=lambda f:(-f['score'],f['assignment'],f['kind']))

def drift(before, after):
    old={a['id']:a for a in before['assignments']};new={a['id']:a for a in after['assignments']}
    return dict(granted=[new[k] for k in sorted(new.keys()-old.keys())],removed=[old[k] for k in sorted(old.keys()-new.keys())],changed=[dict(before=old[k],after=new[k]) for k in sorted(old.keys()&new.keys()) if old[k]!=new[k]])

def campaign(s, findings):
    risks={f['assignment']:[] for f in findings}
    for f in findings: risks[f['assignment']].append(f['kind'])
    ents={e['id']:e for e in s['entitlements']}; decisions=[]
    for a in s['assignments']:
        kinds=risks.get(a['id'],[])
        decision='revoke' if set(kinds)&{'orphan','inactive','sod','excessive'} else 'exception' if 'stale' in kinds else 'approve'
        decisions.append(dict(assignment=a['id'],reviewer=ents[a['entitlement']]['owner'],decision=decision,rationale=', '.join(kinds) or 'Aligned with department baseline',timestamp=stamp(),exception_expiry='2026-11-12' if decision=='exception' else None,simulated=True))
    return decisions

def remediate(s, decisions):
    ids={a['id'] for a in s['assignments']}
    if {d['assignment'] for d in decisions}!=ids or len(decisions)!=len(ids): raise ValueError('Campaign must cover each assignment exactly once')
    if any(d['decision'] not in {'approve','revoke','exception'} for d in decisions): raise ValueError('Invalid decision')
    ents={e['id']:e for e in s['entitlements']}; assignments={a['id']:a for a in s['assignments']}
    for d in decisions:
        if d['reviewer']!=ents[assignments[d['assignment']]['entitlement']]['owner']: raise ValueError('Unauthorized reviewer')
        if not d['rationale'] or not d['timestamp']: raise ValueError('Missing evidence')
        if d['decision']=='exception' and not d['exception_expiry']: raise ValueError('Exception needs expiry')
    revoked={d['assignment'] for d in decisions if d['decision']=='revoke'}
    after=dict(s,assignments=[a for a in s['assignments'] if a['id'] not in revoked])
    return after,[dict(assignment=k,action='revoke',status='verified_absent' if k not in {a['id'] for a in after['assignments']} else 'failed',timestamp=stamp(),target='synthetic snapshot') for k in sorted(revoked)]

def collect(folder):
    result={}
    for name in ['identities','entitlements','assignments']:
        with (folder/(name+'.csv')).open(encoding='utf-8',newline='') as f: result[name]=list(csv.DictReader(f))
    for i in result['identities']: i['active']=i['active'].lower()=='true';i['last_login_days']=int(i['last_login_days'])
    for e in result['entitlements']: e['privileged']=e['privileged'].lower()=='true'
    validate(result);return result

def run(out, source=None):
    if out.exists(): raise ValueError('Output directory already exists; choose a fresh run directory')
    s=collect(source) if source else fixture();validate(s)
    findings=detect(s);decisions=campaign(s,findings);after,log=remediate(s,decisions)
    for name,value in [('before',s),('findings',findings),('decisions',decisions),('after',after),('remediation',log),('drift',drift(s,after)),('privileged-review',[d for d in decisions if next(a for a in s['assignments'] if a['id']==d['assignment'])['entitlement'].endswith(':admin')])]:save(out/(name+'.json'),value)
    summary=dict(mode='synthetic simulation; no external access changed',identities=len(s['identities']),departments=len({i['department'] for i in s['identities']}),applications=len({e['application'] for e in s['entitlements']}),entitlements=len(s['entitlements']),reviewed=len(decisions),decisions={k:sum(d['decision']==k for d in decisions) for k in ['approve','revoke','exception']},findings=len(findings),revocations=len(log),verified=all(r['status']=='verified_absent' for r in log),before_sha256=digest(s),after_sha256=digest(after),timestamp=stamp())
    save(out/'summary.json',summary)
    save(out/'manifest.json',{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.glob('*.json'))})
    (out/'report.md').write_text('# Certification audit report\n\nSynthetic reviewers and decisions; no human approval or external remediation claimed.\n\n'+ '\n'.join(f'- {k}: {v}' for k,v in summary.items()),encoding='utf-8')
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--source',type=Path);a=p.parse_args();print(json.dumps(run(a.out,a.source),indent=2))
