from tests.generalization.base import GeneralizationTestCase
from tests.generalization.expected import ExpectedFindings

class TestMediaArchetype(GeneralizationTestCase):
    async def test_media_clean(self):
        report = await self.run_audit_on('/media/clean/')
        self.evaluate_findings(report, [], [ExpectedFindings.THIN_CONTENT])
