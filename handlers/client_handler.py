import json
import base64
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import ContextTypes, ConversationHandler
from handlers.start_handler import (
    ROLE_CHOICE,
    CLIENT_NAME, CLIENT_PHONE,
    BOOK_VENUE, BOOK_DATE, BOOK_GUESTS,
    BOOK_COUPLE, BOOK_WISHES, BOOK_PAYMENT,
    RATE_BOOKING, RATE_STARS, RATE_COMMENT,
    AI_GUESTS, AI_BUDGET, AI_DATE,
    CLIENT_MENU, get_client_menu
)

CLIENT_MINIAPP_URL = "https://00013290.github.io/tuysavdo/miniapp/client.html"
CANCEL_KEYBOARD = ReplyKeyboardMarkup([["❌ Cancel"]], resize_keyboard=True)


class ClientHandler:
    def __init__(self, database):
        self.db = database
        self.advisor = None

    def set_advisor(self, advisor):
        self.advisor = advisor

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text

        if text == "🔍 Browse Venues":
            return await self.browse_venues(update, context)
        elif text == "📅 Book a Venue":
            return await self.book_venue_start(update, context)
        elif text == "🤖 AI Advice":
            return await self.ai_start(update, context)
        elif text == "📋 My Bookings":
            return await self.my_bookings(update, context)
        elif text == "⭐ Rate a Venue":
            return await self.rate_start(update, context)
        elif text == "🌐 Track Bookings":
            return await self.open_dashboard(update, context)
        else:
            await update.message.reply_text("Please choose an option.", reply_markup=CLIENT_MENU)
            return ROLE_CHOICE

    async def open_dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_id = update.effective_user.id
        bookings = self.db.get_client_bookings(telegram_id)
        venues = self.db.get_all_venues()

        total = len(bookings)
        confirmed = len([b for b in bookings if b[7] == "Confirmed"])
        pending = len([b for b in bookings if b[7] == "Pending"])
        spent = sum(b[4] for b in bookings if b[7] == "Confirmed")

        data = {
            "stats": {"total": total, "confirmed": confirmed, "pending": pending, "spent": round(spent, 2)},
            "bookings": [
                {"id": b[0], "venue": b[1], "date": b[2], "guests": b[3],
                 "total": b[4], "status": b[7], "couple": b[8], "payment": b[6], "downPayment": b[10]}
                for b in bookings[:20]
            ],
            "venues": [
                {"name": v[3], "address": v[4], "capacity": v[6], "price": v[7],
                 "amenities": {"catering": bool(v[11]), "music": bool(v[12]), "decoration": bool(v[13])}}
                for v in venues
            ]
        }

        encoded = base64.b64encode(json.dumps(data).encode()).decode()
        url = f"{CLIENT_MINIAPP_URL}?data={encoded}"
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🌐 Open Client Dashboard", web_app=WebAppInfo(url=url))]])
        await update.message.reply_text("📊 Open your Client Dashboard:", reply_markup=keyboard)
        return ROLE_CHOICE

    # ── Registration ─────────────────────────────────────────────────────
    async def client_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=ReplyKeyboardRemove())
            return ROLE_CHOICE
        context.user_data["client_name"] = update.message.text
        await update.message.reply_text(
            "📞 What is your phone number?\n(e.g. +998901234567)",
            reply_markup=CANCEL_KEYBOARD
        )
        return CLIENT_PHONE

    async def client_phone(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=ReplyKeyboardRemove())
            return ROLE_CHOICE
        name = context.user_data["client_name"]
        phone = update.message.text
        self.db.add_client(update.effective_user.id, name, phone)
        self.db.register_user(update.effective_user.id, name, "", "client")
        await update.message.reply_text(
            f"✅ *Welcome, {name}!*\n\n"
            f"📞 Phone: {phone}\n\n"
            f"You can now browse and book wedding venues!",
            parse_mode="Markdown",
            reply_markup=CLIENT_MENU
        )
        return ROLE_CHOICE

    # ── Browse Venues ─────────────────────────────────────────────────────
    async def browse_venues(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        venues = self.db.get_all_venues()
        if not venues:
            await update.message.reply_text("No venues registered yet.", reply_markup=CLIENT_MENU)
            return ROLE_CHOICE

        await update.message.reply_text(f"🏛 *Available Venues ({len(venues)} total):*", parse_mode="Markdown", reply_markup=CLIENT_MENU)

        for v in venues:
            amenities = []
            if v[11]: amenities.append("🍽 Catering")
            if v[12]: amenities.append("🎵 Music")
            if v[13]: amenities.append("💐 Decoration")
            avg_rating, rating_count = self.db.get_venue_average_rating(v[0])
            stars = "⭐" * int(avg_rating) if avg_rating > 0 else "No ratings yet"

            msg = (
                f"🏛 *{v[3]}* (ID: {v[0]})\n"
                f"👤 Owner: {v[2]}\n"
                f"📍 {v[4]}\n"
                f"📝 {v[5]}\n"
                f"👥 Capacity: {v[6]} guests\n"
                f"💵 Price: ${v[7]}/seat\n"
                f"📞 Contact: {v[8]}\n"
                f"✨ Amenities: {', '.join(amenities) if amenities else 'None'}\n"
                f"⭐ Rating: {stars} ({avg_rating}/5 — {rating_count} reviews)"
            )

            if v[14]:
                await update.message.reply_photo(photo=v[14], caption=msg, parse_mode="Markdown")
            else:
                await update.message.reply_text(msg, parse_mode="Markdown")

        await update.message.reply_text("To book tap 📅 Book a Venue", reply_markup=CLIENT_MENU)
        return ROLE_CHOICE

    # ── Book a Venue ──────────────────────────────────────────────────────
    async def book_venue_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        venues = self.db.get_all_venues()
        if not venues:
            await update.message.reply_text("No venues available yet.", reply_markup=CLIENT_MENU)
            return ROLE_CHOICE

        msg = "📅 *Select a Venue to Book:*\n\n"
        for v in venues:
            amenities = []
            if v[11]: amenities.append("🍽")
            if v[12]: amenities.append("🎵")
            if v[13]: amenities.append("💐")
            avg_rating, _ = self.db.get_venue_average_rating(v[0])
            stars = "⭐" * int(avg_rating) if avg_rating > 0 else ""
            msg += f"*ID {v[0]}* — {v[3]} {stars}\n"
            msg += f"   👥 {v[6]} guests | 💵 ${v[7]}/seat\n"
            msg += f"   {' '.join(amenities) if amenities else 'No amenities'}\n\n"

        msg += "Enter the Venue ID (e.g. type *1*):"
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=CANCEL_KEYBOARD)
        return BOOK_VENUE

    async def book_venue(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Booking cancelled.", reply_markup=CLIENT_MENU)
            return ROLE_CHOICE
        try:
            venue_id = int(update.message.text)
            venue = self.db.get_venue_by_id(venue_id)
            if not venue:
                await update.message.reply_text("Venue not found. Please enter a valid ID.")
                return BOOK_VENUE
            context.user_data["book_venue_id"] = venue_id
            context.user_data["book_venue_name"] = venue[3]
            context.user_data["book_venue_capacity"] = venue[6]
            context.user_data["book_price_per_seat"] = venue[7]
            await update.message.reply_text(
                f"🏛 *{venue[3]}*\n👥 {venue[6]} guests | 💵 ${venue[7]}/seat\n\n"
                f"📅 What is your wedding date?\n(Format: DD/MM/YYYY)",
                parse_mode="Markdown", reply_markup=CANCEL_KEYBOARD
            )
            return BOOK_DATE
        except ValueError:
            await update.message.reply_text("Please enter a valid number.")
            return BOOK_VENUE

    async def book_date(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Booking cancelled.", reply_markup=CLIENT_MENU)
            return ROLE_CHOICE
        event_date = update.message.text
        venue_id = context.user_data["book_venue_id"]
        if not self.db.check_availability(venue_id, event_date):
            await update.message.reply_text(
                f"❌ *Sorry! This venue is booked on {event_date}*\n\nPlease choose a different date:",
                parse_mode="Markdown", reply_markup=CANCEL_KEYBOARD
            )
            return BOOK_DATE
        context.user_data["book_date"] = event_date
        await update.message.reply_text(
            f"✅ *{event_date} is available!*\n\n👥 How many guests?",
            parse_mode="Markdown", reply_markup=CANCEL_KEYBOARD
        )
        return BOOK_GUESTS

    async def book_guests(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Booking cancelled.", reply_markup=CLIENT_MENU)
            return ROLE_CHOICE
        try:
            guests = int(update.message.text)
            capacity = context.user_data["book_venue_capacity"]
            if guests > capacity:
                await update.message.reply_text(
                    f"❌ Maximum capacity is *{capacity} guests*.\nPlease enter up to {capacity}:",
                    parse_mode="Markdown", reply_markup=CANCEL_KEYBOARD
                )
                return BOOK_GUESTS
            context.user_data["book_guests"] = guests
            await update.message.reply_text(
                "💑 What are the *bride and groom's names*?\n\n(e.g. Zabixullo & Sabina)",
                parse_mode="Markdown", reply_markup=CANCEL_KEYBOARD
            )
            return BOOK_COUPLE
        except ValueError:
            await update.message.reply_text("Please enter a valid number.")
            return BOOK_GUESTS

    async def book_couple(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Booking cancelled.", reply_markup=CLIENT_MENU)
            return ROLE_CHOICE
        context.user_data["book_couple"] = update.message.text
        await update.message.reply_text(
            "✨ Any additional wishes for your wedding?\n\n"
            "(e.g. flowers, photographer, fireworks, transport)\n\nOr tap Skip.",
            reply_markup=ReplyKeyboardMarkup([["⏭ Skip", "❌ Cancel"]], resize_keyboard=True)
        )
        return BOOK_WISHES

    async def book_wishes(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Booking cancelled.", reply_markup=CLIENT_MENU)
            return ROLE_CHOICE
        context.user_data["book_wishes"] = "" if update.message.text == "⏭ Skip" else update.message.text

        d = context.user_data
        total_cost = d["book_guests"] * d["book_price_per_seat"]
        down_payment = round(total_cost * 0.50, 2)

        keyboard = [["💵 Cash", "💳 Card"], ["❌ Cancel"]]
        await update.message.reply_text(
            f"💰 *Payment Summary:*\n\n"
            f"👥 Guests: {d['book_guests']}\n"
            f"💵 Price/seat: ${d['book_price_per_seat']}\n"
            f"💰 Total Cost: ${total_cost:.2f}\n"
            f"📊 Down Payment (50%): ${down_payment:.2f}\n\n"
            f"💳 How will you pay the down payment?",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return BOOK_PAYMENT

    async def book_payment(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Booking cancelled.", reply_markup=CLIENT_MENU)
            return ROLE_CHOICE

        payment_method = "cash" if "Cash" in update.message.text else "card"
        d = context.user_data
        client_name = self.db.get_client_name(update.effective_user.id)
        client_phone = self.db.get_client_phone(update.effective_user.id)

        commission, total_cost, down_payment = self.db.add_booking(
            update.effective_user.id, client_name, client_phone,
            d["book_venue_id"], d["book_venue_name"],
            d["book_date"], d["book_guests"],
            d["book_price_per_seat"], payment_method,
            d["book_couple"], d["book_wishes"]
        )

        payment_icon = "💵" if payment_method == "cash" else "💳"
        await update.message.reply_text(
            f"✅ *Booking Request Sent!*\n\n"
            f"🏛 Venue: {d['book_venue_name']}\n"
            f"📅 Wedding Date: {d['book_date']}\n"
            f"💑 Couple: {d['book_couple']}\n"
            f"👥 Guests: {d['book_guests']}\n"
            f"✨ Wishes: {d['book_wishes'] if d['book_wishes'] else 'None'}\n\n"
            f"💰 Total Cost: ${total_cost:.2f}\n"
            f"📊 Down Payment (50%): ${down_payment:.2f}\n"
            f"{payment_icon} Payment: {payment_method.capitalize()}\n"
            f"📋 Status: Pending\n\n"
            f"⏳ Waiting for venue confirmation...\n"
            f"Once confirmed, you'll receive payment instructions.",
            parse_mode="Markdown",
            reply_markup=CLIENT_MENU
        )

        # Notify venue owner instantly
        try:
            venue = self.db.get_venue_by_id(d["book_venue_id"])
            if venue:
                await context.bot.send_message(
                    chat_id=venue[1],
                    text=f"🔔 *New Booking Request!*\n\n"
                         f"👤 Client: {client_name}\n"
                         f"📞 Phone: {client_phone}\n"
                         f"💑 Couple: {d['book_couple']}\n"
                         f"📅 Wedding Date: {d['book_date']}\n"
                         f"👥 Guests: {d['book_guests']}\n"
                         f"✨ Wishes: {d['book_wishes'] if d['book_wishes'] else 'None'}\n\n"
                         f"💰 Total Cost: ${total_cost:.2f}\n"
                         f"📊 Down Payment (50%): ${down_payment:.2f}\n"
                         f"{payment_icon} Payment: {payment_method.capitalize()}\n\n"
                         f"Go to 📋 My Bookings to confirm or reject!",
                    parse_mode="Markdown"
                )
        except Exception as e:
            pass

        return ROLE_CHOICE

    # ── My Bookings ───────────────────────────────────────────────────────
    async def my_bookings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        bookings = self.db.get_client_bookings(update.effective_user.id)
        if not bookings:
            await update.message.reply_text("You have no bookings yet!", reply_markup=CLIENT_MENU)
            return ROLE_CHOICE

        msg = "📋 *Your Bookings:*\n\n"
        for b in bookings:
            status_icon = "✅" if b[7] == "Confirmed" else "❌" if b[7] == "Rejected" else "⏳"
            msg += (
                f"🔹 Booking #{b[0]}\n"
                f"   🏛 {b[1]}\n"
                f"   📅 {b[2]} | 💑 {b[8]}\n"
                f"   👥 {b[3]} guests\n"
                f"   💰 Total: ${b[4]:.2f} | Down: ${b[10]:.2f}\n"
                f"   💳 {b[6].capitalize()}\n"
                f"   {status_icon} {b[7]}\n\n"
            )
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=CLIENT_MENU)
        return ROLE_CHOICE

    # ── Rate a Venue ──────────────────────────────────────────────────────
    async def rate_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_id = update.effective_user.id
        bookings = self.db.get_client_bookings(telegram_id)
        ratable = [b for b in bookings if b[7] == "Confirmed" and not self.db.has_rated(b[0])]
        if not ratable:
            await update.message.reply_text("⭐ No confirmed bookings to rate yet!", reply_markup=CLIENT_MENU)
            return ROLE_CHOICE
        msg = "⭐ *Select a Booking to Rate:*\n\n"
        for b in ratable:
            msg += f"*Booking #{b[0]}* — {b[1]}\n   📅 {b[2]} | 💑 {b[8]}\n\n"
        msg += "Enter the Booking ID:"
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=CANCEL_KEYBOARD)
        return RATE_BOOKING

    async def rate_booking(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=CLIENT_MENU)
            return ROLE_CHOICE
        try:
            booking_id = int(update.message.text)
            booking = self.db.get_booking_by_id(booking_id)
            if not booking:
                await update.message.reply_text("Booking not found.")
                return RATE_BOOKING
            context.user_data["rate_booking_id"] = booking_id
            context.user_data["rate_venue_id"] = booking[4]
            keyboard = [["⭐", "⭐⭐", "⭐⭐⭐"], ["⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], ["❌ Cancel"]]
            await update.message.reply_text(
                f"⭐ *Rate {booking[5]}*\n\nHow many stars?",
                parse_mode="Markdown",
                reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            )
            return RATE_STARS
        except ValueError:
            await update.message.reply_text("Please enter a valid Booking ID.")
            return RATE_BOOKING

    async def rate_stars(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=CLIENT_MENU)
            return ROLE_CHOICE
        stars_map = {"⭐": 1, "⭐⭐": 2, "⭐⭐⭐": 3, "⭐⭐⭐⭐": 4, "⭐⭐⭐⭐⭐": 5}
        context.user_data["rate_stars"] = stars_map.get(update.message.text, 5)
        await update.message.reply_text(
            "💬 Add a comment!\n(Or tap Skip)",
            reply_markup=ReplyKeyboardMarkup([["⏭ Skip", "❌ Cancel"]], resize_keyboard=True)
        )
        return RATE_COMMENT

    async def rate_comment(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=CLIENT_MENU)
            return ROLE_CHOICE
        comment = "" if update.message.text == "⏭ Skip" else update.message.text
        d = context.user_data
        self.db.add_rating(d["rate_booking_id"], d["rate_venue_id"], update.effective_user.id, d["rate_stars"], comment)
        await update.message.reply_text(
            f"✅ *Rating Submitted!*\n\n{'⭐' * d['rate_stars']} ({d['rate_stars']}/5)\n💬 {comment if comment else 'No comment'}\n\nThank you!",
            parse_mode="Markdown", reply_markup=CLIENT_MENU
        )
        return ROLE_CHOICE

    # ── AI Recommend ──────────────────────────────────────────────────────
    async def ai_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🤖 *AI Venue Recommender*\n\nHow many guests?",
            parse_mode="Markdown", reply_markup=CANCEL_KEYBOARD
        )
        return AI_GUESTS

    async def ai_guests(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=CLIENT_MENU)
            return ROLE_CHOICE
        try:
            context.user_data["ai_guests"] = int(update.message.text)
            await update.message.reply_text("💵 Budget per seat in USD? (e.g. 100)", reply_markup=CANCEL_KEYBOARD)
            return AI_BUDGET
        except ValueError:
            await update.message.reply_text("Please enter a valid number.")
            return AI_GUESTS

    async def ai_budget(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=CLIENT_MENU)
            return ROLE_CHOICE
        try:
            context.user_data["ai_budget"] = float(update.message.text)
            await update.message.reply_text(
                "📅 Wedding date? (DD/MM/YYYY or Skip)",
                reply_markup=ReplyKeyboardMarkup([["⏭ Skip", "❌ Cancel"]], resize_keyboard=True)
            )
            return AI_DATE
        except ValueError:
            await update.message.reply_text("Please enter a valid number.")
            return AI_BUDGET

    async def ai_date(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=CLIENT_MENU)
            return ROLE_CHOICE
        text = update.message.text
        context.user_data["ai_date"] = None if text == "⏭ Skip" else text

        d = context.user_data

        if not self.advisor:
            from ai import VenueAdvisor
            self.advisor = VenueAdvisor(self.db)

        best, reason = self.advisor.advise_venue(
            d["ai_guests"], d["ai_budget"], d.get("ai_date")
        )

        if not best:
            await update.message.reply_text(
                "❌ No venues found matching your requirements.\n\nTry increasing your budget or reducing guest count.",
                reply_markup=CLIENT_MENU
            )
            return ROLE_CHOICE

        amenities = []
        if best[11]: amenities.append("🍽 Catering")
        if best[12]: amenities.append("🎵 Music")
        if best[13]: amenities.append("💐 Decoration")

        avg_rating, rating_count = self.db.get_venue_average_rating(best[0])
        stars = "⭐" * int(avg_rating) if avg_rating > 0 else "No ratings yet"
        total_estimate = best[7] * d["ai_guests"]
        down_estimate = total_estimate * 0.50

        msg = (
            f"🤖 *AI Venue Advice — Best Match:*\n\n"
            f"🏆 *{best[3]}*\n"
            f"👤 {best[2]} | 📞 {best[8]}\n"
            f"📍 {best[4]}\n"
            f"📝 {best[5]}\n"
            f"👥 Capacity: {best[6]} guests\n"
            f"💵 Price: ${best[7]}/seat\n"
            f"💰 Total estimate: ${total_estimate:.0f}\n"
            f"📊 Down Payment (50%): ${down_estimate:.0f}\n"
            f"✨ Amenities: {', '.join(amenities) if amenities else 'None'}\n"
            f"⭐ Rating: {stars} ({avg_rating}/5 from {rating_count} reviews)\n\n"
            f"📌 *Why recommended:*\n{reason}"
        )

        if best[14]:
            await update.message.reply_photo(photo=best[14], caption=msg, parse_mode="Markdown", reply_markup=CLIENT_MENU)
        else:
            await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=CLIENT_MENU)

        return ROLE_CHOICE

    # ── Rate a Venue ──────────────────────────────────────────────────────
    async def rate_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_id = update.effective_user.id
        bookings = self.db.get_client_bookings(telegram_id)
        ratable = [b for b in bookings if b[7] == "Confirmed" and not self.db.has_rated(b[0])]
        if not ratable:
            await update.message.reply_text("⭐ No confirmed bookings to rate yet!", reply_markup=CLIENT_MENU)
            return ROLE_CHOICE
        msg = "⭐ *Select a Booking to Rate:*\n\n"
        for b in ratable:
            msg += f"*Booking #{b[0]}* — {b[1]}\n   📅 {b[2]} | 💑 {b[8]}\n\n"
        msg += "Enter the Booking ID:"
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=CANCEL_KEYBOARD)
        return RATE_BOOKING

    async def rate_booking(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=CLIENT_MENU)
            return ROLE_CHOICE
        try:
            booking_id = int(update.message.text)
            booking = self.db.get_booking_by_id(booking_id)
            if not booking:
                await update.message.reply_text("Booking not found.")
                return RATE_BOOKING
            context.user_data["rate_booking_id"] = booking_id
            context.user_data["rate_venue_id"] = booking[4]
            keyboard = [["⭐", "⭐⭐", "⭐⭐⭐"], ["⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], ["❌ Cancel"]]
            await update.message.reply_text(
                f"⭐ *Rate {booking[5]}*\n\nHow many stars?",
                parse_mode="Markdown",
                reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            )
            return RATE_STARS
        except ValueError:
            await update.message.reply_text("Please enter a valid Booking ID.")
            return RATE_BOOKING

    async def rate_stars(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=CLIENT_MENU)
            return ROLE_CHOICE
        stars_map = {"⭐": 1, "⭐⭐": 2, "⭐⭐⭐": 3, "⭐⭐⭐⭐": 4, "⭐⭐⭐⭐⭐": 5}
        context.user_data["rate_stars"] = stars_map.get(update.message.text, 5)
        await update.message.reply_text(
            "💬 Add a comment!\n(Or tap Skip)",
            reply_markup=ReplyKeyboardMarkup([["⏭ Skip", "❌ Cancel"]], resize_keyboard=True)
        )
        return RATE_COMMENT

    async def rate_comment(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=CLIENT_MENU)
            return ROLE_CHOICE
        comment = "" if update.message.text == "⏭ Skip" else update.message.text
        d = context.user_data
        self.db.add_rating(d["rate_booking_id"], d["rate_venue_id"], update.effective_user.id, d["rate_stars"], comment)
        await update.message.reply_text(
            f"✅ *Rating Submitted!*\n\n{'⭐' * d['rate_stars']} ({d['rate_stars']}/5)\n💬 {comment if comment else 'No comment'}\n\nThank you!",
            parse_mode="Markdown", reply_markup=CLIENT_MENU
        )
        return ROLE_CHOICE

    # ── AI Recommend ──────────────────────────────────────────────────────
    async def ai_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🤖 *AI Venue Recommender*\n\nHow many guests?",
            parse_mode="Markdown", reply_markup=CANCEL_KEYBOARD
        )
        return AI_GUESTS

    async def ai_guests(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=CLIENT_MENU)
            return ROLE_CHOICE
        try:
            context.user_data["ai_guests"] = int(update.message.text)
            await update.message.reply_text("💵 Budget per seat in USD? (e.g. 100)", reply_markup=CANCEL_KEYBOARD)
            return AI_BUDGET
        except ValueError:
            await update.message.reply_text("Please enter a valid number.")
            return AI_GUESTS

    async def ai_budget(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=CLIENT_MENU)
            return ROLE_CHOICE
        try:
            context.user_data["ai_budget"] = float(update.message.text)
            await update.message.reply_text(
                "📅 Wedding date? (DD/MM/YYYY or Skip)",
                reply_markup=ReplyKeyboardMarkup([["⏭ Skip", "❌ Cancel"]], resize_keyboard=True)
            )
            return AI_DATE
        except ValueError:
            await update.message.reply_text("Please enter a valid number.")
            return AI_BUDGET