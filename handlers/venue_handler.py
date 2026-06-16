import json
import base64
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import ContextTypes, ConversationHandler
from handlers.start_handler import (
    ROLE_CHOICE,
    VENUE_OWNER_NAME, VENUE_NAME, VENUE_ADDRESS, VENUE_DESC,
    VENUE_CAPACITY, VENUE_PRICE, VENUE_CONTACT, VENUE_LOCATION, VENUE_AMENITIES,
    VENUE_PHOTO, VENUE_EXTRA_AMENITIES, VENUE_PAYMENT_DETAILS,
    VENUE_UPDATE_FIELD, VENUE_UPDATE_VALUE,
    VENUE_PREMIUM, PREMIUM_PLAN, PREMIUM_PAY,
    get_venue_menu
)
from translations import t, TRANSLATIONS

VENUE_MINIAPP_URL = "https://00013290.github.io/tuysavdo/miniapp/venue.html"


def cancel_kb(lang):
    return ReplyKeyboardMarkup([[TRANSLATIONS[lang]["cancel"]]], resize_keyboard=True)

def skip_kb(lang):
    tr = TRANSLATIONS[lang]
    return ReplyKeyboardMarkup([[tr["skip"], tr["cancel"]]], resize_keyboard=True)

def skip_photo_kb(lang):
    return ReplyKeyboardMarkup([[TRANSLATIONS[lang]["skip_photo"]]], resize_keyboard=True)

def amenity_kb(lang):
    tr = TRANSLATIONS[lang]
    return ReplyKeyboardMarkup([
        [tr["catering"], tr["music"], tr["decoration"]],
        [tr["done"], tr["none_of_these"]]
    ], resize_keyboard=True)


class VenueHandler:
    def __init__(self, database):
        self.db = database

    def _lang(self, tid):
        try:
            return self.db.get_user_language(tid) or "en"
        except:
            return "en"

    def _t(self, tid, key, **kwargs):
        return t(tid, key, self.db, **kwargs)

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        tid = update.effective_user.id
        lang = self._lang(tid)

        menus = {
            "my_venue": self.my_venue,
            "edit_venue": self.edit_venue_start,
            "my_bookings": self.my_bookings,
            "my_stats": self.my_stats,
            "availability": self.my_availability,
            "my_ratings": self.my_ratings,
            "my_dashboard": self.open_dashboard,
            "upgrade_btn": self.show_premium,
        }

        for key, handler in menus.items():
            btns = [TRANSLATIONS[l][key] for l in TRANSLATIONS]
            if text in btns:
                return await handler(update, context)

        await update.message.reply_text(self._t(tid, "choose_option"), reply_markup=get_venue_menu(lang))
        return ROLE_CHOICE

    async def show_premium(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        tr = TRANSLATIONS[lang]
        venue = self.db.get_venue_by_telegram_id(tid)

        if venue and self.db.is_venue_premium(venue[0]):
            await update.message.reply_text(
                self._t(tid, "already_premium"),
                parse_mode="Markdown",
                reply_markup=get_venue_menu(lang)
            )
            return ROLE_CHOICE

        # Show benefits
        await update.message.reply_text(
            self._t(tid, "premium_benefits"),
            parse_mode="Markdown"
        )

        # Show plan selection keyboard
        kb = ReplyKeyboardMarkup([
            [tr["plan_basic"]],
            [tr["plan_standard"]],
            [tr["plan_vip"]],
            [tr["cancel"]]
        ], resize_keyboard=True)

        await update.message.reply_text(
            self._t(tid, "select_plan"),
            parse_mode="Markdown",
            reply_markup=kb
        )
        return PREMIUM_PLAN

    async def premium_plan_selected(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        tr = TRANSLATIONS[lang]
        text = update.message.text

        cancel_btns = [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]
        if text in cancel_btns:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=get_venue_menu(lang))
            return ROLE_CHOICE

        # Map plan to amount
        plan_map = {
            tr["plan_basic"]: ("Basic", "$25"),
            tr["plan_standard"]: ("Standard", "$50"),
            tr["plan_vip"]: ("VIP", "$75"),
        }
        # Also check other language variants safely
        for l in TRANSLATIONS:
            trl = TRANSLATIONS[l]
            try:
                plan_map[trl["plan_basic"]] = ("Basic 🥉", "$25")
                plan_map[trl["plan_standard"]] = ("Standard 🥈", "$50")
                plan_map[trl["plan_vip"]] = ("VIP 🥇", "$75")
            except KeyError:
                pass

        if text not in plan_map:
            await update.message.reply_text(self._t(tid, "choose_option"), reply_markup=get_venue_menu(lang))
            return ROLE_CHOICE

        plan_name, amount = plan_map[text]
        context.user_data["premium_plan"] = plan_name
        context.user_data["premium_amount"] = amount

        # Show payment instructions with I've Paid button
        kb = ReplyKeyboardMarkup([
            ["💳 I've Paid / To'ladim"],
            [tr["cancel"]]
        ], resize_keyboard=True)

        await update.message.reply_text(
            self._t(tid, "payment_instructions", plan=plan_name, amount=amount),
            parse_mode="Markdown",
            reply_markup=kb
        )
        return PREMIUM_PAY

    async def premium_payment_sent(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        tr = TRANSLATIONS[lang]
        text = update.message.text

        cancel_btns = [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]
        if text in cancel_btns:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=get_venue_menu(lang))
            return ROLE_CHOICE

        venue = self.db.get_venue_by_telegram_id(tid)
        if not venue:
            await update.message.reply_text(self._t(tid, "no_venue"), reply_markup=get_venue_menu(lang))
            return ROLE_CHOICE

        plan = context.user_data.get("premium_plan", "Unknown")
        amount = context.user_data.get("premium_amount", "Unknown")

        # Notify client
        await update.message.reply_text(
            self._t(tid, "premium_paid_client"),
            parse_mode="Markdown",
            reply_markup=get_venue_menu(lang)
        )

        # Notify admin
        try:
            from handlers.admin_handler import ADMIN_ID
            msg = (
                f"👑 *Premium Payment Request!*\n\n"
                f"🏛 Venue: {venue[3]}\n"
                f"👤 Owner: {venue[2]}\n"
                f"📞 Contact: {venue[8]}\n"
                f"📋 Plan: {plan}\n"
                f"💰 Amount: {amount}\n"
                f"🆔 Venue ID: {venue[0]}\n\n"
                f"Please verify payment and confirm!"
            )
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=msg,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        f"✅ Activate Premium — {venue[3]}",
                        callback_data=f"grant_premium_{venue[0]}_{plan.replace(' ', '_')}"
                    ),
                    InlineKeyboardButton(
                        "❌ Reject",
                        callback_data=f"reject_premium_{venue[0]}"
                    )
                ]])
            )
        except Exception as e:
            print(f"Admin notify error: {e}")

        return ROLE_CHOICE

    async def open_dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        venue = self.db.get_venue_by_telegram_id(tid)
        data = {"bookings": [], "calendar": [], "ratings": [], "stats": {}, "venue": {}}
        if venue:
            bookings = self.db.get_venue_bookings(venue[0])
            booked_dates = self.db.get_booked_dates(venue[0])
            ratings = self.db.get_venue_ratings(venue[0])
            avg_rating, rating_count = self.db.get_venue_average_rating(venue[0])
            data = {
                "venue": {"name": venue[3], "capacity": venue[6], "price": venue[7]},
                "stats": {"total": len(bookings), "confirmed": len([b for b in bookings if b[7]=="Confirmed"]),
                          "pending": len([b for b in bookings if b[7]=="Pending"]),
                          "rejected": len([b for b in bookings if b[7]=="Rejected"]),
                          "revenue": round(sum(b[4] for b in bookings), 2),
                          "avgRating": avg_rating, "ratingCount": rating_count},
                "bookings": [{"id": b[0], "client": b[1], "date": b[2], "guests": b[3],
                              "total": b[4], "status": b[7], "couple": b[8], "payment": b[6]} for b in bookings[:20]],
                "calendar": [{"date": d} for d in booked_dates],
                "ratings": [{"stars": r[0], "comment": r[1], "date": r[2][:10]} for r in ratings[:10]]
            }
        encoded = base64.b64encode(json.dumps(data).encode()).decode()
        url = f"{VENUE_MINIAPP_URL}?data={encoded}"
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🌐 Open Venue Dashboard", web_app=WebAppInfo(url=url))]])
        await update.message.reply_text(self._t(tid, "open_dashboard"), reply_markup=kb)
        return ROLE_CHOICE

    # ── REGISTRATION ──────────────────────────────────────────────────────
    async def venue_owner_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        if update.message.text in [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=ReplyKeyboardRemove())
            return ROLE_CHOICE
        context.user_data["owner_name"] = update.message.text
        await update.message.reply_text(self._t(tid, "ask_venue_name"), reply_markup=cancel_kb(lang))
        return VENUE_NAME

    async def venue_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        if update.message.text in [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=ReplyKeyboardRemove())
            return ROLE_CHOICE
        context.user_data["venue_name"] = update.message.text
        await update.message.reply_text(self._t(tid, "ask_venue_address"), reply_markup=cancel_kb(lang))
        return VENUE_ADDRESS

    async def venue_address(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        if update.message.text in [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=ReplyKeyboardRemove())
            return ROLE_CHOICE
        context.user_data["venue_address"] = update.message.text
        await update.message.reply_text(self._t(tid, "ask_venue_desc"), reply_markup=cancel_kb(lang))
        return VENUE_DESC

    async def venue_desc(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        if update.message.text in [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=ReplyKeyboardRemove())
            return ROLE_CHOICE
        context.user_data["venue_desc"] = update.message.text
        await update.message.reply_text(self._t(tid, "ask_venue_capacity"), reply_markup=cancel_kb(lang))
        return VENUE_CAPACITY

    async def venue_capacity(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        if update.message.text in [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=ReplyKeyboardRemove())
            return ROLE_CHOICE
        try:
            context.user_data["venue_capacity"] = int(update.message.text)
            await update.message.reply_text(self._t(tid, "ask_venue_price"), reply_markup=cancel_kb(lang))
            return VENUE_PRICE
        except ValueError:
            await update.message.reply_text(self._t(tid, "invalid_number"))
            return VENUE_CAPACITY

    async def venue_price(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        if update.message.text in [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=ReplyKeyboardRemove())
            return ROLE_CHOICE
        try:
            context.user_data["venue_price"] = float(update.message.text)
            await update.message.reply_text(self._t(tid, "ask_venue_contact"), reply_markup=cancel_kb(lang))
            return VENUE_CONTACT
        except ValueError:
            await update.message.reply_text(self._t(tid, "invalid_number"))
            return VENUE_PRICE

    async def venue_contact(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        if update.message.text in [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=ReplyKeyboardRemove())
            return ROLE_CHOICE
        context.user_data["venue_contact"] = update.message.text
        await update.message.reply_text(self._t(tid, "ask_venue_location"), reply_markup=cancel_kb(lang))
        return VENUE_LOCATION

    async def venue_location(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        if update.message.text and update.message.text in [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=ReplyKeyboardRemove())
            return ROLE_CHOICE
        if not update.message.location:
            await update.message.reply_text(self._t(tid, "location_required"))
            return VENUE_LOCATION
        context.user_data["venue_lat"] = update.message.location.latitude
        context.user_data["venue_lon"] = update.message.location.longitude
        context.user_data["has_catering"] = 0
        context.user_data["has_music"] = 0
        context.user_data["has_decoration"] = 0
        await update.message.reply_text(
            self._t(tid, "ask_venue_amenities"),
            parse_mode="Markdown",
            reply_markup=amenity_kb(lang)
        )
        return VENUE_AMENITIES

    async def venue_amenities(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        text = update.message.text
        tr = TRANSLATIONS[lang]

        catering_btns = [TRANSLATIONS[l]["catering"] for l in TRANSLATIONS]
        music_btns = [TRANSLATIONS[l]["music"] for l in TRANSLATIONS]
        decoration_btns = [TRANSLATIONS[l]["decoration"] for l in TRANSLATIONS]
        done_btns = [TRANSLATIONS[l]["done"] for l in TRANSLATIONS]
        none_btns = [TRANSLATIONS[l]["none_of_these"] for l in TRANSLATIONS]

        if text in catering_btns:
            context.user_data["has_catering"] = 1
        elif text in music_btns:
            context.user_data["has_music"] = 1
        elif text in decoration_btns:
            context.user_data["has_decoration"] = 1

        if text in done_btns + none_btns:
            if text in none_btns:
                context.user_data["has_catering"] = 0
                context.user_data["has_music"] = 0
                context.user_data["has_decoration"] = 0
            await update.message.reply_text(
                self._t(tid, "ask_extra_amenities"),
                reply_markup=skip_kb(lang)
            )
            return VENUE_EXTRA_AMENITIES

        selected = []
        if context.user_data.get("has_catering"): selected.append(tr["amenity_catering"])
        if context.user_data.get("has_music"): selected.append(tr["amenity_music"])
        if context.user_data.get("has_decoration"): selected.append(tr["amenity_decoration"])
        sel_text = ", ".join(selected) if selected else tr["none"]

        await update.message.reply_text(
            self._t(tid, "select_more_or_done", selected=sel_text),
            parse_mode="Markdown",
            reply_markup=amenity_kb(lang)
        )
        return VENUE_AMENITIES

    async def venue_extra_amenities(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        skip_btns = [TRANSLATIONS[l]["skip"] for l in TRANSLATIONS]
        cancel_btns = [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]
        if update.message.text in cancel_btns:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=ReplyKeyboardRemove())
            return ROLE_CHOICE
        context.user_data["extra_amenities"] = "" if update.message.text in skip_btns else update.message.text
        await update.message.reply_text(self._t(tid, "ask_venue_photo"), reply_markup=skip_photo_kb(lang))
        return VENUE_PHOTO

    async def venue_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        photo_id = ""
        if update.message.photo:
            photo_id = update.message.photo[-1].file_id
        context.user_data["photo_id"] = photo_id
        await update.message.reply_text(
            self._t(tid, "ask_payment_details"),
            parse_mode="Markdown",
            reply_markup=cancel_kb(lang)
        )
        return VENUE_PAYMENT_DETAILS

    async def venue_payment_details(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        cancel_btns = [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]
        if update.message.text in cancel_btns:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=ReplyKeyboardRemove())
            return ROLE_CHOICE

        d = context.user_data
        payment_details = update.message.text

        self.db.add_venue(
            tid, d["owner_name"], d["venue_name"], d["venue_address"], d["venue_desc"],
            d["venue_capacity"], d["venue_price"], d["venue_contact"],
            d.get("venue_lat", 0), d.get("venue_lon", 0),
            d.get("has_catering", 0), d.get("has_music", 0), d.get("has_decoration", 0),
            d.get("photo_id", ""), d.get("extra_amenities", ""), payment_details
        )
        self.db.register_user(tid, d["owner_name"], d["venue_name"], "venue")

        tr = TRANSLATIONS[lang]
        amenities = []
        if d.get("has_catering"): amenities.append(tr["amenity_catering"])
        if d.get("has_music"): amenities.append(tr["amenity_music"])
        if d.get("has_decoration"): amenities.append(tr["amenity_decoration"])

        msg = self._t(tid, "venue_registered",
            owner=d["owner_name"], venue_name=d["venue_name"],
            address=d["venue_address"], desc=d["venue_desc"],
            capacity=d["venue_capacity"], price=d["venue_price"],
            contact=d["venue_contact"],
            amenities=", ".join(amenities) if amenities else tr["none"],
            extra=d.get("extra_amenities") or tr["none"]
        )
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=get_venue_menu(lang))
        return ROLE_CHOICE

    # ── MY VENUE ──────────────────────────────────────────────────────────
    async def my_venue(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        venue = self.db.get_venue_by_telegram_id(tid)
        if not venue:
            await update.message.reply_text(self._t(tid, "no_venue"), reply_markup=get_venue_menu(lang))
            return ROLE_CHOICE

        tr = TRANSLATIONS[lang]
        amenities = []
        if venue[11]: amenities.append(tr["amenity_catering"])
        if venue[12]: amenities.append(tr["amenity_music"])
        if venue[13]: amenities.append(tr["amenity_decoration"])
        avg_rating, rating_count = self.db.get_venue_average_rating(venue[0])
        stars = "⭐" * int(avg_rating) if avg_rating > 0 else tr["no_ratings"]
        premium_badge = tr["premium_badge"] if self.db.is_venue_premium(venue[0]) else tr["free_badge"]

        msg = f"{premium_badge}\n\n" + self._t(tid, "my_venue_display",
            venue_name=venue[3], address=venue[4], desc=venue[5],
            capacity=venue[6], price=venue[7], contact=venue[8],
            amenities=", ".join(amenities) if amenities else tr["none"],
            extra=venue[15] if venue[15] else tr["none"],
            payment=venue[16] if venue[16] else tr["none"],
            stars=stars, avg=avg_rating, count=rating_count
        )

        if venue[14]:
            await update.message.reply_photo(photo=venue[14], caption=msg, parse_mode="Markdown", reply_markup=get_venue_menu(lang))
        else:
            await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=get_venue_menu(lang))
        return ROLE_CHOICE

    # ── EDIT VENUE ────────────────────────────────────────────────────────
    async def edit_venue_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        text = update.message.text
        tr = TRANSLATIONS[lang]

        edit_venue_btns = [TRANSLATIONS[l]["edit_venue"] for l in TRANSLATIONS]
        cancel_btns = [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]

        if text in edit_venue_btns:
            kb = ReplyKeyboardMarkup([
                [tr["edit_desc"], tr["edit_capacity"]],
                [tr["edit_price"], tr["edit_contact"]],
                [tr["edit_payment"], tr["edit_photo"]],
                [tr["cancel"]]
            ], resize_keyboard=True)
            await update.message.reply_text(self._t(tid, "edit_venue_title"), parse_mode="Markdown", reply_markup=kb)
            return VENUE_UPDATE_FIELD

        # Build field map for all languages
        field_map = {}
        photo_btns = []
        for l in TRANSLATIONS:
            trl = TRANSLATIONS[l]
            field_map[trl.get("edit_desc", "")] = ("description", trl.get("edit_desc", ""))
            field_map[trl.get("edit_capacity", "")] = ("capacity", trl.get("edit_capacity", ""))
            field_map[trl.get("edit_price", "")] = ("price_per_seat", trl.get("edit_price", ""))
            field_map[trl.get("edit_contact", "")] = ("contact", trl.get("edit_contact", ""))
            field_map[trl.get("edit_payment", "")] = ("payment_details", trl.get("edit_payment", ""))
            photo_btns.append(trl.get("edit_photo", ""))

        if text in cancel_btns:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=get_venue_menu(lang))
            return ROLE_CHOICE

        if text in photo_btns:
            context.user_data["edit_field_key"] = "photo"
            context.user_data["edit_field_label"] = tr["edit_photo"]
            await update.message.reply_text(self._t(tid, "send_new_photo"), reply_markup=ReplyKeyboardRemove())
            return VENUE_UPDATE_VALUE

        if text in field_map:
            field_key, field_label = field_map[text]
            context.user_data["edit_field_key"] = field_key
            context.user_data["edit_field_label"] = field_label
            await update.message.reply_text(self._t(tid, "enter_new_value"), reply_markup=cancel_kb(lang))
            return VENUE_UPDATE_VALUE

        return await self.save_edit(update, context)

    async def save_edit(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        cancel_btns = [TRANSLATIONS[l]["cancel"] for l in TRANSLATIONS]
        field_key = context.user_data.get("edit_field_key")
        field_label = context.user_data.get("edit_field_label", "")

        if update.message.text and update.message.text in cancel_btns:
            await update.message.reply_text(self._t(tid, "cancelled"), reply_markup=get_venue_menu(lang))
            return ROLE_CHOICE

        if field_key == "photo":
            if update.message.photo:
                self.db.update_venue_photo(tid, update.message.photo[-1].file_id)
                await update.message.reply_text(self._t(tid, "photo_updated"), reply_markup=get_venue_menu(lang))
            else:
                await update.message.reply_text(self._t(tid, "please_send_photo"))
                return VENUE_UPDATE_VALUE
        else:
            self.db.update_venue(tid, field_key, update.message.text)
            await update.message.reply_text(self._t(tid, "field_updated", field=field_label), reply_markup=get_venue_menu(lang))
        return ROLE_CHOICE

    # ── AVAILABILITY ──────────────────────────────────────────────────────
    async def my_availability(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        venue = self.db.get_venue_by_telegram_id(tid)
        if not venue:
            await update.message.reply_text(self._t(tid, "no_venue"), reply_markup=get_venue_menu(lang))
            return ROLE_CHOICE
        booked_dates = self.db.get_booked_dates(venue[0])
        if not booked_dates:
            await update.message.reply_text(self._t(tid, "all_dates_available"), parse_mode="Markdown", reply_markup=get_venue_menu(lang))
            return ROLE_CHOICE
        msg = self._t(tid, "booked_dates_title")
        for date in booked_dates:
            msg += self._t(tid, "booked_date_row", date=date)
        msg += self._t(tid, "other_dates_free")
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=get_venue_menu(lang))
        return ROLE_CHOICE

    # ── MY RATINGS ────────────────────────────────────────────────────────
    async def my_ratings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        tr = TRANSLATIONS[lang]
        venue = self.db.get_venue_by_telegram_id(tid)
        if not venue:
            await update.message.reply_text(self._t(tid, "no_venue"), reply_markup=get_venue_menu(lang))
            return ROLE_CHOICE
        avg_rating, count = self.db.get_venue_average_rating(venue[0])
        ratings = self.db.get_venue_ratings(venue[0])
        if not ratings:
            await update.message.reply_text(self._t(tid, "no_ratings_yet"), reply_markup=get_venue_menu(lang))
            return ROLE_CHOICE
        stars = "⭐" * int(avg_rating)
        msg = self._t(tid, "ratings_header", stars=stars, avg=avg_rating, count=count)
        for r in ratings[:10]:
            comment = r[1] if r[1] else tr["none"]
            msg += f"{'⭐' * r[0]} — {comment}\n   🕐 {r[2][:10]}\n\n"
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=get_venue_menu(lang))
        return ROLE_CHOICE

    # ── MY BOOKINGS ───────────────────────────────────────────────────────
    async def my_bookings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        venue = self.db.get_venue_by_telegram_id(tid)
        if not venue:
            await update.message.reply_text(self._t(tid, "no_venue"), reply_markup=get_venue_menu(lang))
            return ROLE_CHOICE
        bookings = self.db.get_venue_bookings(venue[0])
        if not bookings:
            await update.message.reply_text(self._t(tid, "no_bookings"), reply_markup=get_venue_menu(lang))
            return ROLE_CHOICE

        await update.message.reply_text(
            self._t(tid, "bookings_received", count=len(bookings)),
            parse_mode="Markdown", reply_markup=get_venue_menu(lang)
        )

        tr = TRANSLATIONS[lang]
        for b in bookings:
            wishes = b[9] if b[9] else tr["none"]
            phone = b[11] if b[11] else "-"
            msg = self._t(tid, "booking_item",
                id=b[0], client=b[1], phone=phone, couple=b[8],
                date=b[2], guests=b[3], wishes=wishes,
                total=f"{b[4]:.2f}", down=f"{b[10]:.2f}",
                method=b[6], status=b[7]
            )

            confirm_btn = self._t(tid, "confirm_btn")
            reject_btn = self._t(tid, "reject_btn")
            pay_confirm_btn = self._t(tid, "payment_confirmed_btn")
            pay_fail_btn = self._t(tid, "payment_not_received_btn")

            if b[7] == "Pending":
                kb = InlineKeyboardMarkup([[
                    InlineKeyboardButton(confirm_btn, callback_data=f"confirm_{b[0]}"),
                    InlineKeyboardButton(reject_btn, callback_data=f"reject_{b[0]}")
                ]])
                await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=kb)
            elif b[7] == "Awaiting Payment":
                kb = InlineKeyboardMarkup([[
                    InlineKeyboardButton(pay_confirm_btn, callback_data=f"payment_confirmed_{b[0]}"),
                    InlineKeyboardButton(pay_fail_btn, callback_data=f"payment_failed_{b[0]}")
                ]])
                await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=kb)
            else:
                await update.message.reply_text(msg, parse_mode="Markdown")
        return ROLE_CHOICE

    # ── MY STATS ──────────────────────────────────────────────────────────
    async def my_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tid = update.effective_user.id
        lang = self._lang(tid)
        tr = TRANSLATIONS[lang]
        venue = self.db.get_venue_by_telegram_id(tid)
        if not venue:
            await update.message.reply_text(self._t(tid, "no_venue"), reply_markup=get_venue_menu(lang))
            return ROLE_CHOICE
        bookings = self.db.get_venue_bookings(venue[0])
        total_revenue = sum(b[4] for b in bookings)
        confirmed = len([b for b in bookings if b[7]=="Confirmed"])
        pending = len([b for b in bookings if b[7]=="Pending"])
        rejected = len([b for b in bookings if b[7]=="Rejected"])
        avg_rating, _ = self.db.get_venue_average_rating(venue[0])
        stars = "⭐" * int(avg_rating) if avg_rating > 0 else tr["no_ratings"]

        msg = self._t(tid, "stats_display",
            venue_name=venue[3], capacity=venue[6], price=venue[7],
            stars=stars, avg=avg_rating, total=len(bookings),
            confirmed=confirmed, pending=pending, rejected=rejected,
            revenue=f"{total_revenue:.2f}"
        )
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=get_venue_menu(lang))
        return ROLE_CHOICE

    # ── CALLBACK HANDLER ──────────────────────────────────────────────────
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        data = query.data

        if data.startswith("confirm_"):
            booking_id = int(data.split("_")[1])
            booking = self.db.get_booking_by_id(booking_id)
            self.db.update_booking_status(booking_id, "Awaiting Payment")
            payment_details = self.db.get_venue_payment_details(booking[4])
            client_tid = booking[1]
            client_lang = self._lang(client_tid)

            await query.edit_message_text(
                self._t(query.from_user.id, "booking_confirmed_venue", id=booking_id),
                parse_mode="Markdown"
            )
            try:
                icon = "💵" if booking[11] == "cash" else "💳"
                method_labels = {"cash": {"en": "Cash", "uz": "Naqd pul"}, "card": {"en": "Card", "uz": "Karta"}}
                method_label = method_labels.get(booking[11], {"en": booking[11]}).get(client_lang, booking[11])

                msg = t(client_tid, "booking_confirmed_client", self.db,
                    id=booking_id, venue=booking[5], date=booking[6],
                    couple=booking[13], guests=booking[7],
                    total=f"{booking[8]:.2f}", down=f"{booking[10]:.2f}",
                    icon=icon, method=method_label, payment_details=payment_details
                )
                i_paid_btn = t(client_tid, "i_paid", self.db)
                await context.bot.send_message(
                    chat_id=client_tid, text=msg, parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(i_paid_btn, callback_data=f"paid_{booking_id}")
                    ]])
                )
            except: pass

        elif data.startswith("paid_"):
            booking_id = int(data.split("_")[1])
            booking = self.db.get_booking_by_id(booking_id)
            self.db.update_booking_status(booking_id, "Payment Sent")
            client_tid = booking[1]

            await query.edit_message_text(
                t(client_tid, "payment_sent_client", self.db), parse_mode="Markdown"
            )
            try:
                venue = self.db.get_venue_by_id(booking[4])
                if venue:
                    owner_tid = venue[1]
                    msg = t(owner_tid, "payment_notification_venue", self.db,
                        id=booking_id, client=booking[2], phone=booking[3],
                        couple=booking[13], date=booking[6], down=f"{booking[10]:.2f}"
                    )
                    pay_confirm = t(owner_tid, "payment_confirmed_btn", self.db)
                    pay_fail = t(owner_tid, "payment_not_received_btn", self.db)
                    await context.bot.send_message(
                        chat_id=owner_tid, text=msg, parse_mode="Markdown",
                        reply_markup=InlineKeyboardMarkup([[
                            InlineKeyboardButton(pay_confirm, callback_data=f"payment_confirmed_{booking_id}"),
                            InlineKeyboardButton(pay_fail, callback_data=f"payment_failed_{booking_id}")
                        ]])
                    )
            except: pass

        elif data.startswith("payment_confirmed_"):
            booking_id = int(data.split("_")[2])
            booking = self.db.get_booking_by_id(booking_id)
            self.db.update_booking_status(booking_id, "Confirmed")
            client_tid = booking[1]

            await query.edit_message_text(
                t(query.from_user.id, "payment_confirmed_venue", self.db, id=booking_id),
                parse_mode="Markdown"
            )
            try:
                msg = t(client_tid, "booking_fully_confirmed", self.db,
                    id=booking_id, venue=booking[5], date=booking[6], couple=booking[13]
                )
                await context.bot.send_message(chat_id=client_tid, text=msg, parse_mode="Markdown")
            except: pass

        elif data.startswith("payment_failed_"):
            booking_id = int(data.split("_")[2])
            booking = self.db.get_booking_by_id(booking_id)
            self.db.update_booking_status(booking_id, "Awaiting Payment")
            client_tid = booking[1]

            await query.edit_message_text(
                t(query.from_user.id, "payment_not_received_venue", self.db, id=booking_id),
                parse_mode="Markdown"
            )
            try:
                msg = t(client_tid, "payment_not_confirmed", self.db, id=booking_id)
                i_paid_btn = t(client_tid, "i_paid_again", self.db)
                await context.bot.send_message(
                    chat_id=client_tid, text=msg, parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(i_paid_btn, callback_data=f"paid_{booking_id}")
                    ]])
                )
            except: pass

        elif data.startswith("reject_") and not data.startswith("reject_premium_"):
            booking_id = int(data.split("_")[1])
            booking = self.db.get_booking_by_id(booking_id)
            self.db.update_booking_status(booking_id, "Rejected")
            client_tid = booking[1]

            await query.edit_message_text(
                t(query.from_user.id, "booking_rejected_venue", self.db, id=booking_id),
                parse_mode="Markdown"
            )
            try:
                msg = t(client_tid, "booking_rejected_client", self.db,
                    id=booking_id, venue=booking[5], date=booking[6]
                )
                await context.bot.send_message(chat_id=client_tid, text=msg, parse_mode="Markdown")
            except: pass

        elif data.startswith("grant_premium_"):
            parts = data.split("_")
            venue_id = int(parts[2])
            plan = " ".join(parts[3:]).replace("_", " ")
            from datetime import datetime, timedelta
            expiry = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            self.db.set_premium(venue_id, 1, expiry)

            await query.edit_message_text(
                f"👑 *Premium Activated!*\n\nVenue ID {venue_id} — {plan}\nValid until: {expiry}",
                parse_mode="Markdown"
            )
            # Notify venue owner
            try:
                venue = self.db.get_venue_by_id(venue_id)
                if venue:
                    owner_tid = venue[1]
                    msg = t(owner_tid, "premium_confirmed_venue", self.db,
                        plan=plan, expiry=expiry)
                    await context.bot.send_message(
                        chat_id=owner_tid, text=msg, parse_mode="Markdown"
                    )
            except Exception as e:
                print(f"Premium notify error: {e}")

        elif data.startswith("reject_premium_"):
            venue_id = int(data.split("_")[2])
            await query.edit_message_text(
                f"❌ Premium rejected for Venue ID {venue_id}.",
                parse_mode="Markdown"
            )
            try:
                venue = self.db.get_venue_by_id(venue_id)
                if venue:
                    owner_tid = venue[1]
                    msg = t(owner_tid, "premium_rejected_venue", self.db)
                    await context.bot.send_message(chat_id=owner_tid, text=msg, parse_mode="Markdown")
            except: pass