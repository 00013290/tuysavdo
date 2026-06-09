import math


class VenueAdvisor:
    def __init__(self, database):
        self.db = database

    def advise_venue(self, guest_count, budget_per_seat, event_date=None):
        venues = self.db.get_all_venues()

        if not venues:
            return None, "No venues registered yet."

        # Filter by capacity and budget
        matching = []
        for v in venues:
            venue_id = v[0]
            capacity = v[6]
            price = v[7]

            if capacity >= guest_count and price <= budget_per_seat * 1.2:
                if event_date:
                    if not self.db.check_availability(venue_id, event_date):
                        continue
                matching.append(v)

        if not matching:
            return None, f"No venues available for {guest_count} guests within your budget."

        # Score each venue
        scored = []
        for v in matching:
            venue_id = v[0]
            price = v[7]
            capacity = v[6]
            has_catering = v[11]
            has_music = v[12]
            has_decoration = v[13]

            # Price score — cheaper is better
            price_score = 1 / (price + 0.1)

            # Capacity fit score — closer to guest count = better fit
            capacity_fit = 1 / (abs(capacity - guest_count) + 1)

            # Rating score
            avg_rating, rating_count = self.db.get_venue_average_rating(venue_id)
            rating_score = avg_rating / 5.0 if avg_rating > 0 else 0.5

            # Amenities bonus
            amenities_score = (has_catering + has_music + has_decoration) / 3.0

            # Total weighted score
            total_score = (
                price_score * 0.35 +
                capacity_fit * 0.30 +
                rating_score * 0.25 +
                amenities_score * 0.10
            )

            scored.append((total_score, v))

        # Sort by highest score
        scored.sort(key=lambda x: x[0], reverse=True)
        best_score, best = scored[0]

        avg_rating, rating_count = self.db.get_venue_average_rating(best[0])
        stars = "⭐" * int(avg_rating) if avg_rating > 0 else "No ratings yet"

        amenities = []
        if best[11]: amenities.append("🍽 Catering")
        if best[12]: amenities.append("🎵 Music")
        if best[13]: amenities.append("💐 Decoration")

        reason = (
            f"💵 Price: ${best[7]}/seat — fits your budget\n"
            f"👥 Capacity: {best[6]} guests — matches your requirements\n"
            f"⭐ Rating: {stars} ({avg_rating}/5 from {rating_count} reviews)\n"
            f"✨ Amenities: {', '.join(amenities) if amenities else 'Basic'}\n"
            f"🏆 Best overall match for your wedding"
        )

        return best, reason

    def analyze_price(self, guest_count, price_per_seat):
        venues = self.db.get_all_venues()

        if not venues:
            return "No price data available."

        prices = [v[7] for v in venues if v[6] >= guest_count]

        if not prices:
            return "No venues found with sufficient capacity."

        avg_price = sum(prices) / len(prices)
        min_price = min(prices)
        max_price = max(prices)

        if price_per_seat < avg_price:
            assessment = "✅ Below market average — great value!"
        elif price_per_seat == avg_price:
            assessment = "➡️ Exactly at market average."
        else:
            assessment = "⚠️ Above market average — consider comparing other venues."

        return (
            f"📊 *Price Analysis:*\n"
            f"   Selected price: ${price_per_seat}/seat\n"
            f"   Market average: ${avg_price:.2f}/seat\n"
            f"   Lowest available: ${min_price}/seat\n"
            f"   Highest available: ${max_price}/seat\n\n"
            f"   {assessment}"
        )