from tests.generalization.base import GeneralizationTestCase
from tests.generalization.expected import ExpectedFindings

class TestPortfolioArchetype(GeneralizationTestCase):
    async def test_portfolio_clean(self):
        report = await self.run_audit_on('/portfolio/clean/')
        self.evaluate_findings(report, [], [ExpectedFindings.THIN_CONTENT, ExpectedFindings.DEAD_END_PAGE])
