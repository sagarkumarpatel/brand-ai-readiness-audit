from tests.generalization.base import GeneralizationTestCase
from tests.generalization.expected import ExpectedFindings

class TestDeterminism(GeneralizationTestCase):
    async def test_determinism(self):
        report1 = await self.run_audit_on('/corporate/defective/')
        report2 = await self.run_audit_on('/corporate/defective/')
        
        # normalize audited_at
        report1.pop('audited_at', None)
        report2.pop('audited_at', None)
        
        self.assertEqual(report1, report2)
