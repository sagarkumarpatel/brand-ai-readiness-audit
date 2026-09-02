from tests.generalization.base import GeneralizationTestCase
from tests.generalization.expected import ExpectedFindings

class TestBlogArchetype(GeneralizationTestCase):
    
    async def test_blog_clean(self):
        report = await self.run_audit_on("/blog/clean/")
        self.evaluate_findings(report, 
                               expected_findings=[], 
                               forbidden_findings=[ExpectedFindings.STALE_CONTENT])
                               
    async def test_blog_defective(self):
        report = await self.run_audit_on("/blog/defective/")
        self.evaluate_findings(report, 
                               expected_findings=[ExpectedFindings.STALE_CONTENT], 
                               forbidden_findings=[])

