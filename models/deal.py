"""
Deal model - represents acquisition or exit negotiations.
"""

from typing import Optional, Dict, Any
import random
from .company import Company
import config


class Deal:
    """Represents a negotiation to buy or sell a company."""
    
    def __init__(self, company: Company, deal_type: str = 'acquisition', 
                 seller_reservation_price: float = None):
        """
        Initialize a deal.
        
        Args:
            company: The company being transacted
            deal_type: 'acquisition' or 'exit'
            seller_reservation_price: Minimum price seller will accept (None for random)
        """
        self.company = company
        self.deal_type = deal_type
        
        # Calculate fair value
        self.fair_value = company.current_valuation
        
        # Seller's minimum acceptable price (hidden from player)
        if seller_reservation_price is not None:
            self.seller_reservation_price = seller_reservation_price
        else:
            # Sellers typically want 80-120% of fair value
            price_factor = random.uniform(0.8, 1.2)
            self.seller_reservation_price = self.fair_value * price_factor
            
        # Initial asking price (typically higher than reservation)
        if deal_type == 'acquisition':
            asking_multiplier = random.uniform(1.1, 1.3)
            self.asking_price = self.seller_reservation_price * asking_multiplier
        else:  # exit
            # Buyers typically offer 90-110% of fair value
            self.asking_price = self.fair_value * random.uniform(0.9, 1.1)
            
        # Negotiation state
        self.current_offer: Optional[float] = None
        self.counter_offers = 0
        self.max_counter_offers = config.NEGOTIATION_ROUNDS
        self.deal_closed = False
        self.deal_accepted = False
        
        # Hidden quality factor (affects how good the deal really is)
        self.hidden_quality = random.gauss(1.0, 0.15)  # Usually near 1.0, sometimes better/worse
        
    def make_offer(self, offer_price: float) -> Dict[str, Any]:
        """
        Player makes an offer. Returns negotiation result.
        """
        self.current_offer = offer_price
        
        # Check if offer is acceptable
        if offer_price >= self.seller_reservation_price:
            self.deal_closed = True
            self.deal_accepted = True
            return {
                'accepted': True,
                'message': f"Offer accepted! Deal closed at ${offer_price:,.0f}",
                'final_price': offer_price
            }
            
        # Check if we've exceeded negotiation rounds
        if self.counter_offers >= self.max_counter_offers:
            self.deal_closed = True
            self.deal_accepted = False
            return {
                'accepted': False,
                'message': "Seller has walked away from negotiations.",
                'final_price': None
            }
            
        # Generate counter-offer (move toward reservation price)
        gap = self.seller_reservation_price - offer_price
        counter_price = offer_price + gap * random.uniform(0.6, 0.8)
        
        self.counter_offers += 1
        
        return {
            'accepted': False,
            'counter_offer': counter_price,
            'message': f"Seller counters at ${counter_price:,.0f}",
            'rounds_remaining': self.max_counter_offers - self.counter_offers
        }
        
    def accept_asking_price(self) -> Dict[str, Any]:
        """Player accepts the current asking/counter price."""
        self.deal_closed = True
        self.deal_accepted = True
        return {
            'accepted': True,
            'message': f"Deal accepted at ${self.asking_price:,.0f}",
            'final_price': self.asking_price
        }
        
    def walk_away(self) -> Dict[str, Any]:
        """Player walks away from the deal."""
        self.deal_closed = True
        self.deal_accepted = False
        return {
            'accepted': False,
            'message': "You have walked away from the deal.",
            'final_price': None
        }
        
    def get_deal_quality_score(self) -> float:
        """
        Calculate how good this deal is (for player analytics).
        > 1.0 = good deal, < 1.0 = bad deal
        """
        if not self.deal_accepted or self.current_offer is None:
            return 0.0
            
        if self.deal_type == 'acquisition':
            # Lower price relative to fair value = better deal
            price_ratio = self.current_offer / self.fair_value
            return self.hidden_quality / price_ratio
        else:  # exit
            # Higher price relative to fair value = better deal
            price_ratio = self.current_offer / self.fair_value
            return price_ratio * self.hidden_quality
            
    def __str__(self) -> str:
        return (f"{self.deal_type.title()} Deal: {self.company.name} - "
                f"Asking: ${self.asking_price:,.0f}, "
                f"Fair Value: ${self.fair_value:,.0f}")

