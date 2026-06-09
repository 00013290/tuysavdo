from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

ADMIN_ID = 587392391

(
    ROLE_CHOICE,
    VENUE_OWNER_NAME, VENUE_NAME, VENUE_ADDRESS, VENUE_DESC,
    VENUE_CAPACITY, VENUE_PRICE, VENUE_CONTACT, VENUE_LOCATION, VENUE_AMENITIES,
    VENUE_PHOTO, VENUE_EXTRA_AMENITIES, VENUE_PAYMENT_DETAILS, VENUE_UPDATE_FIELD, VENUE_UPDATE_VALUE, VENUE_LOCATION,
    CLIENT_NAME, CLIENT_PHONE,
    BOOK_VENUE, BOOK_DATE, BOOK_GUESTS,
    BOOK_COUPLE, BOOK_WISHES, BOOK_PAYMENT,
    RATE_BOOKING, RATE_STARS, RATE_COMMENT,
    AI_GUESTS, AI_BUDGET, AI_DATE,
    ADMIN_ACTION
) = range(31)

VENUE_MENU = ReplyKeyboardMarkup([
    ["🏛 My Venue", "✏️ Edit Venue"],
    ["📋 My Bookings", "📊 My Stats"],
    ["🗓 Availability", "⭐ My Ratings"],
    ["🌐 My Dashboard"]
], resize_keyboard=True)

CLIENT_MENU = ReplyKeyboardMarkup([
    ["🔍 Browse Venues", "📅 Book a Venue"],
    ["🤖 AI Advice", "📋 My Bookings"],
    ["⭐ Rate a Venue", "🌐 Track Bookings"],
], resize_keyboard=True)

ADMIN_MENU = ReplyKeyboardMarkup([
    ["📊 Dashboard", "📋 All Bookings"],
    ["👥 All Users", "💰 Revenue Report"],
], resize_keyboard=True)


def get_venue_menu(telegram_id):
    return VENUE_MENU


def get_client_menu(telegram_id):
    return CLIENT_MENU


class StartHandler:
    def __init__(self, database):
        self.db = database

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data.clear()
        telegram_id = update.effective_user.id
        role = self.db.get_user_role(telegram_id)

        if role == "venue":
            await update.message.reply_text(
                "🏛 Welcome back to *TuySavdo*!\n\nManage your venue and bookings below:",
                parse_mode="Markdown", reply_markup=VENUE_MENU
            )
            return ROLE_CHOICE

        elif role == "client":
            await update.message.reply_text(
                "🎊 Welcome back to *TuySavdo*!\n\nFind and book the perfect venue below:",
                parse_mode="Markdown", reply_markup=CLIENT_MENU
            )
            return ROLE_CHOICE

        else:
            if telegram_id == ADMIN_ID:
                await update.message.reply_text(
                    "🔧 *TuySavdo Admin Panel*\n\nWelcome back, Admin!",
                    parse_mode="Markdown", reply_markup=ADMIN_MENU
                )
                return ADMIN_ACTION

            keyboard = [["🏛 Register as Venue Owner", "🎊 Register as Client"]]
            await update.message.reply_text(
                "🎊 Welcome to *TuySavdo*\n"
                "Uzbekistan's Wedding Venue Booking Platform!\n\n"
                "Please choose your role:",
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

        if text == "🏛 Register as Venue Owner":
            await update.message.reply_text(
                "Let's register your venue!\n\nWhat is your full name?",
                reply_markup=ReplyKeyboardRemove()
            )
            return VENUE_OWNER_NAME

        if text == "🎊 Register as Client":
            await update.message.reply_text(
                "Welcome! What is your full name?",
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

        await update.message.reply_text("Please choose an option from the menu.")
        return ROLE_CHOICE