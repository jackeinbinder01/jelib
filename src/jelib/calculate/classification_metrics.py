class ClassificationMetrics:
    def __init__(self, tp, fp, tn, fn):
        self.tp = tp
        self.fp = fp
        self.tn = tn
        self.fn = fn

    def accuracy(self, show_work=False):
        denominator = self.tp + self.fp + self.fn + self.tn
        if denominator == 0:
            if show_work:
                print("Accuracy is undefined (no samples), returning 0.")
            return 0.0

        acc = (self.tp + self.tn) / denominator

        if show_work:
            print("Accuracy = (TP + TN) / (TP + FP + FN + TN)")
            print(f"\t= ({self.tp} + {self.tn}) / ({self.tp} + {self.fp} + {self.fn} + {self.tn})")
            print(f"\t= ({self.tp + self.tn}) / ({denominator})")
            print(f"\t= {acc:.4f}")

        return acc

    def sensitivity(self, show_work=False):
        denominator = self.tp + self.fn
        if denominator == 0:
            if show_work:
                print("Sensitivity is undefined (TP + FN = 0), returning 0.")
            return 0.0

        sensitivity_value = self.tp / denominator

        if show_work:
            print("Sensitivity = TP / (TP + FN)")
            print(f"\t= {self.tp} / ({self.tp} + {self.fn})")
            print(f"\t= {self.tp} / ({denominator})")
            print(f"\t= {sensitivity_value:.4f}")

        return sensitivity_value

    def specificity(self, show_work=False):
        denominator = self.fp + self.tn
        if denominator == 0:
            if show_work:
                print("Specificity is undefined (FP + TN = 0), returning 0.")
            return 0.0

        specificity_value = self.tn / denominator

        if show_work:
            print("Specificity = TN / (FP + TN)")
            print(f"\t= {self.tn} / ({self.fp} + {self.tn})")
            print(f"\t= {self.tn} / ({denominator})")
            print(f"\t= {specificity_value:.4f}")

        return specificity_value

    def recall(self, show_work=False):
        denominator = self.tp + self.fn
        if denominator == 0:
            if show_work:
                print("Recall is undefined (TP + FN = 0), returning 0.")
            return 0.0

        recall_value = self.tp / denominator

        if show_work:
            print("Recall = TP / (TP + FN)")
            print(f"\t= {self.tp} / ({self.tp} + {self.fn})")
            print(f"\t= {self.tp} / ({denominator})")
            print(f"\t= {recall_value:.4f}")

        return recall_value

    def precision(self, show_work=False):
        denominator = self.tp + self.fp
        if denominator == 0:
            if show_work:
                print("Precision is undefined (TP + FP = 0), returning 0.")
            return 0.0

        precision_value = self.tp / denominator

        if show_work:
            print("Precision = TP / (TP + FP)")
            print(f"\t= {self.tp} / ({self.tp} + {self.fp})")
            print(f"\t= {self.tp} / ({denominator})")
            print(f"\t= {precision_value:.4f}")

        return precision_value

    def tpr(self, show_work=False):
        denominator = self.tp + self.fn
        if denominator == 0:
            if show_work:
                print("True Positive Rate is undefined (TP + FN = 0), returning 0.")
            return 0.0

        tpr_value = self.tp / denominator

        if show_work:
            print("True Positive Rate = TP / (TP + FN)")
            print(f"\t= {self.tp} / ({self.tp} + {self.fn})")
            print(f"\t= {self.tp} / ({denominator})")
            print(f"\t= {tpr_value:.4f}")

        return tpr_value

    def fpr(self, show_work=False):
        denominator = self.fp + self.tn
        if denominator == 0:
            if show_work:
                print("False Positive Rate is undefined (FP + TN = 0), returning 0.")
            return 0.0

        fpr_value = self.fp / denominator

        if show_work:
            print("False Positive Rate = FP / (FP + TN)")
            print(f"\t= {self.fp} / ({self.fp} + {self.tn})")
            print(f"\t= {self.fp} / ({denominator})")
            print(f"\t= {fpr_value:.4f}")

        return fpr_value

    def f1_score(self, show_work=False):
        precision_value = self.precision(show_work=show_work)
        recall_value = self.recall(show_work=show_work)
        denominator = precision_value + recall_value

        if denominator == 0:
            if show_work:
                print("F1-Score is undefined (precision + recall = 0), returning 0.")
            return 0.0

        f1 = 2 * ((precision_value * recall_value) / denominator)

        if show_work:
            print("F1-Score = 2 * (Precision * Recall) / (Precision + Recall)")
            print(f"= 2 * ({precision_value:.4f} * {recall_value:.4f}) / ({precision_value:.4f} + {recall_value:.4f})")
            print(f"= 2 * ({precision_value * recall_value:.4f}) / ({denominator:.4f})")
            print(f"= {f1:.4f}")

        return f1

    def summary(self):
        print("=== Classification Metrics Summary ===")
        print(f"Accuracy   : {self.accuracy():.4f}")
        print(f"Precision  : {self.precision():.4f}")
        print(f"Recall     : {self.recall():.4f}")
        print(f"Sensitivity: {self.sensitivity():.4f}")
        print(f"Specificity: {self.specificity():.4f}")
        print(f"TPR        : {self.tpr():.4f}")
        print(f"FPR        : {self.fpr():.4f}")
        print(f"F1-Score   : {self.f1_score():.4f}")

