import json
import base64
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import ContextTypes
from handlers.start_handler import ROLE_CHOICE, ADMIN_ACTION, ADMIN_MENU

ADMIN_ID = 587392391
ADMIN_MINIAPP_URL = "https://00013290.github.io/tuysavdo/miniapp/index.html"


class AdminHandler:
    def __init__(self, database):
        self.db = database

    def build_miniapp_url(self):
        venues, clients, bookings, pending, revenue = self.db.get_stats()
        week_rev = self.db.get_revenue_by_period("week")
        month_rev = self.db.get_revenue_by_period("month")
        year_rev = self.db.get_revenue_by_period("year")
        week_b = len(self.db.get_bookings_by_period("week"))
        month_b = len(self.db.get_bookings_by_period("month"))
        all_bookings = self.db.get_all_bookings()
        all_users = self.db.get_all_users()

        data = {
            "stats": {
                "venues": venues, "clients": clients,
                "bookings": bookings, "pending": pending,
                "revenue": round(revenue, 2),
                "weekRevenue": round(week_rev, 2),
                "monthRevenue": round(month_rev, 2),
                "yearRevenue": round(year_rev, 2),
                "weekBookings": week_b,
                "monthBookings": month_b
            },
            "bookings": [
                {"id": b[0], "client": b[1], "venue": b[2], "date": b[3],
                 "guests": b[4], "total": b[5], "commission": round(b[6], 2),
                 "status": b[7], "couple": b[8], "payment": b[9]}
                for b in all_bookings[:20]
            ],
            "users": [
                {"name": u[1], "company": u[2], "role": u[3]}
                for u in all_users
            ]
        }

        encoded = base64.b64encode(json.dumps(data).encode()).decode()
        return f"{ADMIN_MINIAPP_URL}?data={encoded}"

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_id = update.effective_user.id
        if telegram_id != ADMIN_ID:
            await update.message.reply_text("⛔ Access denied.")
            return ROLE_CHOICE

        text = update.message.text

        if text == "📊 Dashboard":
            return await self.dashboard(update, context)
        elif text == "📋 All Bookings":
            return await self.all_bookings(update, context)
        elif text == "👥 All Users":
            return await self.all_users(update, context)
        elif text == "💰 Revenue Report":
            return await self.revenue_report(update, context)
        elif text in ["📅 This Week", "🗓 This Month", "📆 This Year", "📋 All Bookings List", "🔙 Back to Admin"]:
            return await self.handle_filter(update, context)
        else:
            await update.message.reply_text("Please choose an option.", reply_markup=ADMIN_MENU)
            return ADMIN_ACTION

    async def dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        venues, clients, bookings, pending, revenue = self.db.get_stats()
        week_rev = self.db.get_revenue_by_period("week")
        month_rev = self.db.get_revenue_by_period("month")
        week_b = len(self.db.get_bookings_by_period("week"))
        month_b = len(self.db.get_bookings_by_period("month"))

        miniapp_url = self.build_miniapp_url()
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton("📊 Open Full Admin Panel", web_app=WebAppInfo(url=miniapp_url))
        ]])

        await update.message.reply_text(
            f"🔧 *TuySavdo Admin Dashboard*\n\n"
            f"🏛 Venues: {venues} | 🎊 Clients: {clients}\n"
            f"📋 Total Bookings: {bookings} | ⏳ Pending: {pending}\n\n"
            f"💰 *Revenue:*\n"
            f"   📅 This Week: ${week_rev:.2f}\n"
            f"   🗓 This Month: ${month_rev:.2f}\n"
            f"   💵 All Time: ${revenue:.2f}\n\n"
            f"📋 Last 7 days: {week_b} | Last 30 days: {month_b}",
            parse_mode="Markdown",
            reply_markup=keyboard
        )
        return ADMIN_ACTION

    async def all_bookings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = ReplyKeyboardMarkup([
            ["📅 This Week", "🗓 This Month"],
            ["📆 This Year", "📋 All Bookings List"],
            ["🔙 Back to Admin"]
        ], resize_keyboard=True)
        await update.message.reply_text("📋 *Filter Bookings By:*", parse_mode="Markdown", reply_markup=keyboard)
        return ADMIN_ACTION

    async def handle_filter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        if text == "🔙 Back to Admin":
            await update.message.reply_text("Admin menu:", reply_markup=ADMIN_MENU)
            return ADMIN_ACTION

        period_map = {
            "📅 This Week": "week", "🗓 This Month": "month",
            "📆 This Year": "year", "📋 All Bookings List": "all"
        }
        period = period_map.get(text, "all")
        bookings = self.db.get_bookings_by_period(period)
        revenue = self.db.get_revenue_by_period(period)

        if not bookings:
            await update.message.reply_text("No bookings found.", reply_markup=ADMIN_MENU)
            return ADMIN_ACTION

        label = text.replace("📅 ", "").replace("🗓 ", "").replace("📆 ", "").replace("📋 ", "")
        msg = f"📋 *{label}:* {len(bookings)} bookings | Revenue: ${revenue:.2f}\n\n"
        for b in bookings[:15]:
            msg += f"#{b[0]} {b[2]} → {b[3]} | 📅 {b[5]} | 💰 ${b[7]:.2f} | {b[11]}\n"
        if len(bookings) > 15:
            msg += f"\n... and {len(bookings) - 15} more"

        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=ADMIN_MENU)
        return ADMIN_ACTION

    async def all_users(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        users = self.db.get_all_users()
        if not users:
            await update.message.reply_text("No users yet.", reply_markup=ADMIN_MENU)
            return ADMIN_ACTION

        venues = [u for u in users if u[3] == "venue"]
        clients = [u for u in users if u[3] == "client"]

        msg = f"👥 *All Users ({len(users)} total):*\n\n"
        msg += f"🏛 *Venue Owners ({len(venues)}):*\n"
        for u in venues:
            msg += f"   • {u[1]} — {u[2]}\n"
        msg += f"\n🎊 *Clients ({len(clients)}):*\n"
        for u in clients:
            msg += f"   • {u[1]}\n"

        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=ADMIN_MENU)
        return ADMIN_ACTION

    async def revenue_report(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        week_rev = self.db.get_revenue_by_period("week")
        month_rev = self.db.get_revenue_by_period("month")
        year_rev = self.db.get_revenue_by_period("year")
        all_rev = self.db.get_revenue_by_period("all")
        week_b = len(self.db.get_bookings_by_period("week"))
        month_b = len(self.db.get_bookings_by_period("month"))
        year_b = len(self.db.get_bookings_by_period("year"))
        all_b = len(self.db.get_bookings_by_period("all"))

        await update.message.reply_text(
            f"💰 *Revenue Report:*\n\n"
            f"📊 Commission Rate: *0.1%* per booking\n\n"
            f"📅 *This Week:*\n   {week_b} bookings | ${week_rev:.2f}\n\n"
            f"🗓 *This Month:*\n   {month_b} bookings | ${month_rev:.2f}\n\n"
            f"📆 *This Year:*\n   {year_b} bookings | ${year_rev:.2f}\n\n"
            f"💵 *All Time:*\n   {all_b} bookings | ${all_rev:.2f}",
            parse_mode="Markdown",
            reply_markup=ADMIN_MENU
        )
        return ADMIN_ACTION