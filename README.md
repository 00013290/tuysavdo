# TuySavdo 🎊

**A Telegram-Based Smart Wedding Venue Booking Platform for Uzbekistan**

> Connecting families with wedding venues through AI-powered recommendations, structured booking management, and a two-step payment confirmation system.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [AI Venue Advisor](#ai-venue-advisor)
- [Mini Apps](#mini-apps)
- [Monetisation Model](#monetisation-model)

---

## 🌍 Overview

TuySavdo is a digital wedding venue booking platform built on Telegram, designed for the Uzbekistani wedding market. With over 200,000 weddings registered annually in Uzbekistan, venue discovery and booking still relies almost entirely on phone calls and word of mouth. TuySavdo digitises this process — allowing venue owners to register their facilities and clients to browse, compare, and book venues through a structured, AI-assisted workflow.

The platform was developed as a final year project for the BSc (Hons) Business Information Systems degree at Westminster International University in Tashkent (WIUT).

**Problem Statement:** Families planning weddings in Uzbekistan spend weeks calling venues, visiting locations in person, and negotiating without any structured comparison, availability checking, or formal booking process.

**Solution:** A Telegram-based platform that brings venue discovery, comparison, booking, and payment confirmation into a single, accessible digital workflow.

---

## ✨ Features

### For Venue Owners 🏛
- ✅ Register venue with name, address, capacity, price, contact, and GPS location
- ✅ Add amenities (catering, music, decoration) and additional services
- ✅ Upload venue photo
- ✅ Enter bank/card payment details for client transactions
- ✅ Receive instant Telegram notifications for new bookings
- ✅ Confirm or reject booking requests
- ✅ Share payment details with clients automatically upon confirmation
- ✅ Confirm payment received to finalise booking
- ✅ View availability calendar
- ✅ Track ratings and reviews
- ✅ Web-based Venue Dashboard Mini App

### For Clients 🎊
- ✅ Register with name and phone number
- ✅ Browse all venues with photos, ratings, and amenities
- ✅ AI Venue Advisor — get the best venue recommendation based on guests, budget, and date
- ✅ Book a venue with structured flow — date, guests, couple names, wishes, payment method
- ✅ Receive venue payment details automatically upon booking confirmation
- ✅ Confirm payment with I've Paid button
- ✅ Rate confirmed venues with star ratings and comments
- ✅ Web-based Client Dashboard Mini App

### For Admin 🔧
- ✅ Secure admin panel locked to administrator's Telegram ID
- ✅ Real-time platform statistics
- ✅ Booking filtering by week/month/year
- ✅ Revenue reporting with 0.1% commission breakdown
- ✅ Full user management
- ✅ Web-based Admin Dashboard Mini App

---

## 🏛 System Architecture

```
bot.py — Application Controller
    ↓
StartHandler · VenueHandler · ClientHandler · AdminHandler
    ↓
VenueAdvisor (ai.py) · Database (database.py)
    ↓
tuysavdo.db — SQLite Database
venues · bookings · clients · ratings · users
```

**Design Principles:**
- **Single Responsibility Principle** — each class handles one domain
- **Separation of Concerns** — database, AI, and UI logic are fully separated
- **Modular Architecture** — each handler is independently maintainable

---

## 🛠 Technology Stack

| Component | Technology | Justification |
|---|---|---|
| Programming Language | Python 3.11 | High readability, mature ecosystem |
| Bot Framework | python-telegram-bot 20.7 | Asynchronous, handles concurrent users |
| Database | SQLite | Serverless, built into Python standard library |
| AI Engine | Custom VenueAdvisor class | Fully controlled multi-factor scoring |
| Mini App Front-End | HTML/CSS/JavaScript | Telegram WebApp compatible |
| Hosting | GitHub Pages | Free, reliable HTTPS |
| IDE | VS Code | Lightweight with Python extensions |

---

## ⚙️ Installation

### Prerequisites
- Python 3.11+
- Telegram account
- Git

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/00013290/tuysavdo.git
cd tuysavdo
```

2. **Install dependencies**
```bash
pip install python-telegram-bot==20.7
```

3. **Configure your bot token**

Open `bot.py` and replace the TOKEN:
```python
TOKEN = "your_bot_token_here"
```

Get your token from [@BotFather](https://t.me/BotFather) on Telegram.

4. **Set your Admin Telegram ID**

Open `handlers/admin_handler.py` and `handlers/start_handler.py`:
```python
ADMIN_ID = your_telegram_id_here
```

Get your Telegram ID from [@userinfobot](https://t.me/userinfobot).

5. **Run the bot**
```bash
python bot.py
```

---

## 🚀 Usage

### Starting the Bot
Send `/start` to the bot on Telegram.

- **New users** → Choose to register as Venue Owner or Client
- **Admin** → Goes directly to Admin Panel
- **Returning users** → Sees their role-specific menu

### Venue Owner Flow
1. Register → add venue details → share GPS location → select amenities → add extra services → upload photo → enter payment details
2. Receive instant notifications for new bookings
3. Confirm booking → client receives payment details automatically
4. Verify payment received → confirm → booking finalised

### Client Flow
1. Register with name and phone number
2. Browse venues or use AI Venue Advisor
3. Book: select venue → date → guests → couple names → wishes → payment method
4. Receive payment details after venue confirms
5. Pay and tap I've Paid
6. Rate the venue after the event

### Admin Flow
1. `/start` → Admin Panel directly
2. View real-time platform statistics
3. Filter bookings by time period
4. Open Full Admin Panel (Mini App)

---

## 📁 Project Structure

```
TuySavdo/
│
├── bot.py                  # Application entry point
├── database.py             # Database class — all CRUD operations
├── ai.py                   # VenueAdvisor class — multi-factor scoring
│
├── handlers/
│   ├── __init__.py
│   ├── start_handler.py    # Conversation states, role-based routing
│   ├── venue_handler.py    # Venue registration, booking management
│   ├── client_handler.py   # Client registration, booking flow, AI advice
│   └── admin_handler.py    # Admin dashboard, revenue reporting
│
├── miniapp/
│   ├── index.html          # Admin Mini App dashboard
│   ├── venue.html          # Venue Owner Mini App
│   └── client.html         # Client Mini App
│
├── tuysavdo.db             # SQLite database (auto-generated)
└── README.md               # This file
```

---

## 🗄 Database Schema

Five relational tables:

| Table | Key Fields |
|---|---|
| **venues** | id, telegram_id, venue_name, capacity, price_per_seat, contact, latitude, longitude, payment_details, extra_amenities, photo_id |
| **bookings** | id, venue_id, client_telegram_id, event_date, guest_count, couple_names, wishes, total_cost, down_payment, status |
| **clients** | id, telegram_id, name, phone |
| **ratings** | id, booking_id, venue_id, rating (1-5), comment |
| **users** | id, telegram_id, name, role |

**Relationships:**
- VENUES (1) → receives → BOOKINGS (many)
- BOOKINGS (many) → made by → CLIENTS (1)
- BOOKINGS (1) → generates → RATINGS (1)

---

## 🤖 AI Venue Advisor

The `VenueAdvisor` class implements a multi-factor scoring algorithm:

**Scoring Weights:**
| Factor | Weight | Logic |
|---|---|---|
| Price | 35% | Lower price = higher score |
| Capacity Fit | 30% | Closer to guest count = higher score |
| Rating | 25% | Higher average rating = higher score |
| Amenities | 10% | More amenities = higher score |

**Flow:**
1. Client enters guest count, budget, and optional date
2. System filters venues by capacity and budget
3. Availability checked for specified date
4. Multi-factor scoring applied to all qualifying venues
5. Highest scoring venue returned with explanation

---

## 📱 Mini Apps

Three web-based dashboards hosted on GitHub Pages:

| Mini App | URL | Features |
|---|---|---|
| **Admin** | [index.html](https://00013290.github.io/tuysavdo/miniapp/index.html) | Stats, bookings, revenue, users |
| **Venue Owner** | [venue.html](https://00013290.github.io/tuysavdo/miniapp/venue.html) | Bookings, calendar, ratings |
| **Client** | [client.html](https://00013290.github.io/tuysavdo/miniapp/client.html) | Bookings, tracking, venues |

Real data is passed from the bot via base64-encoded URL parameters.

---

## 💰 Monetisation Model

- **Commission Rate:** 0.1% per confirmed booking
- **Calculation:** `commission = total_cost × 0.001`
- **Down Payment:** 50% of total cost collected from client before confirmation

**Example:**
- 300 guests × $30/seat = $9,000 total
- Down payment (50%): $4,500
- Platform commission (0.1%): $9

---

## 👨‍💻 Developer

**Ismoil Safarov**
BSc (Hons) Business Information Systems
Westminster International University in Tashkent (WIUT)
Student ID: 00013290

---

## 📄 License

This project was developed as part of an undergraduate dissertation at Westminster International University in Tashkent.
Copyright © University of Westminster, UK.
