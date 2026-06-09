from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ConversationHandler, CallbackQueryHandler
)

from database import Database
from ai import VenueAdvisor
from handlers.start_handler import (
    StartHandler,
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
)
from handlers.venue_handler import VenueHandler
from handlers.client_handler import ClientHandler
from handlers.admin_handler import AdminHandler

TOKEN = "8965166931:AAH4FV3MJowDMaIBaX9GYklTrvSvNLS_mfw"


def main():
    db = Database()
    advisor = VenueAdvisor(db)

    start_h = StartHandler(db)
    venue_h = VenueHandler(db)
    client_h = ClientHandler(db)
    client_h.set_advisor(advisor)
    admin_h = AdminHandler(db)

    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_h.start)],
        states={
            ROLE_CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, start_h.role_choice)],

            # Venue registration
            VENUE_OWNER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, venue_h.venue_owner_name)],
            VENUE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, venue_h.venue_name)],
            VENUE_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, venue_h.venue_address)],
            VENUE_DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, venue_h.venue_desc)],
            VENUE_CAPACITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, venue_h.venue_capacity)],
            VENUE_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, venue_h.venue_price)],
            VENUE_CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, venue_h.venue_contact)],
            VENUE_LOCATION: [
                MessageHandler(filters.LOCATION, venue_h.venue_location),
                MessageHandler(filters.TEXT & ~filters.COMMAND, venue_h.venue_location)
            ],
            VENUE_LOCATION: [
                MessageHandler(filters.LOCATION, venue_h.venue_location),
                MessageHandler(filters.TEXT & ~filters.COMMAND, venue_h.venue_location)
            ],
            VENUE_AMENITIES: [MessageHandler(filters.TEXT & ~filters.COMMAND, venue_h.venue_amenities)],
            VENUE_EXTRA_AMENITIES: [MessageHandler(filters.TEXT & ~filters.COMMAND, venue_h.venue_extra_amenities)],
            VENUE_PHOTO: [
                MessageHandler(filters.PHOTO, venue_h.venue_photo),
                MessageHandler(filters.TEXT & ~filters.COMMAND, venue_h.venue_photo)
            ],
            VENUE_PAYMENT_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, venue_h.venue_payment_details)],

            # Venue management
            VENUE_UPDATE_FIELD: [MessageHandler(filters.TEXT & ~filters.COMMAND, venue_h.edit_venue_start)],
            VENUE_UPDATE_VALUE: [
                MessageHandler(filters.PHOTO, venue_h.save_edit),
                MessageHandler(filters.TEXT & ~filters.COMMAND, venue_h.save_edit)
            ],

            # Client registration
            CLIENT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, client_h.client_name)],
            CLIENT_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, client_h.client_phone)],

            # Booking flow
            BOOK_VENUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, client_h.book_venue)],
            BOOK_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, client_h.book_date)],
            BOOK_GUESTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, client_h.book_guests)],
            BOOK_COUPLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, client_h.book_couple)],
            BOOK_WISHES: [MessageHandler(filters.TEXT & ~filters.COMMAND, client_h.book_wishes)],
            BOOK_PAYMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, client_h.book_payment)],

            # Rating flow
            RATE_BOOKING: [MessageHandler(filters.TEXT & ~filters.COMMAND, client_h.rate_booking)],
            RATE_STARS: [MessageHandler(filters.TEXT & ~filters.COMMAND, client_h.rate_stars)],
            RATE_COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, client_h.rate_comment)],

            # AI
            AI_GUESTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, client_h.ai_guests)],
            AI_BUDGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, client_h.ai_budget)],
            AI_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, client_h.ai_date)],
            # Admin
            ADMIN_ACTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_h.handle)],
        },
        fallbacks=[CommandHandler("start", start_h.start)],
    )

    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(venue_h.handle_callback))

    print("🎊 TuySavdo bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()