import math

import pandas as pd


class GainCalculator:

    def __init__(self, table: pd.DataFrame, target: str):
        self.table = table
        self.target = target
        self.E = self.entropy()

    @staticmethod
    def information(p, n, show_work=False):
        if p == 0 or n == 0:
            return 0.0
        p_frac = p / (p + n)
        n_frac = n / (p + n)

        if show_work:
            print("I(p, n) = -(p / (p + n)) * log_2(p / (p + n)) - (n / (p + n)) * log_2(n / (p + n))")
            print(f"I({p}, {n}) = -({p} / ({p} + {n})) * log_2({p} / ({p} + {n})) - ({n} / ({p} + {n})) * log_2({n} / ({p} + {n}))")
            print(f"I({p}, {n}) = -({p} / ({p + n})) * log_2({p} / ({p + n})) - ({n} / ({p + n})) * log_2({n} / ({p + n}))")
            print(f"I({p}, {n}) = {(-p / (p + n)):.4f} * log_2({(p / (p + n)):.4f}) - {(n / (p + n)):.4f} * log_2({(n / (p + n)):.4f})")
            print(f"I({p}, {n}) = {(-p / (p + n)):.4f} * {math.log2((p / (p + n))):.4f} - {(n / (p + n)):.4f} * {math.log2(n / (p + n)):.4f}")
            print(f"I({p}, {n}) = {(-p / (p + n)) * math.log2((p / (p + n))):.4f} - {(n / (p + n)) * math.log2(n / (p + n)):.4f}")
            print(f"I({p}, {n}) = {(-p / (p + n)) * math.log2((p / (p + n))) - (n / (p + n)) * math.log2(n / (p + n)):.4f}")

        return -p_frac * math.log2(p_frac) - n_frac * math.log2(n_frac)

    def entropy(self, show_work=False):
        counts = self.table[self.target].value_counts()
        if len(counts) != 2:
            raise ValueError("Target column must be binary (True/False)")
        p = counts.get(True, 0)
        n = counts.get(False, 0)
        if p + n == 0:
            return 0.0

        if show_work:
            print("Steps:\n")
            print("Calculate initial entropy for dataset I(p, n):\n")
            print(f"\tp = Sum({self.target}(X)) = {p}")
            print(f"\tn = Sum(~{self.target}(X)) = {n}\n")

            print(f"\tI(p, n) = - (p / (p + n)) * log_2(p / (p + n)) - (n / (p + n)) * log_2(n / (p + n))\n")

            denom = p + n
            pf = f"{p}/{denom}"
            nf = f"{n}/{denom}"
            log_pf = math.log2(p / denom)
            log_nf = math.log2(n / denom)
            term_pf = -p / denom * log_pf
            term_nf = -n / denom * log_nf

            print(f"\tI({p}, {n}) = - ({pf}) * log_2({pf}) - ({nf}) * log_2({nf})")
            print(f"\t= - ({pf}) * {log_pf:.4f} - ({nf}) * {log_nf:.4f}")
            print(f"\t= {term_pf:.4f} + {term_nf:.4f}")
            print(f"\t= {term_pf + term_nf:.4f}\n")

        return self.information(p, n)

    def information_for_attribute(self, attribute, show_work=False):
        grouped = self.table.groupby(attribute)
        total = len(self.table)

        info_sum = 0.0
        sum_parts = []

        if show_work:
            print(f"Calculate expected entropy of splitting on {attribute}:\n")

        for value, subset in grouped:
            counts = subset[self.target].value_counts()
            p = counts.get(True, 0)
            n = counts.get(False, 0)
            subset_size = p + n
            weight = subset_size / total
            entropy = self.information(p, n)

            if show_work:
                attr = attribute
                value_str = f"{attr}(X)" if value else f"~{attr}(X)"
                suffix = "t" if value else "f"

                print(f"\tp_{suffix} = Sum({value_str} ^ {self.target}(X)) = {p} ")
                print(f"\tn_{suffix} = Sum({value_str} ^ ~{self.target}(X)) = {n}\n")

                denom = p + n
                pf = f"{p}/{denom}"
                nf = f"{n}/{denom}"
                log_pf = math.log2(p / denom) if p > 0 else 0
                log_nf = math.log2(n / denom) if n > 0 else 0
                term_pf = -p / denom * log_pf if p > 0 else 0
                term_nf = -n / denom * log_nf if n > 0 else 0

                print(f"\tI({p}, {n}) = - ({pf}) * log_2({pf}) - ({nf}) * log_2({nf})")
                print(f"\t         = - ({pf}) * {log_pf:.4f} - ({nf}) * {log_nf:.4f}")
                print(f"\t         = {term_pf:.4f} + {term_nf:.4f}")
                print(f"\t         = {entropy:.4f}\n")

            sum_parts.append(f"({p + n}/{total}) * I({p}, {n})")
            info_sum += weight * entropy

        if show_work:
            print(f"\tE({attribute}) = " + " + ".join(sum_parts))
            print(f"\t             = {info_sum:.4f}\n")

        return info_sum

    def gain(self, attribute, show_work=False):
        entropy_total = self.entropy(show_work=show_work)
        expected_entropy = self.information_for_attribute(attribute, show_work=show_work)
        gain_value = entropy_total - expected_entropy

        if show_work:
            print(f"Calculate Gain({attribute}):\n")
            print(f"\tGain({attribute}) = I(p, n) - E({attribute})")
            print(f"\t= {entropy_total:.4f} - {expected_entropy:.4f}")
            print(f"\t= {gain_value:.4f}")

        return gain_value







