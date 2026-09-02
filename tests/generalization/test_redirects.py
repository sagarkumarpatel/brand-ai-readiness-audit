from tests.generalization.base import GeneralizationTestCase
from tests.generalization.expected import ExpectedFindings

class TestRedirectsArchetype(GeneralizationTestCase):
    async def test_redirects_clean(self):
        report = await self.run_audit_on('/redirects/clean/')
        self.evaluate_findings(report, [], [ExpectedFindings.EXCESSIVE_REDIRECT_CHAIN])

    async def test_redirects_defective(self):
        report = await self.run_audit_on('/redirects/defective/')
        self.evaluate_findings(report, [ExpectedFindings.EXCESSIVE_REDIRECT_CHAIN], [])
