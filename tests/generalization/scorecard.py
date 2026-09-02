class Scorecard:
    def __init__(self):
        self.tp = 0
        self.fp = 0
        self.fn = 0
        self.severity_matches = 0
        self.recommendation_matches = 0
        self.total_findings_evaluated = 0

    def add_result(self, expected_id, found_finding):
        self.total_findings_evaluated += 1
        if found_finding is None:
            self.fn += 1
        else:
            self.tp += 1
            # We would normally check severity and recommendations here too

    def add_false_positive(self):
        self.total_findings_evaluated += 1
        self.fp += 1

    def compute(self):
        precision = self.tp / (self.tp + self.fp) if (self.tp + self.fp) > 0 else 0.0
        recall = self.tp / (self.tp + self.fn) if (self.tp + self.fn) > 0 else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        return {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "tp": self.tp,
            "fp": self.fp,
            "fn": self.fn
        }

