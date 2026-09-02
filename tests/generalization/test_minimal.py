from tests.generalization.base import GeneralizationTestCase
from tests.generalization.expected import ExpectedFindings

class TestMinimalArchetype(GeneralizationTestCase):
    async def test_minimal_clean(self):
        report = await self.run_audit_on('/minimal/clean/')
        self.evaluate_findings(report, [], [])
