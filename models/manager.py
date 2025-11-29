"""
Manager model - procedurally generated NPCs managing portfolio companies.
"""

import random
import config


class Manager:
    """Represents a company management team with behavioral attributes."""
    
    def __init__(self, name: str = None, competence: float = None, 
                 risk_profile: float = None, cooperativeness: float = None):
        self.name = name or self._generate_name()
        
        # All attributes on 0-1 scale
        self.competence = competence if competence is not None else random.uniform(
            config.MIN_MANAGER_COMPETENCE, config.MAX_MANAGER_COMPETENCE
        )
        self.risk_profile = risk_profile if risk_profile is not None else random.uniform(
            config.MIN_MANAGER_RISK_PROFILE, config.MAX_MANAGER_RISK_PROFILE
        )
        self.cooperativeness = cooperativeness if cooperativeness is not None else random.uniform(
            config.MIN_MANAGER_COOPERATIVENESS, config.MAX_MANAGER_COOPERATIVENESS
        )
        
    def _generate_name(self) -> str:
        """Generate a random manager name with gender variety and diverse backgrounds."""
        male_first_names = [
            "Braylyn", "Jaxon", "Hunter", "Cuyler", "Landon", "Kason", "Vignesh", "David", "Noah",
            "Moshe", "Elior", "Jacob", "Winston", "Jensen", "Arjun", "Santiago", "Yosef", "Chang",
            "Rohan", "Isaac", "Haruto", "Brigham", "Ezra", "Aaryan"
        ]
        female_first_names = [
            "Rebecca", "Skylynn", "Aubree", "Mckynlee", "Hannah", "Lakyn", "Neha", "Sariah", "Rivka",
            "Tzipporah", "Priya", "Chaya", "Mei", "Sophia", "Maliyah", "Adalyn", "Yvette", "Shanti",
            "Lexie", "Hui", "Ivy", "Trang", "Arya", "Kavya"
        ]
        last_names = [
            "Smith", "Johnson", "Brown", "Williams", "Rabinowitz", "Stein", "Lieberman", "Goldberg",
            "Shumway", "Brigham", "Chen", "Wang", "Lee", "Kim", "Chakrabarthy", "Patel", "Venkataraman", 
            "Kumar", "Martinez", "Garcia", "Davis", "Yang", "Wong", "Gupta", "Avraham", "Kimball", "Tapia"
        ]
        
        gender = random.choice(['male', 'female'])
        if gender == 'male':
            first_name = random.choice(male_first_names)
        else:
            first_name = random.choice(female_first_names)
        last_name = random.choice(last_names)
        return f"{first_name} {last_name}"
        return f"{random.choice(first_names)} {random.choice(last_names)}"
        
    def get_performance_modifier(self) -> float:
        """
        Calculate performance impact based on competence and risk profile.
        Returns a modifier to apply to company growth.
        """
        # Competence directly improves performance
        base_modifier = (self.competence - 0.5) * 0.1  # ±5%
        
        # Risk profile adds variance (can be good or bad)
        risk_factor = random.gauss(0, self.risk_profile * 0.05)
        
        return base_modifier + risk_factor
        
    def get_negotiation_difficulty(self) -> float:
        """
        Calculate how difficult this manager is to negotiate with.
        Lower cooperativeness = harder to replace or negotiate with.
        """
        return 1.0 - self.cooperativeness
        
    def get_stability_factor(self) -> float:
        """
        Calculate operational stability.
        High competence + high cooperativeness = more stable.
        """
        return (self.competence + self.cooperativeness) / 2.0
        
    def __str__(self) -> str:
        return f"{self.name} (Competence: {self.competence:.1%}, Risk: {self.risk_profile:.1%}, Coop: {self.cooperativeness:.1%})"
        
    def __repr__(self) -> str:
        return f"Manager(name='{self.name}', competence={self.competence:.2f}, risk={self.risk_profile:.2f}, coop={self.cooperativeness:.2f})"

