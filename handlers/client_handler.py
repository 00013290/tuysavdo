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
    get_client_menu
)
from translations import t, TRANSLATIONS

CLIENT_MINIAPP_URL = "https://00013290.github.io/tuysavdo/miniapp/client.html"


def cancel_kb(lang):
    return ReplyKeyboardMarkup([[TRANSLATIONS[lang]["cancel"]]], resize_keyboard=True)

def skip_cancel_kb(lang):
    tr = TRANSLATIONS[lang]
    return ReplyKeyboardMarkup([[tr["skip"], tr["cancel"]]], resize_keyboard=True)


class ClientHandler:
    def __init__(self, database):
        self.db = database
        self.advisor = None

    def _lang(self, tid):
        try:
            return self.db.get_user_language(tid) or "en"
        except:
            return "en"

    def _t(self, tid, key, **kwargs):
        return t(tid, key, self.db, **kwargs)

    def set_advisor(self, advisor):
        self.advisor = advisor

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        tid = update.effective_user.id
        lang = self._lang(tid)

        menus = {
            "browse_venues": self.browse_venues,
            "book_venue_btn": self.book_venue_start,
            "ai_advice": self.ai_start,
            "my_bookings_client": self.my_bookings,
            "rate_venue": self.rate_start,
            "track_bookings": self.open_dashboard,
        }

        for key, handler in menus.items():
            btns = [TRANSLATIONS[l][key] for l in TRANSLATIONS]
            if text in btns:
                return await handler(update, context)

        await update.message.reply_text(self._t(tid, "choose_option"), reply_markup=get_client_menu(lang))
        return ROLE_CHOICE

    async def open_dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        bookings = self.db.get_client_bookings(tid)
        venues = self.db.get_all_venues()
        total = len(bookings)
        confirmed = len([b for b in bookings if b[7]=="Confirmed"])
        pending = len([b for b in bookings if b[7]=="Pending"])
        spent = sum(b[4] for b in bookings if b[7]=="Confirmed")
        data = {
            "stats": {"total": total, "confirmed": confirmed, "pending": pending, "spent": round(spent, 2)},
            "bookings": [{"id": b[0], "venue": b[1], "date": b[2], "guests": b[3],
                          "total": b[4], "status": b[7], "couple": b[8], "payment": b[6], "downPayment": b[10]}
                         for b in bookings[:20]],
            "venues": [{"name": v[3], "address": v[4], "capacity": v[6], "price": v[7],
                        "amenities": {"catering": bool(v[11]), "music": bool(v[12]), "decoration": bool(v[13])}}
                       for v in venues]
        }
        encoded = base64.b64encode(json.dumps(data).encode()).decode()
        url = f"{CLIENT_MINIAPP_URL}?data={encoded}"
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🌐 Open Client Dashboard", web_app=WebAppInfo(url=url))]])
        await update.message.reply_text("📊 Open your Client Dashboard:", reply_markup=kb)
        return ROLE_CHOICE

    # ── REGISTRATION ──────────────────────────────────────────────────────
    async def client_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        cancel_btns = [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]
        if update.message.text in cancel_btns:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=ReplyKeyboardRemove())
            return ROLE_CHOICE
        context.user_data["client_name"] = update.message.text
        await update.message.reply_text(self._t(tid, "ask_client_phone"), reply_markup=cancel_kb(lang))
        return CLIENT_PHONE

    async def client_phone(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        cancel_btns = [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]
        if update.message.text in cancel_btns:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=ReplyKeyboardRemove())
            return ROLE_CHOICE
        name = context.user_data["client_name"]
        phone = update.message.text
        self.db.add_client(tid, name, phone)
        self.db.register_user(tid, name, "", "client")
        await update.message.reply_text(
            self._t(tid, "client_registered", name=name, phone=phone),
            parse_mode="Markdown", reply_markup=get_client_menu(lang)
        )
        return ROLE_CHOICE

    # ── BROWSE VENUES ─────────────────────────────────────────────────────
    async def browse_venues(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        tr = TRANSLATIONS[lang]
        venues = self.db.get_all_venues_sorted()
        if not venues:
            await update.message.reply_text(self._t(tid, "no_venues"), reply_markup=get_client_menu(lang))
            return ROLE_CHOICE

        await update.message.reply_text(
            self._t(tid, "browse_title", count=len(venues)),
            parse_mode="Markdown", reply_markup=get_client_menu(lang)
        )

        for v in venues:
            amenities = []
            if v[11]: amenities.append(tr["amenity_catering"])
            if v[12]: amenities.append(tr["amenity_music"])
            if v[13]: amenities.append(tr["amenity_decoration"])
            avg_rating, rating_count = self.db.get_venue_average_rating(v[0])
            stars = "⭐" * int(avg_rating) if avg_rating > 0 else tr["no_ratings"]
            is_premium = self.db.is_venue_premium(v[0])
            premium_label = f"\n{tr['premium_badge']}" if is_premium else ""

            msg = premium_label + "\n" + self._t(tid, "venue_item",
                name=v[3], id=v[0], owner=v[2], address=v[4], desc=v[5],
                capacity=v[6], price=v[7], contact=v[8],
                amenities=", ".join(amenities) if amenities else tr["none"],
                stars=stars, avg=avg_rating, count=rating_count
            )

            if v[14]:
                await update.message.reply_photo(photo=v[14], caption=msg, parse_mode="Markdown")
            else:
                await update.message.reply_text(msg, parse_mode="Markdown")

        await update.message.reply_text(self._t(tid, "to_book"), reply_markup=get_client_menu(lang))
        return ROLE_CHOICE

    # ── BOOKING FLOW ──────────────────────────────────────────────────────
    async def book_venue_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        tr = TRANSLATIONS[lang]
        venues = self.db.get_all_venues_sorted()
        if not venues:
            await update.message.reply_text(self._t(tid, "no_venues"), reply_markup=get_client_menu(lang))
            return ROLE_CHOICE

        msg = self._t(tid, "select_venue")
        for v in venues:
            amenities = []
            if v[11]: amenities.append(tr["amenity_catering"])
            if v[12]: amenities.append(tr["amenity_music"])
            if v[13]: amenities.append(tr["amenity_decoration"])
            avg_rating, _ = self.db.get_venue_average_rating(v[0])
            stars = "⭐" * int(avg_rating) if avg_rating > 0 else ""
            amenities_text = " ".join([tr["amenity_catering"][:2] if v[11] else "",
                                       tr["amenity_music"][:2] if v[12] else "",
                                       tr["amenity_decoration"][:2] if v[13] else ""])
            is_premium = self.db.is_venue_premium(v[0])
            premium_tag = f" {tr['premium_badge']}" if is_premium else ""
            msg += self._t(tid, "venue_list_item",
                id=v[0], name=v[3] + premium_tag, stars=stars,
                capacity=v[6], price=v[7],
                amenities=amenities_text.strip() or tr["none"]
            )

        msg += self._t(tid, "enter_venue_id")
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=cancel_kb(lang))
        return BOOK_VENUE

    async def book_venue(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        cancel_btns = [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]
        if update.message.text in cancel_btns:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=get_client_menu(lang))
            return ROLE_CHOICE
        try:
            venue_id = int(update.message.text)
            venue = self.db.get_venue_by_id(venue_id)
            if not venue:
                await update.message.reply_text(self._t(tid, "venue_not_found"))
                return BOOK_VENUE
            context.user_data["book_venue_id"] = venue_id
            context.user_data["book_venue_name"] = venue[3]
            context.user_data["book_venue_capacity"] = venue[6]
            context.user_data["book_price_per_seat"] = venue[7]
            await update.message.reply_text(
                self._t(tid, "venue_selected", name=venue[3], capacity=venue[6], price=venue[7]),
                parse_mode="Markdown", reply_markup=cancel_kb(lang)
            )
            return BOOK_DATE
        except ValueError:
            await update.message.reply_text(self._t(tid, "invalid_number"))
            return BOOK_VENUE

    async def book_date(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        cancel_btns = [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]
        if update.message.text in cancel_btns:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=get_client_menu(lang))
            return ROLE_CHOICE
        event_date = update.message.text
        venue_id = context.user_data["book_venue_id"]
        if not self.db.check_availability(venue_id, event_date):
            await update.message.reply_text(
                self._t(tid, "date_unavailable", date=event_date),
                parse_mode="Markdown", reply_markup=cancel_kb(lang)
            )
            return BOOK_DATE
        context.user_data["book_date"] = event_date
        await update.message.reply_text(
            self._t(tid, "date_available", date=event_date),
            parse_mode="Markdown", reply_markup=cancel_kb(lang)
        )
        return BOOK_GUESTS

    async def book_guests(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        cancel_btns = [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]
        if update.message.text in cancel_btns:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=get_client_menu(lang))
            return ROLE_CHOICE
        try:
            guests = int(update.message.text)
            capacity = context.user_data["book_venue_capacity"]
            if guests > capacity:
                await update.message.reply_text(
                    self._t(tid, "capacity_exceeded", capacity=capacity),
                    parse_mode="Markdown", reply_markup=cancel_kb(lang)
                )
                return BOOK_GUESTS
            context.user_data["book_guests"] = guests
            await update.message.reply_text(
                self._t(tid, "ask_couple_names"),
                parse_mode="Markdown", reply_markup=cancel_kb(lang)
            )
            return BOOK_COUPLE
        except ValueError:
            await update.message.reply_text(self._t(tid, "invalid_number"))
            return BOOK_GUESTS

    async def book_couple(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        cancel_btns = [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]
        if update.message.text in cancel_btns:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=get_client_menu(lang))
            return ROLE_CHOICE
        context.user_data["book_couple"] = update.message.text
        await update.message.reply_text(
            self._t(tid, "ask_wishes"),
            reply_markup=skip_cancel_kb(lang)
        )
        return BOOK_WISHES

    async def book_wishes(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        skip_btns = [TRANSLATIONS[l]["skip"] for l in TRANSLATIONS]
        cancel_btns = [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]
        if update.message.text in cancel_btns:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=get_client_menu(lang))
            return ROLE_CHOICE
        context.user_data["book_wishes"] = "" if update.message.text in skip_btns else update.message.text

        d = context.user_data
        total_cost = d["book_guests"] * d["book_price_per_seat"]
        down_payment = round(total_cost * 0.50, 2)
        tr = TRANSLATIONS[lang]

        kb = ReplyKeyboardMarkup([[tr["cash"], tr["card"]], [tr["cancel"]]], resize_keyboard=True)
        await update.message.reply_text(
            self._t(tid, "payment_summary",
                guests=d["book_guests"], price=d["book_price_per_seat"],
                total=f"{total_cost:.2f}", down=f"{down_payment:.2f}"),
            parse_mode="Markdown", reply_markup=kb
        )
        return BOOK_PAYMENT

    async def book_payment(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        tr = TRANSLATIONS[lang]
        cancel_btns = [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]
        cash_btns = [TRANSLATIONS[l]["cash"] for l in TRANSLATIONS]
        if update.message.text in cancel_btns:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=get_client_menu(lang))
            return ROLE_CHOICE

        payment_method = "cash" if update.message.text in cash_btns else "card"
        d = context.user_data
        client_name = self.db.get_client_name(tid)
        client_phone = self.db.get_client_phone(tid)

        commission, total_cost, down_payment = self.db.add_booking(
            tid, client_name, client_phone,
            d["book_venue_id"], d["book_venue_name"],
            d["book_date"], d["book_guests"],
            d["book_price_per_seat"], payment_method,
            d["book_couple"], d["book_wishes"]
        )
        self.db.increment_venue_bookings(d["book_venue_id"])

        method_label = tr["cash"] if payment_method == "cash" else tr["card"]
        wishes_text = d["book_wishes"] if d["book_wishes"] else tr["none"]

        await update.message.reply_text(
            self._t(tid, "booking_sent",
                venue=d["book_venue_name"], date=d["book_date"],
                couple=d["book_couple"], guests=d["book_guests"],
                wishes=wishes_text, total=f"{total_cost:.2f}",
                down=f"{down_payment:.2f}", method=method_label),
            parse_mode="Markdown", reply_markup=get_client_menu(lang)
        )

        # Notify venue owner in their language
        try:
            venue = self.db.get_venue_by_id(d["book_venue_id"])
            if venue:
                owner_tid = venue[1]
                owner_lang = self._lang(owner_tid)
                owner_tr = TRANSLATIONS[owner_lang]
                owner_method = owner_tr["cash"] if payment_method == "cash" else owner_tr["card"]
                icon = "💵" if payment_method == "cash" else "💳"
                msg = t(owner_tid, "new_booking_notification", self.db,
                    client=client_name, phone=client_phone,
                    couple=d["book_couple"], date=d["book_date"],
                    guests=d["book_guests"], wishes=wishes_text,
                    total=f"{total_cost:.2f}", down=f"{down_payment:.2f}",
                    method=owner_method
                )
                await context.bot.send_message(chat_id=owner_tid, text=msg, parse_mode="Markdown")
        except: pass

        return ROLE_CHOICE

    # ── MY BOOKINGS ───────────────────────────────────────────────────────
    async def my_bookings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        bookings = self.db.get_client_bookings(tid)
        if not bookings:
            await update.message.reply_text(self._t(tid, "no_bookings_client"), reply_markup=get_client_menu(lang))
            return ROLE_CHOICE

        msg = self._t(tid, "my_bookings_title")
        for b in bookings:
            status_icon = "✅" if b[7]=="Confirmed" else "❌" if b[7]=="Rejected" else "⏳"
            msg += self._t(tid, "booking_item_client",
                id=b[0], venue=b[1], date=b[2], couple=b[8],
                guests=b[3], total=f"{b[4]:.2f}", down=f"{b[10]:.2f}",
                method=b[6], status_icon=status_icon, status=b[7]
            )
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=get_client_menu(lang))
        return ROLE_CHOICE

    # ── RATE A VENUE ──────────────────────────────────────────────────────
    async def rate_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        bookings = self.db.get_client_bookings(tid)
        ratable = [b for b in bookings if b[7]=="Confirmed" and not self.db.has_rated(b[0])]
        if not ratable:
            await update.message.reply_text(self._t(tid, "no_bookings_to_rate"), reply_markup=get_client_menu(lang))
            return ROLE_CHOICE

        msg = self._t(tid, "rate_select")
        for b in ratable:
            msg += self._t(tid, "rate_booking_item", id=b[0], venue=b[1], date=b[2], couple=b[8])
        msg += self._t(tid, "enter_booking_id")
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=cancel_kb(lang))
        return RATE_BOOKING

    async def rate_booking(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        cancel_btns = [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]
        if update.message.text in cancel_btns:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=get_client_menu(lang))
            return ROLE_CHOICE
        try:
            booking_id = int(update.message.text)
            booking = self.db.get_booking_by_id(booking_id)
            if not booking:
                await update.message.reply_text(self._t(tid, "booking_not_found"))
                return RATE_BOOKING
            context.user_data["rate_booking_id"] = booking_id
            context.user_data["rate_venue_id"] = booking[4]
            kb = ReplyKeyboardMarkup([
                ["⭐", "⭐⭐", "⭐⭐⭐"],
                ["⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
                [TRANSLATIONS[lang]["cancel"]]
            ], resize_keyboard=True)
            await update.message.reply_text(
                self._t(tid, "rate_stars_prompt", venue=booking[5]),
                parse_mode="Markdown", reply_markup=kb
            )
            return RATE_STARS
        except ValueError:
            await update.message.reply_text(self._t(tid, "invalid_number"))
            return RATE_BOOKING

    async def rate_stars(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        cancel_btns = [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]
        if update.message.text in cancel_btns:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=get_client_menu(lang))
            return ROLE_CHOICE
        stars_map = {"⭐": 1, "⭐⭐": 2, "⭐⭐⭐": 3, "⭐⭐⭐⭐": 4, "⭐⭐⭐⭐⭐": 5}
        context.user_data["rate_stars"] = stars_map.get(update.message.text, 5)
        await update.message.reply_text(
            self._t(tid, "rate_comment_prompt"),
            reply_markup=skip_cancel_kb(lang)
        )
        return RATE_COMMENT

    async def rate_comment(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        skip_btns = [TRANSLATIONS[l]["skip"] for l in TRANSLATIONS]
        cancel_btns = [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]
        if update.message.text in cancel_btns:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=get_client_menu(lang))
            return ROLE_CHOICE
        comment = "" if update.message.text in skip_btns else update.message.text
        d = context.user_data
        self.db.add_rating(d["rate_booking_id"], d["rate_venue_id"], tid, d["rate_stars"], comment)
        tr = TRANSLATIONS[lang]
        await update.message.reply_text(
            self._t(tid, "rating_submitted",
                stars="⭐" * d["rate_stars"], count=d["rate_stars"],
                comment=comment if comment else tr["none"]),
            parse_mode="Markdown", reply_markup=get_client_menu(lang)
        )
        return ROLE_CHOICE

    # ── AI ADVICE ─────────────────────────────────────────────────────────
    async def ai_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        await update.message.reply_text(
            self._t(tid, "ai_start"),
            parse_mode="Markdown", reply_markup=cancel_kb(lang)
        )
        return AI_GUESTS

    async def ai_guests(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        cancel_btns = [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]
        if update.message.text in cancel_btns:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=get_client_menu(lang))
            return ROLE_CHOICE
        try:
            context.user_data["ai_guests"] = int(update.message.text)
            await update.message.reply_text(self._t(tid, "ai_ask_budget"), reply_markup=cancel_kb(lang))
            return AI_BUDGET
        except ValueError:
            await update.message.reply_text(self._t(tid, "invalid_number"))
            return AI_GUESTS

    async def ai_budget(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        cancel_btns = [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]
        if update.message.text in cancel_btns:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=get_client_menu(lang))
            return ROLE_CHOICE
        try:
            context.user_data["ai_budget"] = float(update.message.text)
            await update.message.reply_text(self._t(tid, "ai_ask_date"), reply_markup=skip_cancel_kb(lang))
            return AI_DATE
        except ValueError:
            await update.message.reply_text(self._t(tid, "invalid_number"))
            return AI_BUDGET

    async def ai_date(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        tr = TRANSLATIONS[lang]
        skip_btns = [TRANSLATIONS[l]["skip"] for l in TRANSLATIONS]
        cancel_btns = [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]
        if update.message.text in cancel_btns:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=get_client_menu(lang))
            return ROLE_CHOICE
        context.user_data["ai_date"] = None if update.message.text in skip_btns else update.message.text

        d = context.user_data
        if not self.advisor:
            from ai import VenueAdvisor
            self.advisor = VenueAdvisor(self.db)

        best, _ = self.advisor.advise_venue(d["ai_guests"], d["ai_budget"], d.get("ai_date"))

        if not best:
            await update.message.reply_text(self._t(tid, "ai_no_match"), reply_markup=get_client_menu(lang))
            return ROLE_CHOICE

        amenities = []
        if best[11]: amenities.append(tr["amenity_catering"])
        if best[12]: amenities.append(tr["amenity_music"])
        if best[13]: amenities.append(tr["amenity_decoration"])

        avg_rating, rating_count = self.db.get_venue_average_rating(best[0])
        stars = "⭐" * int(avg_rating) if avg_rating > 0 else tr["no_ratings"]
        total_estimate = best[7] * d["ai_guests"]
        down_estimate = total_estimate * 0.50

        amenities_text = ", ".join(amenities) if amenities else tr["none"]

        reason = self._t(tid, "ai_reason",
            price=best[7], capacity=best[6],
            stars=stars, avg=avg_rating, count=rating_count,
            amenities=amenities_text
        )

        msg = self._t(tid, "ai_result",
            name=best[3], owner=best[2], contact=best[8],
            address=best[4], desc=best[5], capacity=best[6],
            price=best[7], total=f"{total_estimate:.0f}",
            down=f"{down_estimate:.0f}", amenities=amenities_text,
            stars=stars, avg=avg_rating, count=rating_count, reason=reason
        )

        if best[14]:
            await update.message.reply_photo(photo=best[14], caption=msg, parse_mode="Markdown", reply_markup=get_client_menu(lang))
        else:
            await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=get_client_menu(lang))

        return ROLE_CHOICE