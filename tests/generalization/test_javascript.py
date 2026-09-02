from tests.generalization.base import GeneralizationTestCase
from tests.generalization.expected import ExpectedFindings

class TestJSArchetype(GeneralizationTestCase):
    async def test_javascript_clean(self):
        report = await self.run_audit_on('/js/clean/')
        self.evaluate_findings(report, [], [ExpectedFindings.THIN_CONTENT])
