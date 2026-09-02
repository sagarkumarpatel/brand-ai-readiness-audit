from tests.generalization.base import GeneralizationTestCase
from tests.generalization.expected import ExpectedFindings

class TestMultilingualArchetype(GeneralizationTestCase):
    async def test_multilingual_clean(self):
        report = await self.run_audit_on('/multi/clean/')
        self.evaluate_findings(report, [], [ExpectedFindings.THIN_CONTENT])
