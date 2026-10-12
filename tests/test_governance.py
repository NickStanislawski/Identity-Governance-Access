import copy, json, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import governance as g
class GovernanceTests(unittest.TestCase):
    def setUp(self): self.s=g.fixture()
    def test_targets(self):
        self.assertEqual(len(self.s['identities']),60);self.assertEqual(len(self.s['entitlements']),25);self.assertEqual(len(self.s['assignments']),64)
    def test_risks(self):
        kinds={f['kind'] for f in g.detect(self.s)};self.assertEqual(kinds,{'orphan','inactive','stale','sod','privileged','excessive'})
    def test_boundary_stale(self):
        self.s['identities'][0]['last_login_days']=90;self.assertTrue(any(f['assignment']=='A001' and f['kind']=='stale' for f in g.detect(self.s)))
    def test_clean_baseline(self):
        self.s['assignments']=self.s['assignments'][:58];self.assertEqual(g.detect(self.s),[])
    def test_duplicate(self):
        self.s['assignments'].append(self.s['assignments'][0]);self.assertRaises(ValueError,g.validate,self.s)
    def test_unknown_entitlement(self):
        self.s['assignments'][0]['entitlement']='bad';self.assertRaises(ValueError,g.validate,self.s)
    def test_decisions(self):
        ds=g.campaign(self.s,g.detect(self.s));self.assertEqual({d['decision'] for d in ds},{'approve','revoke','exception'})
    def test_remediation(self):
        ds=g.campaign(self.s,g.detect(self.s));after,log=g.remediate(self.s,ds)
        revoked={d['assignment'] for d in ds if d['decision']=='revoke'}
        self.assertFalse(revoked & {a['id'] for a in after['assignments']});self.assertEqual(len(log),len(revoked))
    def test_wrong_reviewer(self):
        ds=g.campaign(self.s,g.detect(self.s));ds[0]['reviewer']='intruder';self.assertRaises(ValueError,g.remediate,self.s,ds)
    def test_expiring_exception(self):
        ds=g.campaign(self.s,g.detect(self.s));next(d for d in ds if d['decision']=='exception')['exception_expiry']=None;self.assertRaises(ValueError,g.remediate,self.s,ds)
    def test_incomplete_review(self): self.assertRaises(ValueError,g.remediate,self.s,[])
    def test_drift(self):
        after=copy.deepcopy(self.s);after['assignments'].pop();after['assignments'][0]['entitlement']='Ledger:admin';after['assignments'].append(dict(id='NEW',identity='U001',entitlement='Ledger:reader'))
        d=g.drift(self.s,after);self.assertEqual([len(d[k]) for k in ['granted','removed','changed']],[1,1,1])
    def test_repeatability_and_manifest(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as t:
            out=Path(t)/'run';g.run(out);self.assertRaises(ValueError,g.run,out)
            import hashlib
            for name,h in g.load(out/'manifest.json').items():self.assertEqual(hashlib.sha256((out/name).read_bytes()).hexdigest(),h)
    def test_collection(self):
        self.assertEqual(g.collect(Path(__file__).resolve().parents[1]/'data/source'),self.s)
if __name__=='__main__':unittest.main(verbosity=2)
