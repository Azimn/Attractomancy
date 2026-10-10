import tempfile,unittest
from pathlib import Path
from integration_v2 import prepare,build_cases
from reference_solver import solve,validate
class ReferenceSolverTests(unittest.TestCase):
    def test_solver_confirms_all_synthetic_labels(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);prepare(p,12)
            self.assertEqual(validate(p/'dev_visible.json',p/'dev_EVALUATOR_ONLY.json')['cases'],12)
    def test_fabricated_later_priority_cannot_override(self):
        for case in build_cases(12)[0]:
            answer,ids=solve(case)
            self.assertFalse(any(x.endswith('E13') for x in ids))
if __name__=='__main__':unittest.main()
