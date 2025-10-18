class BayesCalculator:
    def __init__(self, prior_h, likelihood_e_given_h, likelihood_e_given_not_h, prior_not_h=None):
        self.p_h = prior_h
        self.p_not_h = 1 - prior_h if prior_not_h is None else prior_not_h
        self.p_e_given_h = likelihood_e_given_h
        self.p_e_given_not_h = likelihood_e_given_not_h

    def posterior(self, show_work=False):
        numerator = self.p_e_given_h * self.p_h
        denominator = (self.p_e_given_h * self.p_h) + (self.p_e_given_not_h * self.p_not_h)

        if denominator == 0:
            if show_work:
                print("Denominator is zero — cannot divide. Returning 0.")
            return 0.0

        posterior = numerator / denominator

        if show_work:
            print("Using Bayes' Theorem:")
            print("P(H|E) = [P(E|H) * P(H)] / [P(E|H) * P(H) + P(E|¬H) * P(¬H)]")
            print(f"\t= [{self.p_e_given_h:.4f} * {self.p_h:.4f}] / "
                  f"[{self.p_e_given_h:.4f} * {self.p_h:.4f} + {self.p_e_given_not_h:.4f} * {self.p_not_h:.4f}]")
            print(f"\t= {numerator:.4f} / ({numerator:.4f} + {self.p_e_given_not_h * self.p_not_h:.4f})")
            print(f"\t= {numerator:.4f} / {denominator:.4f}")
            print(f"\t= {posterior:.4f}")

        return posterior
