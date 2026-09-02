from tests.generalization.base import GeneralizationTestCase
from tests.generalization.expected import ExpectedFindings

class TestDocsArchetype(GeneralizationTestCase):
    async def test_docs_clean(self):
        report = await self.run_audit_on('/docs/clean/')
        self.evaluate_findings(report, [], [ExpectedFindings.WALL_OF_TEXT])
                               
    async def test_docs_defective(self):
        report = await self.run_audit_on('/docs/defective/')
        self.evaluate_findings(report, [ExpectedFindings.WALL_OF_TEXT], [])
