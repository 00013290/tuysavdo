from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from translations import t, get_lang_keyboard, TRANSLATIONS

ADMIN_ID = 587392391

(
    LANG_CHOICE,
    ROLE_CHOICE,
    VENUE_OWNER_NAME, VENUE_NAME, VENUE_ADDRESS, VENUE_DESC,
    VENUE_CAPACITY, VENUE_PRICE, VENUE_CONTACT, VENUE_LOCATION, VENUE_AMENITIES,
    VENUE_PHOTO, VENUE_EXTRA_AMENITIES, VENUE_PAYMENT_DETAILS,
    VENUE_UPDATE_FIELD, VENUE_UPDATE_VALUE,
    VENUE_PREMIUM, PREMIUM_PLAN, PREMIUM_PAY,
    CLIENT_NAME, CLIENT_PHONE,
    BOOK_VENUE, BOOK_DATE, BOOK_GUESTS,
    BOOK_COUPLE, BOOK_WISHES, BOOK_PAYMENT,
    RATE_BOOKING, RATE_STARS, RATE_COMMENT,
    AI_GUESTS, AI_BUDGET, AI_DATE,
    ADMIN_ACTION
) = range(34)


def get_venue_menu(lang="en"):
    tr = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    return ReplyKeyboardMarkup([
        [tr["my_venue"], tr["edit_venue"]],
        [tr["my_bookings"], tr["my_stats"]],
        [tr["availability"], tr["my_ratings"]],
        [tr["my_dashboard"], tr["upgrade_btn"]],
    ], resize_keyboard=True)


def get_client_menu(lang="en"):
    tr = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    return ReplyKeyboardMarkup([
        [tr["browse_venues"], tr["book_venue_btn"]],
        [tr["ai_advice"], tr["my_bookings_client"]],
        [tr["rate_venue"], tr["track_bookings"]],
    ], resize_keyboard=True)


ADMIN_MENU = ReplyKeyboardMarkup([
    ["📊 Dashboard", "📋 All Bookings"],
    ["👥 All Users", "💰 Revenue Report"],
    ["👑 Premium Subscribers"],
], resize_keyboard=True)

# Keep English versions as constants for callback matching
VENUE_MENU = get_venue_menu("en")
CLIENT_MENU = get_client_menu("en")


class StartHandler:
    def __init__(self, database):
        self.db = database

    def _lang(self, telegram_id):
        try:
            return self.db.get_user_language(telegram_id) or "en"
        except:
            return "en"

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data.clear()
        telegram_id = update.effective_user.id

        if telegram_id == ADMIN_ID:
            await update.message.reply_text(
                "🔧 *TuySavdo Admin Panel*\n\nWelcome back, Admin!",
                parse_mode="Markdown", reply_markup=ADMIN_MENU
            )
            return ADMIN_ACTION

        role = self.db.get_user_role(telegram_id)

        if role == "venue":
            lang = self._lang(telegram_id)
            await update.message.reply_text(
                t(telegram_id, "welcome_back_venue", self.db),
                parse_mode="Markdown", reply_markup=get_venue_menu(lang)
            )
            return ROLE_CHOICE

        elif role == "client":
            lang = self._lang(telegram_id)
            await update.message.reply_text(
                t(telegram_id, "welcome_back_client", self.db),
                parse_mode="Markdown", reply_markup=get_client_menu(lang)
            )
            return ROLE_CHOICE

        else:
            # New user — ask language first
            await update.message.reply_text(
                "🌐 *Welcome to TuySavdo!*\n\n"
                "Please choose your language:\n"
                "Iltimos, tilingizni tanlang:",
                parse_mode="Markdown",
                reply_markup=get_lang_keyboard()
            )
            return LANG_CHOICE

    async def lang_choice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        telegram_id = update.effective_user.id

        lang_map = {
            "🇬🇧 English": "en",
            "🇺🇿 O'zbek": "uz",
        }

        lang = lang_map.get(text, "en")
        self.db.set_user_language(telegram_id, lang)

        confirm = TRANSLATIONS[lang]["language_set"]
        await update.message.reply_text(confirm, reply_markup=ReplyKeyboardRemove())

        reg_venue = TRANSLATIONS[lang]["register_venue_owner"]
        reg_client = TRANSLATIONS[lang]["register_client"]
        welcome = TRANSLATIONS[lang]["welcome_new"]

        keyboard = [[reg_venue, reg_client]]
        await update.message.reply_text(
            welcome,
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return ROLE_CHOICE

    async def role_choice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.message.text:
            return ROLE_CHOICE

        text = update.message.text
        telegram_id = update.effective_user.id
        role = self.db.get_user_role(telegram_id)
        lang = self._lang(telegram_id)

        # Check register buttons in all languages
        venue_btns = [TRANSLATIONS[l]["register_venue_owner"] for l in TRANSLATIONS]
        client_btns = [TRANSLATIONS[l]["register_client"] for l in TRANSLATIONS]

        if text in venue_btns:
            await update.message.reply_text(
                t(telegram_id, "ask_owner_name", self.db),
                reply_markup=ReplyKeyboardRemove()
            )
            return VENUE_OWNER_NAME

        if text in client_btns:
            await update.message.reply_text(
                t(telegram_id, "ask_client_name", self.db),
                reply_markup=ReplyKeyboardRemove()
            )
            return CLIENT_NAME

        if role == "venue":
            from handlers.venue_handler import VenueHandler
            handler = VenueHandler(self.db)
            return await handler.handle(update, context)

        if role == "client":
            from handlers.client_handler import ClientHandler
            handler = ClientHandler(self.db)
            return await handler.handle(update, context)

        await update.message.reply_text(t(telegram_id, "choose_option", self.db))
        return ROLE_CHOICE