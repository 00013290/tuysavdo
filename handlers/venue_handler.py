import json
import base64
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import ContextTypes, ConversationHandler
from handlers.start_handler import (
    ROLE_CHOICE,
    VENUE_OWNER_NAME, VENUE_NAME, VENUE_ADDRESS, VENUE_DESC,
    VENUE_CAPACITY, VENUE_PRICE, VENUE_CONTACT, VENUE_LOCATION, VENUE_AMENITIES,
    VENUE_PHOTO, VENUE_EXTRA_AMENITIES, VENUE_PAYMENT_DETAILS, VENUE_UPDATE_FIELD, VENUE_UPDATE_VALUE, VENUE_LOCATION,
    VENUE_MENU, get_venue_menu
)

VENUE_MINIAPP_URL = "https://00013290.github.io/tuysavdo/miniapp/venue.html"
CANCEL_KEYBOARD = ReplyKeyboardMarkup([["❌ Cancel"]], resize_keyboard=True)

# venue columns:
# 0=id, 1=telegram_id, 2=owner_name, 3=venue_name, 4=address
# 5=description, 6=capacity, 7=price_per_seat, 8=contact
# 9=latitude, 10=longitude, 11=has_catering, 12=has_music
# 13=has_decoration, 14=photo_id, 15=payment_details


class VenueHandler:
    def __init__(self, database):
        self.db = database

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        telegram_id = update.effective_user.id

        if text == "🏛 My Venue":
            return await self.my_venue(update, context)
        elif text == "✏️ Edit Venue":
            return await self.edit_venue_start(update, context)
        elif text == "📋 My Bookings":
            return await self.my_bookings(update, context)
        elif text == "📊 My Stats":
            return await self.my_stats(update, context)
        elif text == "🗓 Availability":
            return await self.my_availability(update, context)
        elif text == "⭐ My Ratings":
            return await self.my_ratings(update, context)
        elif text == "🌐 My Dashboard":
            return await self.open_dashboard(update, context)
        else:
            await update.message.reply_text("Please choose an option.", reply_markup=get_venue_menu(telegram_id))
            return ROLE_CHOICE

    async def open_dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_id = update.effective_user.id
        venue = self.db.get_venue_by_telegram_id(telegram_id)
        data = {"bookings": [], "calendar": [], "ratings": [], "stats": {}, "venue": {}}

        if venue:
            bookings = self.db.get_venue_bookings(venue[0])
            booked_dates = self.db.get_booked_dates(venue[0])
            ratings = self.db.get_venue_ratings(venue[0])
            avg_rating, rating_count = self.db.get_venue_average_rating(venue[0])

            data = {
                "venue": {"name": venue[3], "capacity": venue[6], "price": venue[7]},
                "stats": {
                    "total": len(bookings),
                    "confirmed": len([b for b in bookings if b[7] == "Confirmed"]),
                    "pending": len([b for b in bookings if b[7] == "Pending"]),
                    "rejected": len([b for b in bookings if b[7] == "Rejected"]),
                    "revenue": round(sum(b[4] for b in bookings), 2),
                    "avgRating": avg_rating,
                    "ratingCount": rating_count
                },
                "bookings": [{"id": b[0], "client": b[1], "date": b[2], "guests": b[3],
                              "total": b[4], "status": b[7], "couple": b[8], "payment": b[6]} for b in bookings[:20]],
                "calendar": [{"date": d} for d in booked_dates],
                "ratings": [{"stars": r[0], "comment": r[1], "date": r[2][:10]} for r in ratings[:10]]
            }

        encoded = base64.b64encode(json.dumps(data).encode()).decode()
        url = f"{VENUE_MINIAPP_URL}?data={encoded}"
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🌐 Open Venue Dashboard", web_app=WebAppInfo(url=url))]])
        await update.message.reply_text("📊 Open your Venue Dashboard:", reply_markup=keyboard)
        return ROLE_CHOICE

    # ── Registration ─────────────────────────────────────────────────────
    async def venue_owner_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=ReplyKeyboardRemove())
            return ROLE_CHOICE
        context.user_data["owner_name"] = update.message.text
        await update.message.reply_text("What is the name of your venue?", reply_markup=CANCEL_KEYBOARD)
        return VENUE_NAME

    async def venue_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=ReplyKeyboardRemove())
            return ROLE_CHOICE
        context.user_data["venue_name"] = update.message.text
        await update.message.reply_text("What is your venue's address?", reply_markup=CANCEL_KEYBOARD)
        return VENUE_ADDRESS

    async def venue_address(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=ReplyKeyboardRemove())
            return ROLE_CHOICE
        context.user_data["venue_address"] = update.message.text
        await update.message.reply_text(
            "Add a short description of your venue:\n(e.g. Elegant wedding hall with garden and VIP rooms)",
            reply_markup=CANCEL_KEYBOARD
        )
        return VENUE_DESC

    async def venue_desc(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=ReplyKeyboardRemove())
            return ROLE_CHOICE
        context.user_data["venue_desc"] = update.message.text
        await update.message.reply_text("Maximum capacity? (e.g. 500)", reply_markup=CANCEL_KEYBOARD)
        return VENUE_CAPACITY

    async def venue_capacity(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=ReplyKeyboardRemove())
            return ROLE_CHOICE
        try:
            context.user_data["venue_capacity"] = int(update.message.text)
            await update.message.reply_text("Price per seat in USD? (e.g. 100)", reply_markup=CANCEL_KEYBOARD)
            return VENUE_PRICE
        except ValueError:
            await update.message.reply_text("Please enter a valid number.")
            return VENUE_CAPACITY

    async def venue_price(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=ReplyKeyboardRemove())
            return ROLE_CHOICE
        try:
            context.user_data["venue_price"] = float(update.message.text)
            await update.message.reply_text("Your contact number?", reply_markup=CANCEL_KEYBOARD)
            return VENUE_CONTACT
        except ValueError:
            await update.message.reply_text("Please enter a valid number.")
            return VENUE_PRICE

    async def venue_contact(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=ReplyKeyboardRemove())
            return ROLE_CHOICE
        context.user_data["venue_contact"] = update.message.text
        await update.message.reply_text(
            "📍 Please share your venue location!\n\nTap 📎 → Location → Send your location",
            reply_markup=CANCEL_KEYBOARD
        )
        return VENUE_LOCATION

    async def venue_location(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=ReplyKeyboardRemove())
            return ROLE_CHOICE
        if not update.message.location:
            await update.message.reply_text("⚠️ Please share your location using 📎 → Location")
            return VENUE_LOCATION

        context.user_data["venue_lat"] = update.message.location.latitude
        context.user_data["venue_lon"] = update.message.location.longitude
        context.user_data["has_catering"] = 0
        context.user_data["has_music"] = 0
        context.user_data["has_decoration"] = 0

        keyboard = [["✅ Catering", "✅ Music", "✅ Decoration"], ["✔️ Done", "❌ None of these"]]
        await update.message.reply_text(
            "🎊 What amenities does your venue offer?\n\nTap each to select, then ✔️ Done:\n\nSelected: *None yet*",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return VENUE_AMENITIES

    async def venue_amenities(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        if text == "✅ Catering":
            context.user_data["has_catering"] = 1
        elif text == "✅ Music":
            context.user_data["has_music"] = 1
        elif text == "✅ Decoration":
            context.user_data["has_decoration"] = 1

        if text in ["✔️ Done", "❌ None of these"]:
            if text == "❌ None of these":
                context.user_data["has_catering"] = 0
                context.user_data["has_music"] = 0
                context.user_data["has_decoration"] = 0
            await update.message.reply_text(
                "✨ Any additional services or amenities your venue offers?\n\n"
                "(e.g. Private parking, VIP rooms, outdoor garden, swimming pool, drone photography)\n\n"
                "Or tap Skip.",
                reply_markup=ReplyKeyboardMarkup([["⏭ Skip", "❌ Cancel"]], resize_keyboard=True)
            )
            return VENUE_EXTRA_AMENITIES

        selected = []
        if context.user_data.get("has_catering"): selected.append("🍽 Catering")
        if context.user_data.get("has_music"): selected.append("🎵 Music")
        if context.user_data.get("has_decoration"): selected.append("💐 Decoration")
        selected_text = ", ".join(selected) if selected else "None yet"

        keyboard = [["✅ Catering", "✅ Music", "✅ Decoration"], ["✔️ Done", "❌ None of these"]]
        await update.message.reply_text(
            f"✨ Selected: *{selected_text}*\n\nSelect more or tap ✔️ Done:",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return VENUE_AMENITIES

    async def venue_extra_amenities(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=ReplyKeyboardRemove())
            return ROLE_CHOICE
        context.user_data["extra_amenities"] = "" if update.message.text == "⏭ Skip" else update.message.text
        keyboard = ReplyKeyboardMarkup([["⏭ Skip Photo"]], resize_keyboard=True)
        await update.message.reply_text(
            "📸 Send a photo of your venue!\nOr tap Skip Photo.",
            reply_markup=keyboard
        )
        return VENUE_PHOTO

    async def venue_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        photo_id = ""
        if update.message.photo:
            photo_id = update.message.photo[-1].file_id
        context.user_data["photo_id"] = photo_id

        await update.message.reply_text(
            "💳 *Payment Details*\n\n"
            "Enter your bank card number or bank account details.\n"
            "Clients will use this to pay the 50% down payment.\n\n"
            "(e.g. Uzcard: 5614 1234 5678 9111 — Edem Ibragimov)",
            parse_mode="Markdown",
            reply_markup=CANCEL_KEYBOARD
        )
        return VENUE_PAYMENT_DETAILS

    async def venue_payment_details(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=ReplyKeyboardRemove())
            return ROLE_CHOICE

        d = context.user_data
        payment_details = update.message.text

        self.db.add_venue(
            update.effective_user.id,
            d["owner_name"], d["venue_name"],
            d["venue_address"], d["venue_desc"],
            d["venue_capacity"], d["venue_price"],
            d["venue_contact"],
            d.get("venue_lat", 0), d.get("venue_lon", 0),
            d.get("has_catering", 0),
            d.get("has_music", 0),
            d.get("has_decoration", 0),
            d.get("photo_id", ""),
            d.get("extra_amenities", ""),
            payment_details
        )
        self.db.register_user(update.effective_user.id, d["owner_name"], d["venue_name"], "venue")

        amenities = []
        if d.get("has_catering"): amenities.append("🍽 Catering")
        if d.get("has_music"): amenities.append("🎵 Music")
        if d.get("has_decoration"): amenities.append("💐 Decoration")

        await update.message.reply_text(
            f"✅ *Venue Registered Successfully!*\n\n"
            f"👤 Owner: {d['owner_name']}\n"
            f"🏛 Venue: {d['venue_name']}\n"
            f"📍 Address: {d['venue_address']}\n"
            f"📝 {d['venue_desc']}\n"
            f"👥 Capacity: {d['venue_capacity']} guests\n"
            f"💵 Price: ${d['venue_price']}/seat\n"
            f"📞 Contact: {d['venue_contact']}\n"
            f"✨ Amenities: {', '.join(amenities) if amenities else 'None'}\n"
            f"✨ Extra: {d.get('extra_amenities', 'None')}\n"
            f"💳 Payment details saved ✅\n\n"
            f"Clients can now find and book your venue!",
            parse_mode="Markdown",
            reply_markup=VENUE_MENU
        )
        return ROLE_CHOICE

    # ── My Venue ──────────────────────────────────────────────────────────
    async def my_venue(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_id = update.effective_user.id
        venue = self.db.get_venue_by_telegram_id(telegram_id)
        if not venue:
            await update.message.reply_text("You have no venue registered.", reply_markup=VENUE_MENU)
            return ROLE_CHOICE

        amenities = []
        if venue[11]: amenities.append("🍽 Catering")
        if venue[12]: amenities.append("🎵 Music")
        if venue[13]: amenities.append("💐 Decoration")

        avg_rating, rating_count = self.db.get_venue_average_rating(venue[0])
        stars = "⭐" * int(avg_rating) if avg_rating > 0 else "No ratings yet"

        msg = (
            f"🏛 *Your Venue:*\n\n"
            f"🏛 Name: {venue[3]}\n"
            f"📍 Address: {venue[4]}\n"
            f"📝 {venue[5]}\n"
            f"👥 Capacity: {venue[6]} guests\n"
            f"💵 Price: ${venue[7]}/seat\n"
            f"📞 Contact: {venue[8]}\n"
            f"✨ Amenities: {', '.join(amenities) if amenities else 'None'}\n"
            f"✨ Extra amenities: {venue[15] if venue[15] else 'None'}\n"
            f"💳 Payment: {venue[16] if venue[16] else 'Not set'}\n"
            f"⭐ Rating: {stars} ({avg_rating}/5 from {rating_count} reviews)"
        )

        if venue[14]:
            await update.message.reply_photo(photo=venue[14], caption=msg, parse_mode="Markdown", reply_markup=VENUE_MENU)
        else:
            await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=VENUE_MENU)
        return ROLE_CHOICE

    # ── Edit Venue ────────────────────────────────────────────────────────
    async def edit_venue_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        telegram_id = update.effective_user.id

        if text == "✏️ Edit Venue":
            keyboard = [
                ["📝 Description", "👥 Capacity"],
                ["💵 Price", "📞 Contact"],
                ["💳 Payment Details", "📸 Update Photo"],
                ["❌ Cancel"]
            ]
            await update.message.reply_text(
                "✏️ *Edit Venue*\n\nWhat would you like to update?",
                parse_mode="Markdown",
                reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            )
            return VENUE_UPDATE_FIELD

        elif text in ["📝 Description", "👥 Capacity", "💵 Price", "📞 Contact", "💳 Payment Details", "📸 Update Photo"]:
            field_map = {
                "📝 Description": "description",
                "👥 Capacity": "capacity",
                "💵 Price": "price_per_seat",
                "📞 Contact": "contact",
                "💳 Payment Details": "payment_details"
            }
            context.user_data["edit_field"] = text
            context.user_data["edit_field_key"] = field_map.get(text, "photo")
            if text == "📸 Update Photo":
                await update.message.reply_text("📸 Send your new venue photo:", reply_markup=ReplyKeyboardRemove())
            else:
                await update.message.reply_text(f"Enter new value for {text}:", reply_markup=CANCEL_KEYBOARD)
            return VENUE_UPDATE_VALUE

        elif text == "❌ Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=get_venue_menu(telegram_id))
            return ROLE_CHOICE

        else:
            return await self.save_edit(update, context)

    async def save_edit(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_id = update.effective_user.id
        field_key = context.user_data.get("edit_field_key")

        if update.message.text == "❌ Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=get_venue_menu(telegram_id))
            return ROLE_CHOICE

        if field_key == "photo":
            if update.message.photo:
                photo_id = update.message.photo[-1].file_id
                self.db.update_venue_photo(telegram_id, photo_id)
                await update.message.reply_text("✅ Photo updated!", reply_markup=get_venue_menu(telegram_id))
            else:
                await update.message.reply_text("Please send a photo.")
                return VENUE_UPDATE_VALUE
        else:
            self.db.update_venue(telegram_id, field_key, update.message.text)
            await update.message.reply_text(
                f"✅ {context.user_data.get('edit_field')} updated!",
                reply_markup=get_venue_menu(telegram_id)
            )
        return ROLE_CHOICE

    # ── Availability ──────────────────────────────────────────────────────
    async def my_availability(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_id = update.effective_user.id
        venue = self.db.get_venue_by_telegram_id(telegram_id)
        if not venue:
            await update.message.reply_text("You have no venue registered.", reply_markup=VENUE_MENU)
            return ROLE_CHOICE

        booked_dates = self.db.get_booked_dates(venue[0])
        if not booked_dates:
            await update.message.reply_text(
                "🗓 *Availability Calendar*\n\n✅ All dates are available!",
                parse_mode="Markdown", reply_markup=VENUE_MENU
            )
            return ROLE_CHOICE

        msg = "🗓 *Booked Dates:*\n\n"
        for date in booked_dates:
            msg += f"❌ {date}\n"
        msg += "\nAll other dates are ✅ available!"
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=VENUE_MENU)
        return ROLE_CHOICE

    # ── My Ratings ────────────────────────────────────────────────────────
    async def my_ratings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_id = update.effective_user.id
        venue = self.db.get_venue_by_telegram_id(telegram_id)
        if not venue:
            await update.message.reply_text("You have no venue registered.", reply_markup=VENUE_MENU)
            return ROLE_CHOICE

        avg_rating, count = self.db.get_venue_average_rating(venue[0])
        ratings = self.db.get_venue_ratings(venue[0])

        if not ratings:
            await update.message.reply_text("⭐ No ratings yet.", reply_markup=VENUE_MENU)
            return ROLE_CHOICE

        stars = "⭐" * int(avg_rating)
        msg = f"⭐ *Your Ratings:*\n\nAverage: {stars} ({avg_rating}/5 from {count} reviews)\n\n"
        for r in ratings[:10]:
            msg += f"{'⭐' * r[0]} — {r[1] if r[1] else 'No comment'}\n   🕐 {r[2][:10]}\n\n"

        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=VENUE_MENU)
        return ROLE_CHOICE

    # ── My Bookings ───────────────────────────────────────────────────────
    async def my_bookings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_id = update.effective_user.id
        venue = self.db.get_venue_by_telegram_id(telegram_id)
        if not venue:
            await update.message.reply_text("You have no venue registered.", reply_markup=VENUE_MENU)
            return ROLE_CHOICE

        bookings = self.db.get_venue_bookings(venue[0])
        if not bookings:
            await update.message.reply_text("No bookings received yet.", reply_markup=VENUE_MENU)
            return ROLE_CHOICE

        await update.message.reply_text(
            f"📋 *Bookings Received ({len(bookings)} total):*",
            parse_mode="Markdown", reply_markup=VENUE_MENU
        )

        for b in bookings:
            # b: id, client_name, event_date, guest_count, total_cost, commission,
            #    payment_method, status, couple_names, wishes, down_payment, client_phone, placed_at
            booking_text = (
                f"🔹 *Booking #{b[0]}*\n"
                f"   👤 Client: {b[1]}\n"
                f"   📞 Phone: {b[11] if b[11] else 'Not provided'}\n"
                f"   💑 Couple: {b[8]}\n"
                f"   📅 Date: {b[2]}\n"
                f"   👥 Guests: {b[3]}\n"
                f"   ✨ Wishes: {b[9] if b[9] else 'None'}\n"
                f"   💰 Total: ${b[4]:.2f}\n"
                f"   📊 Down Payment (50%): ${b[10]:.2f}\n"
                f"   💳 Payment: {b[6].capitalize()}\n"
                f"   📊 Status: {b[7]}"
            )

            if b[7] == "Pending":
                keyboard = InlineKeyboardMarkup([[
                    InlineKeyboardButton("✅ Confirm", callback_data=f"confirm_{b[0]}"),
                    InlineKeyboardButton("❌ Reject", callback_data=f"reject_{b[0]}")
                ]])
                await update.message.reply_text(booking_text, parse_mode="Markdown", reply_markup=keyboard)
            elif b[7] == "Awaiting Payment":
                keyboard = InlineKeyboardMarkup([[
                    InlineKeyboardButton("✅ Payment Confirmed", callback_data=f"payment_confirmed_{b[0]}"),
                    InlineKeyboardButton("❌ Payment Failed", callback_data=f"payment_failed_{b[0]}")
                ]])
                await update.message.reply_text(booking_text, parse_mode="Markdown", reply_markup=keyboard)
            else:
                await update.message.reply_text(booking_text, parse_mode="Markdown")

        return ROLE_CHOICE

    # ── My Stats ──────────────────────────────────────────────────────────
    async def my_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_id = update.effective_user.id
        venue = self.db.get_venue_by_telegram_id(telegram_id)
        if not venue:
            await update.message.reply_text("You have no venue registered.", reply_markup=VENUE_MENU)
            return ROLE_CHOICE

        bookings = self.db.get_venue_bookings(venue[0])
        total_revenue = sum(b[4] for b in bookings)
        confirmed = len([b for b in bookings if b[7] == "Confirmed"])
        pending = len([b for b in bookings if b[7] == "Pending"])
        rejected = len([b for b in bookings if b[7] == "Rejected"])
        avg_rating, rating_count = self.db.get_venue_average_rating(venue[0])
        stars = "⭐" * int(avg_rating) if avg_rating > 0 else "No ratings yet"

        await update.message.reply_text(
            f"📊 *Your Statistics:*\n\n"
            f"🏛 Venue: {venue[3]}\n"
            f"👥 Capacity: {venue[6]} guests\n"
            f"💵 Price: ${venue[7]}/seat\n"
            f"⭐ Rating: {stars} ({avg_rating}/5)\n\n"
            f"📋 Total Bookings: {len(bookings)}\n"
            f"✅ Confirmed: {confirmed}\n"
            f"⏳ Pending: {pending}\n"
            f"❌ Rejected: {rejected}\n"
            f"💰 Total Revenue: ${total_revenue:.2f}",
            parse_mode="Markdown", reply_markup=VENUE_MENU
        )
        return ROLE_CHOICE

    # ── Handle Callback ───────────────────────────────────────────────────
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        data = query.data

        # Step 1: Venue confirms booking request → sends payment details to client
        if data.startswith("confirm_"):
            booking_id = int(data.split("_")[1])
            booking = self.db.get_booking_by_id(booking_id)
            self.db.update_booking_status(booking_id, "Awaiting Payment")

            # Get venue payment details
            payment_details = self.db.get_venue_payment_details(booking[4])

            await query.edit_message_text(
                f"✅ *Booking #{booking_id} Confirmed!*\n\n"
                f"Waiting for client to make the down payment.",
                parse_mode="Markdown"
            )
            try:
                payment_icon = "💵" if booking[11] == "cash" else "💳"
                await context.bot.send_message(
                    chat_id=booking[1],
                    text=f"🎊 *Your booking #{booking_id} has been accepted!*\n\n"
                         f"🏛 Venue: {booking[5]}\n"
                         f"📅 Date: {booking[6]}\n"
                         f"💑 Couple: {booking[13]}\n"
                         f"👥 Guests: {booking[7]}\n"
                         f"💰 Total Cost: ${booking[8]:.2f}\n\n"
                         f"📊 *Please pay the 50% down payment:*\n"
                         f"💳 Amount: *${booking[10]:.2f}*\n"
                         f"{payment_icon} Method: {booking[11].capitalize()}\n"
                         f"🏦 Payment Details:\n*{payment_details}*\n\n"
                         f"After paying, tap the button below 👇",
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("💳 I've Paid the Down Payment", callback_data=f"paid_{booking_id}")
                    ]])
                )
            except:
                pass

        # Step 2: Client says they paid → notify venue owner
        elif data.startswith("paid_"):
            booking_id = int(data.split("_")[1])
            booking = self.db.get_booking_by_id(booking_id)
            self.db.update_booking_status(booking_id, "Payment Sent")

            await query.edit_message_text(
                f"✅ *Payment notification sent!*\n\n"
                f"Waiting for venue to confirm receipt of payment.",
                parse_mode="Markdown"
            )

            # Notify venue owner
            try:
                venue = self.db.get_venue_by_id(booking[4])
                if venue:
                    await context.bot.send_message(
                        chat_id=venue[1],
                        text=f"💳 *Payment Notification — Booking #{booking_id}*\n\n"
                             f"👤 Client: {booking[2]}\n"
                             f"📞 Phone: {booking[3]}\n"
                             f"💑 Couple: {booking[13]}\n"
                             f"📅 Date: {booking[6]}\n"
                             f"💰 Down Payment: ${booking[10]:.2f}\n\n"
                             f"Please check your account and confirm!",
                        parse_mode="Markdown",
                        reply_markup=InlineKeyboardMarkup([[
                            InlineKeyboardButton("✅ Payment Confirmed", callback_data=f"payment_confirmed_{booking_id}"),
                            InlineKeyboardButton("❌ Not Received", callback_data=f"payment_failed_{booking_id}")
                        ]])
                    )
            except:
                pass

        # Step 3: Venue confirms payment received → booking confirmed!
        elif data.startswith("payment_confirmed_"):
            booking_id = int(data.split("_")[2])
            booking = self.db.get_booking_by_id(booking_id)
            self.db.update_booking_status(booking_id, "Confirmed")

            await query.edit_message_text(
                f"✅ *Payment Confirmed! Booking #{booking_id} is now CONFIRMED!*",
                parse_mode="Markdown"
            )
            try:
                await context.bot.send_message(
                    chat_id=booking[1],
                    text=f"🎊 *Booking #{booking_id} is CONFIRMED!*\n\n"
                         f"🏛 Venue: {booking[5]}\n"
                         f"📅 Date: {booking[6]}\n"
                         f"💑 Couple: {booking[13]}\n\n"
                         f"Your wedding is booked! Congratulations! 🎉",
                    parse_mode="Markdown"
                )
            except:
                pass

        # Payment failed
        elif data.startswith("payment_failed_"):
            booking_id = int(data.split("_")[2])
            booking = self.db.get_booking_by_id(booking_id)
            self.db.update_booking_status(booking_id, "Awaiting Payment")

            await query.edit_message_text(
                f"❌ Payment not received for Booking #{booking_id}.\nWaiting for client to retry.",
                parse_mode="Markdown"
            )
            try:
                await context.bot.send_message(
                    chat_id=booking[1],
                    text=f"❌ *Payment not confirmed for Booking #{booking_id}*\n\n"
                         f"The venue couldn't verify your payment.\n"
                         f"Please check and try again.",
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("💳 I\'ve Paid Again", callback_data=f"paid_{booking_id}")
                    ]])
                )
            except:
                pass

        # Reject booking
        elif data.startswith("reject_"):
            booking_id = int(data.split("_")[1])
            booking = self.db.get_booking_by_id(booking_id)
            self.db.update_booking_status(booking_id, "Rejected")
            await query.edit_message_text(f"❌ *Booking #{booking_id} Rejected*", parse_mode="Markdown")
            try:
                await context.bot.send_message(
                    chat_id=booking[1],
                    text=f"❌ *Your booking #{booking_id} has been rejected.*\n\n"
                         f"🏛 Venue: {booking[5]}\n"
                         f"📅 Date: {booking[6]}\n\n"
                         f"Please try another venue.",
                    parse_mode="Markdown"
                )
            except:
                pass