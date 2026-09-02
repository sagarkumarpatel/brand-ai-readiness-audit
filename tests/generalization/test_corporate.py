from tests.generalization.base import GeneralizationTestCase
from tests.generalization.expected import ExpectedFindings

class TestCorporateArchetype(GeneralizationTestCase):
    
    async def test_corporate_clean(self):
        report = await self.run_audit_on("/corporate/clean/")
        # Should not flag short contact page as thin content
        self.evaluate_findings(report, 
                               expected_findings=[], 
                               forbidden_findings=[ExpectedFindings.THIN_CONTENT, ExpectedFindings.MISSING_CANONICAL])
                               
    async def test_corporate_defective(self):
        report = await self.run_audit_on("/corporate/defective/")
        self.evaluate_findings(report, 
                               expected_findings=[ExpectedFindings.MISSING_CANONICAL, ExpectedFindings.THIN_CONTENT], 
                               forbidden_findings=[])

