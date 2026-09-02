from tests.generalization.base import GeneralizationTestCase
from tests.generalization.expected import ExpectedFindings

class TestEcommerceArchetype(GeneralizationTestCase):
    
    async def test_ecommerce_clean(self):
        report = await self.run_audit_on("/ecommerce/clean/")
        # Cart shouldn't be thin content
        self.evaluate_findings(report, 
                               expected_findings=[], 
                               forbidden_findings=[ExpectedFindings.THIN_CONTENT, ExpectedFindings.MISSING_STRUCTURED_DATA])
                               
    async def test_ecommerce_defective(self):
        report = await self.run_audit_on("/ecommerce/defective/")
        self.evaluate_findings(report, 
                               expected_findings=[ExpectedFindings.MISSING_STRUCTURED_DATA, ExpectedFindings.DEAD_END_PAGE], 
                               forbidden_findings=[])

