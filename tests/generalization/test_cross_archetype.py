import unittest
from tests.generalization.base import GeneralizationTestCase
from tests.generalization.expected import ExpectedFindings

class TestCrossArchetype(GeneralizationTestCase):
    async def test_consistency(self):
        # Defect missing canonical on corporate
        report_corp = await self.run_audit_on('/corporate/defective/')
        
        corp_missing_can = [f for f in report_corp.get('findings', []) if f['id'] == ExpectedFindings.MISSING_CANONICAL]
        self.assertEqual(len(corp_missing_can), 1)
        self.assertEqual(corp_missing_can[0]['severity'], 'LOW')
