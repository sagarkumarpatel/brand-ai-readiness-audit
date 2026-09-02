from tests.generalization.base import GeneralizationTestCase
from tests.generalization.expected import ExpectedFindings

class TestSaaSArchetype(GeneralizationTestCase):
    async def test_saas_clean(self):
        report = await self.run_audit_on('/saas/clean/')
        self.evaluate_findings(report, [], [ExpectedFindings.THIN_CONTENT])
