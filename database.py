import sqlite3


class Database:
    def __init__(self):
        self.db_name = "tuysavdo.db"
        self.init_db()

    def get_conn(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        conn = self.get_conn()
        c = conn.cursor()

        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                name TEXT,
                company TEXT,
                role TEXT,
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS venues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                owner_name TEXT,
                venue_name TEXT,
                address TEXT,
                description TEXT DEFAULT '',
                capacity INTEGER DEFAULT 0,
                price_per_seat REAL DEFAULT 0,
                contact TEXT,
                latitude REAL,
                longitude REAL,
                has_catering INTEGER DEFAULT 0,
                has_music INTEGER DEFAULT 0,
                has_decoration INTEGER DEFAULT 0,
                photo_id TEXT DEFAULT '',
                extra_amenities TEXT DEFAULT '',
                payment_details TEXT DEFAULT '',
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_telegram_id INTEGER,
                client_name TEXT,
                client_phone TEXT DEFAULT '',
                venue_id INTEGER,
                venue_name TEXT,
                event_date TEXT,
                guest_count INTEGER,
                total_cost REAL,
                commission REAL,
                down_payment REAL,
                payment_method TEXT DEFAULT 'cash',
                status TEXT DEFAULT 'Pending',
                couple_names TEXT DEFAULT '',
                wishes TEXT DEFAULT '',
                reminded INTEGER DEFAULT 0,
                placed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (venue_id) REFERENCES venues(id)
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                name TEXT,
                phone TEXT DEFAULT '',
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_id INTEGER UNIQUE,
                venue_id INTEGER,
                client_telegram_id INTEGER,
                rating INTEGER,
                comment TEXT DEFAULT '',
                rated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (venue_id) REFERENCES venues(id)
            )
        """)

        conn.commit()
        conn.close()

    # ── User methods ─────────────────────────────────────────────────────
    def get_user_role(self, telegram_id):
        conn = self.get_conn()
        result = conn.execute("SELECT role FROM users WHERE telegram_id=?", (telegram_id,)).fetchone()
        conn.close()
        return result[0] if result else None

    def register_user(self, telegram_id, name, company, role):
        conn = self.get_conn()
        conn.execute("INSERT OR REPLACE INTO users (telegram_id, name, company, role) VALUES (?,?,?,?)", (telegram_id, name, company, role))
        conn.commit()
        conn.close()

    def get_all_users(self):
        conn = self.get_conn()
        result = conn.execute("SELECT telegram_id, name, company, role, registered_at FROM users").fetchall()
        conn.close()
        return result

    # ── Venue methods ────────────────────────────────────────────────────
    def add_venue(self, telegram_id, owner_name, venue_name, address, description,
                  capacity, price_per_seat, contact, latitude=0, longitude=0,
                  has_catering=0, has_music=0, has_decoration=0, photo_id='', extra_amenities='', payment_details=''):
        conn = self.get_conn()
        conn.execute("""
            INSERT OR REPLACE INTO venues
            (telegram_id, owner_name, venue_name, address, description,
             capacity, price_per_seat, contact,
             has_catering, has_music, has_decoration, photo_id, payment_details)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (telegram_id, owner_name, venue_name, address, description,
              capacity, price_per_seat, contact,
              has_catering, has_music, has_decoration, photo_id, payment_details))
        conn.commit()
        conn.close()

    def get_venue_by_telegram_id(self, telegram_id):
        conn = self.get_conn()
        result = conn.execute("SELECT * FROM venues WHERE telegram_id=?", (telegram_id,)).fetchone()
        conn.close()
        return result

    def get_venue_by_id(self, venue_id):
        conn = self.get_conn()
        result = conn.execute("SELECT * FROM venues WHERE id=?", (venue_id,)).fetchone()
        conn.close()
        return result

    def get_all_venues(self):
        conn = self.get_conn()
        result = conn.execute("SELECT * FROM venues").fetchall()
        conn.close()
        return result

    def update_venue(self, telegram_id, field, value):
        conn = self.get_conn()
        conn.execute(f"UPDATE venues SET {field}=? WHERE telegram_id=?", (value, telegram_id))
        conn.commit()
        conn.close()

    def update_venue_photo(self, telegram_id, photo_id):
        conn = self.get_conn()
        conn.execute("UPDATE venues SET photo_id=? WHERE telegram_id=?", (photo_id, telegram_id))
        conn.commit()
        conn.close()

    def get_venue_average_rating(self, venue_id):
        conn = self.get_conn()
        result = conn.execute("SELECT AVG(rating), COUNT(*) FROM ratings WHERE venue_id=?", (venue_id,)).fetchone()
        conn.close()
        avg = round(result[0], 1) if result[0] else 0
        return avg, result[1] or 0

    def get_venue_payment_details(self, venue_id):
        conn = self.get_conn()
        result = conn.execute("SELECT payment_details FROM venues WHERE id=?", (venue_id,)).fetchone()
        conn.close()
        return result[0] if result else ""

    # ── Client methods ───────────────────────────────────────────────────
    def add_client(self, telegram_id, name, phone=""):
        conn = self.get_conn()
        conn.execute("INSERT OR REPLACE INTO clients (telegram_id, name, phone) VALUES (?,?,?)", (telegram_id, name, phone))
        conn.commit()
        conn.close()

    def get_client_name(self, telegram_id):
        conn = self.get_conn()
        result = conn.execute("SELECT name FROM clients WHERE telegram_id=?", (telegram_id,)).fetchone()
        conn.close()
        return result[0] if result else "Unknown"

    def get_client_phone(self, telegram_id):
        conn = self.get_conn()
        result = conn.execute("SELECT phone FROM clients WHERE telegram_id=?", (telegram_id,)).fetchone()
        conn.close()
        return result[0] if result else ""

    # ── Booking methods ──────────────────────────────────────────────────
    def add_booking(self, client_telegram_id, client_name, client_phone, venue_id, venue_name,
                    event_date, guest_count, price_per_seat, payment_method="cash",
                    couple_names="", wishes=""):
        total_cost = round(guest_count * price_per_seat, 2)
        commission = round(total_cost * 0.001, 2)  # 0.1% commission
        down_payment = round(total_cost * 0.50, 2)  # 50% down payment
        conn = self.get_conn()
        conn.execute("""
            INSERT INTO bookings
            (client_telegram_id, client_name, client_phone, venue_id, venue_name,
             event_date, guest_count, total_cost, commission, down_payment,
             payment_method, couple_names, wishes)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (client_telegram_id, client_name, client_phone, venue_id, venue_name,
              event_date, guest_count, total_cost, commission, down_payment,
              payment_method, couple_names, wishes))
        conn.commit()
        conn.close()
        return commission, total_cost, down_payment

    def get_client_bookings(self, telegram_id):
        conn = self.get_conn()
        result = conn.execute("""
            SELECT id, venue_name, event_date, guest_count,
                   total_cost, commission, payment_method,
                   status, couple_names, wishes, down_payment, placed_at
            FROM bookings WHERE client_telegram_id=?
            ORDER BY placed_at DESC
        """, (telegram_id,)).fetchall()
        conn.close()
        return result

    def get_all_bookings(self):
        conn = self.get_conn()
        result = conn.execute("""
            SELECT id, client_name, venue_name, event_date,
                   guest_count, total_cost, commission,
                   status, couple_names, payment_method, down_payment, placed_at
            FROM bookings ORDER BY placed_at DESC
        """).fetchall()
        conn.close()
        return result

    def get_venue_bookings(self, venue_id):
        conn = self.get_conn()
        result = conn.execute("""
            SELECT id, client_name, event_date, guest_count,
                   total_cost, commission, payment_method,
                   status, couple_names, wishes, down_payment, client_phone, placed_at
            FROM bookings WHERE venue_id=?
            ORDER BY placed_at DESC
        """, (venue_id,)).fetchall()
        conn.close()
        return result

    def get_booking_by_id(self, booking_id):
        conn = self.get_conn()
        result = conn.execute("SELECT * FROM bookings WHERE id=?", (booking_id,)).fetchone()
        conn.close()
        return result

    def update_booking_status(self, booking_id, status):
        conn = self.get_conn()
        conn.execute("UPDATE bookings SET status=? WHERE id=?", (status, booking_id))
        conn.commit()
        conn.close()

    def check_availability(self, venue_id, event_date):
        conn = self.get_conn()
        result = conn.execute("""
            SELECT id FROM bookings
            WHERE venue_id=? AND event_date=? AND status != 'Rejected'
        """, (venue_id, event_date)).fetchone()
        conn.close()
        return result is None

    def get_booked_dates(self, venue_id):
        conn = self.get_conn()
        result = conn.execute("""
            SELECT event_date FROM bookings
            WHERE venue_id=? AND status != 'Rejected'
            ORDER BY event_date ASC
        """, (venue_id,)).fetchall()
        conn.close()
        return [r[0] for r in result]

    def get_bookings_by_period(self, period="all"):
        conn = self.get_conn()
        if period == "week":
            query = "SELECT * FROM bookings WHERE placed_at >= datetime('now', '-7 days') ORDER BY placed_at DESC"
        elif period == "month":
            query = "SELECT * FROM bookings WHERE placed_at >= datetime('now', '-30 days') ORDER BY placed_at DESC"
        elif period == "year":
            query = "SELECT * FROM bookings WHERE placed_at >= datetime('now', '-365 days') ORDER BY placed_at DESC"
        else:
            query = "SELECT * FROM bookings ORDER BY placed_at DESC"
        result = conn.execute(query).fetchall()
        conn.close()
        return result

    # ── Rating methods ───────────────────────────────────────────────────
    def add_rating(self, booking_id, venue_id, client_telegram_id, rating, comment=""):
        conn = self.get_conn()
        conn.execute("""
            INSERT OR REPLACE INTO ratings
            (booking_id, venue_id, client_telegram_id, rating, comment)
            VALUES (?,?,?,?,?)
        """, (booking_id, venue_id, client_telegram_id, rating, comment))
        conn.commit()
        conn.close()

    def get_venue_ratings(self, venue_id):
        conn = self.get_conn()
        result = conn.execute("""
            SELECT rating, comment, rated_at FROM ratings
            WHERE venue_id=? ORDER BY rated_at DESC
        """, (venue_id,)).fetchall()
        conn.close()
        return result

    def has_rated(self, booking_id):
        conn = self.get_conn()
        result = conn.execute("SELECT id FROM ratings WHERE booking_id=?", (booking_id,)).fetchone()
        conn.close()
        return result is not None

    # ── Stats methods ────────────────────────────────────────────────────
    def get_stats(self):
        conn = self.get_conn()
        venues = conn.execute("SELECT COUNT(*) FROM venues").fetchone()[0]
        clients = conn.execute("SELECT COUNT(*) FROM clients").fetchone()[0]
        bookings = conn.execute("SELECT COUNT(*) FROM bookings").fetchone()[0]
        pending = conn.execute("SELECT COUNT(*) FROM bookings WHERE status='Pending'").fetchone()[0]
        revenue = conn.execute("SELECT SUM(commission) FROM bookings").fetchone()[0] or 0
        conn.close()
        return venues, clients, bookings, pending, revenue

    def get_revenue_by_period(self, period="all"):
        conn = self.get_conn()
        if period == "week":
            result = conn.execute("SELECT SUM(commission) FROM bookings WHERE placed_at >= datetime('now', '-7 days')").fetchone()[0]
        elif period == "month":
            result = conn.execute("SELECT SUM(commission) FROM bookings WHERE placed_at >= datetime('now', '-30 days')").fetchone()[0]
        elif period == "year":
            result = conn.execute("SELECT SUM(commission) FROM bookings WHERE placed_at >= datetime('now', '-365 days')").fetchone()[0]
        else:
            result = conn.execute("SELECT SUM(commission) FROM bookings").fetchone()[0]
        conn.close()
        return result or 0

    def get_total_revenue(self):
        return self.get_revenue_by_period("all")