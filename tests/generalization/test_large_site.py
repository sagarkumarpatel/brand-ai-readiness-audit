from tests.generalization.base import GeneralizationTestCase
from tests.generalization.expected import ExpectedFindings

class TestLargeArchetype(GeneralizationTestCase):
    async def test_large_clean(self):
        report = await self.run_audit_on('/large/clean/')
        self.evaluate_findings(report, [], [])
