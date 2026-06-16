# TuySavdo — Translations: English and Uzbek only

TRANSLATIONS = {
    "en": {
        "choose_language": "🌐 *Welcome to TuySavdo!*\n\nPlease choose your language:\n\nIltimos, tilingizni tanlang:",
        "language_set": "✅ Language set to English!",
        "register_venue_owner": "🏛 Register as Venue Owner",
        "register_client": "🎊 Register as Client",
        "welcome_new": "🎊 *Welcome to TuySavdo*\nUzbekistan's Wedding Venue Booking Platform!\n\nPlease choose your role:",
        "welcome_back_venue": "🏛 Welcome back to *TuySavdo*!\n\nManage your venue and bookings below:",
        "welcome_back_client": "🎊 Welcome back to *TuySavdo*!\n\nFind and book the perfect venue below:",
        "choose_option": "Please choose an option from the menu.",
        "cancelled": "❌ Cancelled.",

        # Buttons
        "cancel": "❌ Cancel",
        "skip": "⏭ Skip",
        "skip_photo": "⏭ Skip Photo",
        "done": "✔️ Done",
        "none_of_these": "❌ None of these",
        "catering": "✅ Catering",
        "music": "✅ Music",
        "decoration": "✅ Decoration",
        "amenity_catering": "🍽 Catering",
        "amenity_music": "🎵 Music",
        "amenity_decoration": "💐 Decoration",
        "none": "None",
        "no_ratings": "No ratings yet",
        "reviews": "reviews",
        "guests": "guests",
        "seat": "seat",
        "selected": "✨ Selected",

        # Venue menu
        "my_venue": "🏛 My Venue",
        "edit_venue": "✏️ Edit Venue",
        "my_bookings": "📋 My Bookings",
        "my_stats": "📊 My Stats",
        "availability": "🗓 Availability",
        "my_ratings": "⭐ My Ratings",
        "my_dashboard": "🌐 My Dashboard",

        # Client menu
        "browse_venues": "🔍 Browse Venues",
        "book_venue_btn": "📅 Book a Venue",
        "ai_advice": "🤖 AI Advice",
        "my_bookings_client": "📋 My Bookings",
        "rate_venue": "⭐ Rate a Venue",
        "track_bookings": "🌐 Track Bookings",

        # Venue registration
        "ask_owner_name": "Let's register your venue!\n\nWhat is your full name?",
        "ask_venue_name": "What is the name of your venue?",
        "ask_venue_address": "What is your venue's address?",
        "ask_venue_desc": "Add a short description of your venue:\n(e.g. Elegant wedding hall with garden and VIP rooms)",
        "ask_venue_capacity": "Maximum capacity? (e.g. 500)",
        "ask_venue_price": "Price per seat in USD? (e.g. 25)",
        "ask_venue_contact": "Your contact number?",
        "ask_venue_location": "📍 Please share your venue location!\n\nTap 📎 → Location → Send your location",
        "location_required": "⚠️ Please share your location using 📎 → Location",
        "ask_venue_amenities": "🎊 What amenities does your venue offer?\n\nTap each to select, then ✔️ Done:\n\nSelected: *None yet*",
        "select_more_or_done": "✨ Selected: *{selected}*\n\nSelect more or tap ✔️ Done:",
        "ask_extra_amenities": "✨ Any additional services your venue offers?\n\n(e.g. Private parking, VIP rooms, outdoor garden)\n\nOr tap Skip.",
        "ask_venue_photo": "📸 Send a photo of your venue!\nOr tap Skip Photo.",
        "ask_payment_details": "💳 *Payment Details*\n\nEnter your bank card number or account details.\nClients will use this to pay the 50% down payment.\n\n(e.g. Uzcard: 8600 1234 5678 9012 — Your Name)",
        "invalid_number": "Please enter a valid number.",
        "venue_registered": (
            "✅ *Venue Registered Successfully!*\n\n"
            "👤 Owner: {owner}\n"
            "🏛 Venue: {venue_name}\n"
            "📍 Address: {address}\n"
            "📝 {desc}\n"
            "👥 Capacity: {capacity} guests\n"
            "💵 Price: ${price}/seat\n"
            "📞 Contact: {contact}\n"
            "✨ Amenities: {amenities}\n"
            "✨ Extra services: {extra}\n"
            "💳 Payment details saved ✅\n\n"
            "Clients can now find and book your venue!"
        ),

        # My Venue display
        "my_venue_display": (
            "🏛 *Your Venue:*\n\n"
            "🏛 Name: {venue_name}\n"
            "📍 Address: {address}\n"
            "📝 {desc}\n"
            "👥 Capacity: {capacity} guests\n"
            "💵 Price: ${price}/seat\n"
            "📞 Contact: {contact}\n"
            "✨ Amenities: {amenities}\n"
            "✨ Extra services: {extra}\n"
            "💳 Payment: {payment}\n"
            "⭐ Rating: {stars} ({avg}/5 from {count} reviews)"
        ),
        "no_venue": "You have no venue registered.",
        "open_dashboard": "📊 Open your Venue Dashboard:",

        # Edit venue
        "edit_venue_title": "✏️ *Edit Venue*\n\nWhat would you like to update?",
        "edit_desc": "📝 Description",
        "edit_capacity": "👥 Capacity",
        "edit_price": "💵 Price",
        "edit_contact": "📞 Contact",
        "edit_payment": "💳 Payment Details",
        "edit_photo": "📸 Update Photo",
        "send_new_photo": "📸 Send your new venue photo:",
        "enter_new_value": "Enter new value:",
        "photo_updated": "✅ Photo updated!",
        "please_send_photo": "Please send a photo.",
        "field_updated": "✅ {field} updated!",

        # Availability
        "all_dates_available": "🗓 *Availability Calendar*\n\n✅ All dates are available!",
        "booked_dates_title": "🗓 *Booked Dates:*\n\n",
        "booked_date_row": "❌ {date}\n",
        "other_dates_free": "\nAll other dates are ✅ available!",

        # Ratings
        "no_ratings_yet": "⭐ No ratings yet.",
        "ratings_header": "⭐ *Your Ratings:*\n\nAverage: {stars} ({avg}/5 from {count} reviews)\n\n",

        # My Bookings (venue)
        "bookings_received": "📋 *Bookings Received ({count} total):*",
        "no_bookings": "No bookings received yet.",
        "booking_item": (
            "🔹 *Booking #{id}*\n"
            "   👤 Client: {client}\n"
            "   📞 Phone: {phone}\n"
            "   💑 Couple: {couple}\n"
            "   📅 Date: {date}\n"
            "   👥 Guests: {guests}\n"
            "   ✨ Wishes: {wishes}\n"
            "   💰 Total: ${total}\n"
            "   📊 Down Payment (50%): ${down}\n"
            "   💳 Payment: {method}\n"
            "   📊 Status: {status}"
        ),

        # Stats
        "stats_display": (
            "📊 *Your Statistics:*\n\n"
            "🏛 Venue: {venue_name}\n"
            "👥 Capacity: {capacity} guests\n"
            "💵 Price: ${price}/seat\n"
            "⭐ Rating: {stars} ({avg}/5)\n\n"
            "📋 Total Bookings: {total}\n"
            "✅ Confirmed: {confirmed}\n"
            "⏳ Pending: {pending}\n"
            "❌ Rejected: {rejected}\n"
            "💰 Total Revenue: ${revenue}"
        ),

        # Payment flow (venue callbacks)
        "booking_confirmed_venue": "✅ *Booking #{id} Confirmed!*\n\nWaiting for client to make the down payment.",
        "payment_confirmed_venue": "✅ *Payment Confirmed! Booking #{id} is now CONFIRMED!*",
        "payment_not_received_venue": "❌ Payment not received for Booking #{id}.\nWaiting for client to retry.",
        "booking_rejected_venue": "❌ *Booking #{id} Rejected*",
        "confirm_btn": "✅ Confirm",
        "reject_btn": "❌ Reject",
        "payment_confirmed_btn": "✅ Payment Confirmed",
        "payment_not_received_btn": "❌ Not Received",

        # Payment flow (client receives)
        "booking_confirmed_client": (
            "🎊 *Your booking #{id} has been accepted!*\n\n"
            "🏛 Venue: {venue}\n"
            "📅 Date: {date}\n"
            "💑 Couple: {couple}\n"
            "👥 Guests: {guests}\n"
            "💰 Total Cost: ${total}\n\n"
            "📊 *Please pay the 50% down payment:*\n"
            "💳 Amount: *${down}*\n"
            "{icon} Method: {method}\n"
            "🏦 Payment Details:\n*{payment_details}*\n\n"
            "After paying, tap the button below 👇"
        ),
        "i_paid": "💳 I've Paid the Down Payment",
        "payment_sent_client": "✅ *Payment notification sent!*\n\nWaiting for venue to confirm receipt.",
        "payment_notification_venue": (
            "💳 *Payment Notification — Booking #{id}*\n\n"
            "👤 Client: {client}\n"
            "📞 Phone: {phone}\n"
            "💑 Couple: {couple}\n"
            "📅 Date: {date}\n"
            "💰 Down Payment: ${down}\n\n"
            "Please check your account and confirm!"
        ),
        "booking_fully_confirmed": (
            "🎊 *Booking #{id} is CONFIRMED!*\n\n"
            "🏛 Venue: {venue}\n"
            "📅 Date: {date}\n"
            "💑 Couple: {couple}\n\n"
            "Your wedding is booked! Congratulations! 🎉"
        ),
        "payment_not_confirmed": (
            "❌ *Payment not confirmed for Booking #{id}*\n\n"
            "The venue couldn't verify your payment.\n"
            "Please check and try again."
        ),
        "i_paid_again": "💳 I've Paid Again",
        "booking_rejected_client": (
            "❌ *Your booking #{id} has been rejected.*\n\n"
            "🏛 Venue: {venue}\n"
            "📅 Date: {date}\n\n"
            "Please try another venue."
        ),

        # Client registration
        "ask_client_name": "Welcome! What is your full name?",
        "ask_client_phone": "📞 What is your phone number?\n(e.g. +998901234567)",
        "client_registered": "✅ *Welcome, {name}!*\n\n📞 Phone: {phone}\n\nYou can now browse and book wedding venues!",

        # Browse venues
        "browse_title": "🏛 *Available Venues ({count} total):*",
        "venue_item": (
            "🏛 *{name}* (ID: {id})\n"
            "👤 Owner: {owner}\n"
            "📍 {address}\n"
            "📝 {desc}\n"
            "👥 Capacity: {capacity} guests\n"
            "💵 Price: ${price}/seat\n"
            "📞 Contact: {contact}\n"
            "✨ Amenities: {amenities}\n"
            "⭐ Rating: {stars} ({avg}/5 — {count} reviews)"
        ),
        "no_venues": "No venues registered yet.",
        "to_book": "To book tap 📅 Book a Venue",

        # Booking
        "select_venue": "📅 *Select a Venue to Book:*\n\n",
        "venue_list_item": "*ID {id}* — {name} {stars}\n   👥 {capacity} guests | 💵 ${price}/seat\n   {amenities}\n\n",
        "enter_venue_id": "Enter the Venue ID (e.g. type *1*):",
        "venue_not_found": "Venue not found. Please enter a valid ID.",
        "venue_selected": "🏛 *{name}*\n👥 {capacity} guests | 💵 ${price}/seat\n\n📅 What is your wedding date?\n(Format: DD/MM/YYYY)",
        "ask_wedding_date": "📅 What is your wedding date?\n(Format: DD/MM/YYYY)",
        "date_unavailable": "❌ *Sorry! This venue is booked on {date}*\n\nPlease choose a different date:",
        "date_available": "✅ *{date} is available!*\n\n👥 How many guests?",
        "capacity_exceeded": "❌ Maximum capacity is *{capacity} guests*.\nPlease enter up to {capacity}:",
        "ask_couple_names": "💑 What are the *bride and groom's names*?\n\n(e.g. Jasur & Malika)",
        "ask_wishes": "✨ Any additional wishes for your wedding?\n\n(e.g. flowers, photographer, fireworks)\n\nOr tap Skip.",
        "payment_summary": (
            "💰 *Payment Summary:*\n\n"
            "👥 Guests: {guests}\n"
            "💵 Price/seat: ${price}\n"
            "💰 Total Cost: ${total}\n"
            "📊 Down Payment (50%): ${down}\n\n"
            "💳 How will you pay the down payment?"
        ),
        "cash": "💵 Cash",
        "card": "💳 Card",
        "booking_sent": (
            "✅ *Booking Request Sent!*\n\n"
            "🏛 Venue: {venue}\n"
            "📅 Wedding Date: {date}\n"
            "💑 Couple: {couple}\n"
            "👥 Guests: {guests}\n"
            "✨ Wishes: {wishes}\n\n"
            "💰 Total Cost: ${total}\n"
            "📊 Down Payment (50%): ${down}\n"
            "💳 Payment: {method}\n"
            "📋 Status: Pending\n\n"
            "⏳ Waiting for venue confirmation...\n"
            "Once confirmed, you will receive payment instructions."
        ),
        "new_booking_notification": (
            "🔔 *New Booking Request!*\n\n"
            "👤 Client: {client}\n"
            "📞 Phone: {phone}\n"
            "💑 Couple: {couple}\n"
            "📅 Wedding Date: {date}\n"
            "👥 Guests: {guests}\n"
            "✨ Wishes: {wishes}\n\n"
            "💰 Total Cost: ${total}\n"
            "📊 Down Payment (50%): ${down}\n"
            "💳 Payment: {method}\n\n"
            "Go to 📋 My Bookings to confirm or reject!"
        ),

        # My Bookings (client)
        "my_bookings_title": "📋 *Your Bookings:*\n\n",
        "no_bookings_client": "You have no bookings yet!",
        "booking_item_client": (
            "🔹 Booking #{id}\n"
            "   🏛 {venue}\n"
            "   📅 {date} | 💑 {couple}\n"
            "   👥 {guests} guests\n"
            "   💰 Total: ${total} | Down: ${down}\n"
            "   💳 {method}\n"
            "   {status_icon} {status}\n\n"
        ),

        # Rating
        "rate_select": "⭐ *Select a Booking to Rate:*\n\n",
        "rate_booking_item": "*Booking #{id}* — {venue}\n   📅 {date} | 💑 {couple}\n\n",
        "enter_booking_id": "Enter the Booking ID:",
        "no_bookings_to_rate": "⭐ No confirmed bookings to rate yet!",
        "booking_not_found": "Booking not found.",
        "rate_stars_prompt": "⭐ *Rate {venue}*\n\nHow many stars?",
        "rate_comment_prompt": "💬 Add a comment!\n(Or tap Skip)",
        "rating_submitted": "✅ *Rating Submitted!*\n\n{stars} ({count}/5)\n💬 {comment}\n\nThank you!",

        # AI
        "ai_start": "🤖 *AI Venue Advisor*\n\nI will find the best venue for your wedding!\n\nHow many guests are you expecting?",
        "ai_ask_budget": "💵 Budget per seat in USD? (e.g. 30)",
        "ai_ask_date": "📅 Wedding date? (DD/MM/YYYY or Skip)",
        "ai_no_match": "❌ No venues found matching your requirements.\n\nTry increasing your budget or reducing guest count.",
        "ai_result": (
            "🤖 *AI Venue Advice — Best Match:*\n\n"
            "🏆 *{name}*\n"
            "👤 {owner} | 📞 {contact}\n"
            "📍 {address}\n"
            "📝 {desc}\n"
            "👥 Capacity: {capacity} guests\n"
            "💵 Price: ${price}/seat\n"
            "💰 Total estimate: ${total}\n"
            "📊 Down Payment (50%): ${down}\n"
            "✨ Amenities: {amenities}\n"
            "⭐ Rating: {stars} ({avg}/5 from {count} reviews)\n\n"
            "📌 *Why recommended:*\n{reason}"
        ),
        "ai_reason": (
            "💵 Price: ${price}/seat — fits your budget\n"
            "👥 Capacity: {capacity} guests — matches your requirements\n"
            "⭐ Rating: {stars} ({avg}/5 from {count} reviews)\n"
            "✨ Amenities: {amenities}\n"
            "🏆 Best overall match for your wedding"
        ),
        # Premium
        "premium_badge": "👑 PREMIUM",
        "free_badge": "🆓 FREE",
        "upgrade_title": "👑 *Upgrade to Premium*",
        "premium_benefits": (
            "👑 *TuySavdo Premium Plans*\n\n"
            "Choose the plan that fits your venue:\n\n"
            "🥉 *Basic — $25/month*\n"
            "   ✅ Verified Badge\n"
            "   🏆 Top of search results\n\n"
            "🥈 *Standard — $50/month*\n"
            "   ✅ Everything in Basic\n"
            "   📣 Featured on our Instagram & Telegram\n"
            "   📊 Advanced Analytics\n\n"
            "🥇 *VIP — $75/month*\n"
            "   ✅ Everything in Standard\n"
            "   ⚡ Priority support\n"
            "   📈 Dedicated social media post weekly\n\n"
            "💳 *How to subscribe:*\n"
            "Send payment to: *8600 0505 0000 6666*\n"
            "Then tap the button below 👇"
        ),
        "select_plan": "👑 *Select your Premium Plan:*",
        "plan_basic": "🥉 Basic — $25/month",
        "plan_standard": "🥈 Standard — $50/month",
        "plan_vip": "🥇 VIP — $75/month",
        "payment_instructions": (
            "💳 *Payment Instructions*\n\n"
            "Plan selected: *{plan}*\n"
            "Amount: *{amount}*\n\n"
            "Send payment to:\n"
            "🏦 *Uzcard: 8600 0505 0000 6666*\n"
            "👤 TuySavdo\n\n"
            "After sending payment, tap ✅ I\'ve Paid below."
        ),
        "premium_paid_client": "✅ *Payment notification sent to admin!*\n\nYour Premium will be activated within minutes after verification.",
        "premium_payment_admin": (
            "👑 *Premium Payment Request!*\n\n"
            "🏛 Venue: {venue}\n"
            "👤 Owner: {owner}\n"
            "📞 Contact: {contact}\n"
            "📋 Plan: {plan}\n"
            "💰 Amount: {amount}\n\n"
            "Please verify payment and confirm!"
        ),
        "confirm_premium_btn": "✅ Activate Premium",
        "reject_premium_btn": "❌ Reject",
        "premium_confirmed_venue": "🎉 *Your Premium has been activated!*\n\nPlan: {plan}\nValid until: {expiry}\n\nYou now appear at the TOP of all venue listings! 👑",
        "premium_rejected_venue": "❌ *Premium payment could not be verified.*\n\nPlease contact admin: @TuySavdoAdmin",
        "any_questions": "📩 Any questions? Contact: @TuySavdoAdmin",
        "already_premium": "👑 *You are already a Premium venue!*\n\nYour premium features are active.",
        "premium_activated": "👑 *Premium Activated!*\n\nVenue ID {id} is now Premium until {expiry}.",
        "premium_revoked": "❌ Premium revoked for Venue ID {id}.",
        "venue_not_found_admin": "Venue not found with ID {id}.",
        "upgrade_btn": "👑 Upgrade to Premium",
        "premium_info_btn": "ℹ️ Premium Info",
        "phase_info": (
            "📋 *TuySavdo Monetisation Model:*\n\n"
            "🆓 *Phase 1 — Launch (Current):*\n"
            "Everything is FREE. Our goal is to build the venue database and attract clients.\n\n"
            "💳 *Phase 2 — Growth:*\n"
            "After receiving 10+ confirmed bookings through TuySavdo, venues pay a small flat fee per booking. You only pay when we deliver clients.\n\n"
            "👑 *Phase 3 — Premium:*\n"
            "Optional Premium subscription for enhanced visibility, social media promotion, and verified badge.\n\n"
            "You are currently in Phase 1 — enjoy everything for FREE! 🎉"
        ),
        "current_phase": "🆓 *Currently in Phase 1 — Everything is FREE!*",
        "bookings_until_fee": "📊 You have {count} confirmed bookings. After 10, a small flat fee applies.",
    },

    "uz": {
        "choose_language": "🌐 *TuySavdo*ga xush kelibsiz!\n\nIltimos, tilingizni tanlang:\n\nPlease choose your language:",
        "language_set": "✅ Til O'zbek tiliga o'rnatildi!",
        "register_venue_owner": "🏛 To'yxona egasi sifatida ro'yxatdan o'tish",
        "register_client": "🎊 Mijoz sifatida ro'yxatdan o'tish",
        "welcome_new": "🎊 *TuySavdo*ga xush kelibsiz!\nO'zbekiston to'yxonalarini bron qilish platformasi!\n\nRolingizni tanlang:",
        "welcome_back_venue": "🏛 *TuySavdo*ga xush kelibsiz!\n\nTo'yxona va buyurtmalaringizni boshqaring:",
        "welcome_back_client": "🎊 *TuySavdo*ga xush kelibsiz!\n\nMukammal to'yxona toping va band qiling:",
        "choose_option": "Iltimos, menyudan tanlang.",
        "cancelled": "❌ Bekor qilindi.",

        # Buttons
        "cancel": "❌ Bekor qilish",
        "skip": "⏭ O'tkazib yuborish",
        "skip_photo": "⏭ Rasmni o'tkazib yuborish",
        "done": "✔️ Tayyor",
        "none_of_these": "❌ Hech biri yo'q",
        "catering": "✅ Ovqatlanish",
        "music": "✅ Musiqa",
        "decoration": "✅ Bezak",
        "amenity_catering": "🍽 Ovqatlanish",
        "amenity_music": "🎵 Musiqa",
        "amenity_decoration": "💐 Bezak",
        "none": "Yo'q",
        "no_ratings": "Hali reyting yo'q",
        "reviews": "sharh",
        "guests": "nafar",
        "seat": "o'rindiq",
        "selected": "✨ Tanlangan",

        # Venue menu
        "my_venue": "🏛 Mening to'yxonam",
        "edit_venue": "✏️ To'yxonani tahrirlash",
        "my_bookings": "📋 Buyurtmalarim",
        "my_stats": "📊 Statistikam",
        "availability": "🗓 Band kunlar",
        "my_ratings": "⭐ Reytinglarim",
        "my_dashboard": "🌐 Boshqaruv paneli",

        # Client menu
        "browse_venues": "🔍 To'yxonalarni ko'rish",
        "book_venue_btn": "📅 To'yxona band qilish",
        "ai_advice": "🤖 AI Maslahat",
        "my_bookings_client": "📋 Buyurtmalarim",
        "rate_venue": "⭐ Baho berish",
        "track_bookings": "🌐 Buyurtmalarni kuzatish",

        # Venue registration
        "ask_owner_name": "To'yxonangizni ro'yxatdan o'tkazaylik!\n\nTo'liq ismingiz nima?",
        "ask_venue_name": "To'yxonangizning nomi nima?",
        "ask_venue_address": "To'yxonangizning manzili qayerda?",
        "ask_venue_desc": "To'yxonangiz haqida qisqacha ma'lumot yozing:\n(Masalan: Bog' va VIP xonali zamonaviy to'yxona)",
        "ask_venue_capacity": "Maksimal sig'im? (Masalan: 500)",
        "ask_venue_price": "Har bir o'rindiq narxi USD da? (Masalan: 25)",
        "ask_venue_contact": "Telefon raqamingiz?",
        "ask_venue_location": "📍 To'yxonangizning joylashuvini yuboring!\n\n📎 → Joylashuv → Joylashuvni yuboring",
        "location_required": "⚠️ Iltimos, 📎 → Joylashuv orqali joylashuvingizni yuboring",
        "ask_venue_amenities": "🎊 To'yxonangizda qanday xizmatlar mavjud?\n\nHar birini tanlang, so'ng ✔️ Tayyor:\n\nTanlangan: *Hech narsa*",
        "select_more_or_done": "✨ Tanlangan: *{selected}*\n\nYana tanlang yoki ✔️ Tayyor bosing:",
        "ask_extra_amenities": "✨ Qo'shimcha xizmatlar bormi?\n\n(Masalan: Xususiy parking, VIP xonalar, ochiq hovli)\n\nYoki O'tkazib yuborish tugmasini bosing.",
        "ask_venue_photo": "📸 To'yxonangizning rasmini yuboring!\nYoki Rasmni o'tkazib yuborish tugmasini bosing.",
        "ask_payment_details": "💳 *To'lov ma'lumotlari*\n\nBank karta raqamingiz yoki hisob ma'lumotlaringizni kiriting.\nMijozlar 50% avansni shu orqali to'laydi.\n\n(Masalan: Uzcard: 8600 1234 5678 9012 — Ismingiz)",
        "invalid_number": "Iltimos, to'g'ri raqam kiriting.",
        "venue_registered": (
            "✅ *To'yxona muvaffaqiyatli ro'yxatdan o'tdi!*\n\n"
            "👤 Egasi: {owner}\n"
            "🏛 To'yxona: {venue_name}\n"
            "📍 Manzil: {address}\n"
            "📝 {desc}\n"
            "👥 Sig'im: {capacity} nafar\n"
            "💵 Narx: ${price}/o'rindiq\n"
            "📞 Telefon: {contact}\n"
            "✨ Xizmatlar: {amenities}\n"
            "✨ Qo'shimcha xizmatlar: {extra}\n"
            "💳 To'lov ma'lumotlari saqlandi ✅\n\n"
            "Mijozlar endi to'yxonangizni topib bron qilishlari mumkin!"
        ),

        # My Venue display
        "my_venue_display": (
            "🏛 *Sizning to'yxonangiz:*\n\n"
            "🏛 Nomi: {venue_name}\n"
            "📍 Manzil: {address}\n"
            "📝 {desc}\n"
            "👥 Sig'im: {capacity} nafar\n"
            "💵 Narx: ${price}/o'rindiq\n"
            "📞 Telefon: {contact}\n"
            "✨ Xizmatlar: {amenities}\n"
            "✨ Qo'shimcha xizmatlar: {extra}\n"
            "💳 To'lov: {payment}\n"
            "⭐ Reyting: {stars} ({avg}/5, {count} sharh)"
        ),
        "no_venue": "Ro'yxatdan o'tgan to'yxonangiz yo'q.",
        "open_dashboard": "📊 Boshqaruv panelingizni oching:",

        # Edit venue
        "edit_venue_title": "✏️ *To'yxonani tahrirlash*\n\nNimani yangilamoqchisiz?",
        "edit_desc": "📝 Tavsif",
        "edit_capacity": "👥 Sig'im",
        "edit_price": "💵 Narx",
        "edit_contact": "📞 Aloqa",
        "edit_payment": "💳 To'lov ma'lumotlari",
        "edit_photo": "📸 Rasmni yangilash",
        "send_new_photo": "📸 Yangi rasm yuboring:",
        "enter_new_value": "Yangi qiymat kiriting:",
        "photo_updated": "✅ Rasm yangilandi!",
        "please_send_photo": "Iltimos, rasm yuboring.",
        "field_updated": "✅ {field} yangilandi!",

        # Availability
        "all_dates_available": "🗓 *Band kunlar*\n\n✅ Barcha sanalar bo'sh!",
        "booked_dates_title": "🗓 *Band sanalar:*\n\n",
        "booked_date_row": "❌ {date}\n",
        "other_dates_free": "\nQolgan barcha sanalar ✅ bo'sh!",

        # Ratings
        "no_ratings_yet": "⭐ Hali reyting yo'q.",
        "ratings_header": "⭐ *Sizning reytinglaringiz:*\n\nO'rtacha: {stars} ({avg}/5, {count} sharh)\n\n",

        # My Bookings (venue)
        "bookings_received": "📋 *Buyurtmalar ({count} ta):*",
        "no_bookings": "Hali buyurtma yo'q.",
        "booking_item": (
            "🔹 *Buyurtma #{id}*\n"
            "   👤 Mijoz: {client}\n"
            "   📞 Telefon: {phone}\n"
            "   💑 Juftlik: {couple}\n"
            "   📅 Sana: {date}\n"
            "   👥 Mehmonlar: {guests}\n"
            "   ✨ Xohishlar: {wishes}\n"
            "   💰 Jami: ${total}\n"
            "   📊 Avans (50%): ${down}\n"
            "   💳 To'lov: {method}\n"
            "   📊 Holat: {status}"
        ),

        # Stats
        "stats_display": (
            "📊 *Sizning statistikangiz:*\n\n"
            "🏛 To'yxona: {venue_name}\n"
            "👥 Sig'im: {capacity} nafar\n"
            "💵 Narx: ${price}/o'rindiq\n"
            "⭐ Reyting: {stars} ({avg}/5)\n\n"
            "📋 Jami buyurtmalar: {total}\n"
            "✅ Tasdiqlangan: {confirmed}\n"
            "⏳ Kutilmoqda: {pending}\n"
            "❌ Rad etilgan: {rejected}\n"
            "💰 Jami daromad: ${revenue}"
        ),

        # Payment flow (venue callbacks)
        "booking_confirmed_venue": "✅ *#{id} buyurtma tasdiqlandi!*\n\nMijozning avans to'lovini kutmoqda.",
        "payment_confirmed_venue": "✅ *To'lov tasdiqlandi! #{id} buyurtma TASDIQLANDI!*",
        "payment_not_received_venue": "❌ #{id} buyurtma uchun to'lov kelmadi.\nMijoz qayta urinishini kutmoqda.",
        "booking_rejected_venue": "❌ *#{id} buyurtma rad etildi*",
        "confirm_btn": "✅ Tasdiqlash",
        "reject_btn": "❌ Rad etish",
        "payment_confirmed_btn": "✅ To'lov tasdiqlandi",
        "payment_not_received_btn": "❌ Kelmadi",

        # Payment flow (client receives)
        "booking_confirmed_client": (
            "🎊 *#{id} buyurtmangiz qabul qilindi!*\n\n"
            "🏛 To'yxona: {venue}\n"
            "📅 Sana: {date}\n"
            "💑 Juftlik: {couple}\n"
            "👥 Mehmonlar: {guests}\n"
            "💰 Jami narx: ${total}\n\n"
            "📊 *50% avansni to'lang:*\n"
            "💳 Summa: *${down}*\n"
            "{icon} Usul: {method}\n"
            "🏦 To'lov ma'lumotlari:\n*{payment_details}*\n\n"
            "To'lovdan so'ng quyidagi tugmani bosing 👇"
        ),
        "i_paid": "💳 Avansni to'ladim",
        "payment_sent_client": "✅ *To'lov xabari yuborildi!*\n\nTo'yxona tasdiqini kuting.",
        "payment_notification_venue": (
            "💳 *To'lov xabarnomasi — Buyurtma #{id}*\n\n"
            "👤 Mijoz: {client}\n"
            "📞 Telefon: {phone}\n"
            "💑 Juftlik: {couple}\n"
            "📅 Sana: {date}\n"
            "💰 Avans: ${down}\n\n"
            "Hisobingizni tekshiring va tasdiqlang!"
        ),
        "booking_fully_confirmed": (
            "🎊 *#{id} buyurtma TASDIQLANDI!*\n\n"
            "🏛 To'yxona: {venue}\n"
            "📅 Sana: {date}\n"
            "💑 Juftlik: {couple}\n\n"
            "To'yingiz band qilindi! Tabriklaymiz! 🎉"
        ),
        "payment_not_confirmed": (
            "❌ *#{id} buyurtma uchun to'lov tasdiqlanmadi*\n\n"
            "To'yxona to'lovni topa olmadi.\n"
            "Iltimos, tekshirib qayta urinib ko'ring."
        ),
        "i_paid_again": "💳 Qayta to'ladim",
        "booking_rejected_client": (
            "❌ *#{id} buyurtmangiz rad etildi.*\n\n"
            "🏛 To'yxona: {venue}\n"
            "📅 Sana: {date}\n\n"
            "Boshqa to'yxonani sinab ko'ring."
        ),

        # Client registration
        "ask_client_name": "Xush kelibsiz! To'liq ismingiz nima?",
        "ask_client_phone": "📞 Telefon raqamingiz?\n(Masalan: +998901234567)",
        "client_registered": "✅ *Xush kelibsiz, {name}!*\n\n📞 Telefon: {phone}\n\nEndi to'yxonalarni ko'rib bron qilishingiz mumkin!",

        # Browse venues
        "browse_title": "🏛 *Mavjud to'yxonalar ({count} ta):*",
        "venue_item": (
            "🏛 *{name}* (ID: {id})\n"
            "👤 Egasi: {owner}\n"
            "📍 {address}\n"
            "📝 {desc}\n"
            "👥 Sig'im: {capacity} nafar\n"
            "💵 Narx: ${price}/o'rindiq\n"
            "📞 Telefon: {contact}\n"
            "✨ Xizmatlar: {amenities}\n"
            "⭐ Reyting: {stars} ({avg}/5 — {count} sharh)"
        ),
        "no_venues": "Hali ro'yxatdan o'tgan to'yxona yo'q.",
        "to_book": "Band qilish uchun 📅 To'yxona band qilish tugmasini bosing",

        # Booking
        "select_venue": "📅 *Band qilish uchun to'yxona tanlang:*\n\n",
        "venue_list_item": "*ID {id}* — {name} {stars}\n   👥 {capacity} nafar | 💵 ${price}/o'rindiq\n   {amenities}\n\n",
        "enter_venue_id": "To'yxona ID raqamini kiriting (Masalan: *1*):",
        "venue_not_found": "To'yxona topilmadi. To'g'ri ID kiriting.",
        "venue_selected": "🏛 *{name}*\n👥 {capacity} nafar | 💵 ${price}/o'rindiq\n\n📅 To'y sanasi?\n(Format: KK/OO/YYYY)",
        "ask_wedding_date": "📅 To'y sanasi?\n(Format: KK/OO/YYYY)",
        "date_unavailable": "❌ *Kechirasiz! Bu to'yxona {date} kuni band!*\n\nBoshqa sana tanlang:",
        "date_available": "✅ *{date} sanasi bo'sh!*\n\n👥 Nechta mehmon bo'ladi?",
        "capacity_exceeded": "❌ Maksimal sig'im *{capacity} nafar*.\nIltimos, {capacity} gacha kiriting:",
        "ask_couple_names": "💑 *Kelin va kuyovning ismlari?*\n\n(Masalan: Jasur va Malika)",
        "ask_wishes": "✨ To'y uchun qo'shimcha xohishlaringiz?\n\n(Masalan: gullar, fotograf, salut)\n\nYoki O'tkazib yuborish tugmasini bosing.",
        "payment_summary": (
            "💰 *To'lov xulosasi:*\n\n"
            "👥 Mehmonlar: {guests}\n"
            "💵 Narx/o'rindiq: ${price}\n"
            "💰 Umumiy narx: ${total}\n"
            "📊 Avans (50%): ${down}\n\n"
            "💳 Avans to'lovini qanday amalga oshirasiz?"
        ),
        "cash": "💵 Naqd pul",
        "card": "💳 Karta",
        "booking_sent": (
            "✅ *Buyurtma so'rovi yuborildi!*\n\n"
            "🏛 To'yxona: {venue}\n"
            "📅 To'y sanasi: {date}\n"
            "💑 Juftlik: {couple}\n"
            "👥 Mehmonlar: {guests}\n"
            "✨ Xohishlar: {wishes}\n\n"
            "💰 Umumiy narx: ${total}\n"
            "📊 Avans (50%): ${down}\n"
            "💳 To'lov: {method}\n"
            "📋 Holat: Kutilmoqda\n\n"
            "⏳ To'yxona tasdig'i kutilmoqda...\n"
            "Tasdiqlangandan so'ng to'lov ma'lumotlari yuboriladi."
        ),
        "new_booking_notification": (
            "🔔 *Yangi buyurtma so'rovi!*\n\n"
            "👤 Mijoz: {client}\n"
            "📞 Telefon: {phone}\n"
            "💑 Juftlik: {couple}\n"
            "📅 To'y sanasi: {date}\n"
            "👥 Mehmonlar: {guests}\n"
            "✨ Xohishlar: {wishes}\n\n"
            "💰 Umumiy narx: ${total}\n"
            "📊 Avans (50%): ${down}\n"
            "💳 To'lov: {method}\n\n"
            "📋 Buyurtmalarim bo'limiga o'ting!"
        ),

        # My Bookings (client)
        "my_bookings_title": "📋 *Sizning buyurtmalaringiz:*\n\n",
        "no_bookings_client": "Sizda hali buyurtma yo'q!",
        "booking_item_client": (
            "🔹 Buyurtma #{id}\n"
            "   🏛 {venue}\n"
            "   📅 {date} | 💑 {couple}\n"
            "   👥 {guests} nafar\n"
            "   💰 Jami: ${total} | Avans: ${down}\n"
            "   💳 {method}\n"
            "   {status_icon} {status}\n\n"
        ),

        # Rating
        "rate_select": "⭐ *Baho berish uchun buyurtma tanlang:*\n\n",
        "rate_booking_item": "*Buyurtma #{id}* — {venue}\n   📅 {date} | 💑 {couple}\n\n",
        "enter_booking_id": "Buyurtma ID raqamini kiriting:",
        "no_bookings_to_rate": "⭐ Hali baholash uchun tasdiqlangan buyurtma yo'q!",
        "booking_not_found": "Buyurtma topilmadi.",
        "rate_stars_prompt": "⭐ *{venue}ni baholang*\n\nNechta yulduz?",
        "rate_comment_prompt": "💬 Izoh qoldiring!\n(Yoki O'tkazib yuborish tugmasini bosing)",
        "rating_submitted": "✅ *Baho yuborildi!*\n\n{stars} ({count}/5)\n💬 {comment}\n\nRahmat!",

        # AI
        "ai_start": "🤖 *AI To'yxona Maslahatchisi*\n\nTo'yingiz uchun eng yaxshi to'yxonani topaman!\n\nNechta mehmon bo'ladi?",
        "ai_ask_budget": "💵 Har bir o'rindiq uchun byudjet (USD)? (Masalan: 30)",
        "ai_ask_date": "📅 To'y sanasi? (KK/OO/YYYY yoki O'tkazib yuborish)",
        "ai_no_match": "❌ Talablaringizga mos to'yxona topilmadi.\n\nByudjetni oshiring yoki mehmonlar sonini kamaytiring.",
        "ai_result": (
            "🤖 *AI Maslahati — Eng yaxshi tanlov:*\n\n"
            "🏆 *{name}*\n"
            "👤 {owner} | 📞 {contact}\n"
            "📍 {address}\n"
            "📝 {desc}\n"
            "👥 Sig'im: {capacity} nafar\n"
            "💵 Narx: ${price}/o'rindiq\n"
            "💰 Taxminiy narx: ${total}\n"
            "📊 Avans (50%): ${down}\n"
            "✨ Xizmatlar: {amenities}\n"
            "⭐ Reyting: {stars} ({avg}/5, {count} sharh)\n\n"
            "📌 *Nima uchun tavsiya etildi:*\n{reason}"
        ),
        "ai_reason": (
            "💵 Narx: ${price}/o'rindiq — byudjetingizga mos\n"
            "👥 Sig'im: {capacity} nafar — talablaringizga mos\n"
            "⭐ Reyting: {stars} ({avg}/5, {count} sharh)\n"
            "✨ Xizmatlar: {amenities}\n"
            "🏆 To'yingiz uchun eng yaxshi tanlov"
        ),
        # Premium
        "premium_badge": "👑 PREMIUM",
        "free_badge": "🆓 BEPUL",
        "upgrade_title": "👑 *Premiumga o'tish*",
        "premium_benefits": (
            "👑 *TuySavdo Premium*\n\n"
            "Biznesingizni o'stirish uchun kuchli imkoniyatlar:\n\n"
            "✅ *Tasdiqlangan nishon* — mijozlar ishonchini oshiradi\n"
            "🏆 *Qidiruv natijalarida birinchi* — bepul to'yxonalardan oldin ko'rinadi\n"
            "📣 *Ijtimoiy tarmoqlarda reklama* — Instagram va Telegramda to'yxonangizni reklama qilamiz\n"
            "📊 *Kengaytirilgan statistika* — batafsil bron ma'lumotlari\n"
            "⚡ *Birinchi xabarnomalar* — tezkor bron bildirishnomalari\n\n"
            "💰 *Narxlar:*\n"
            "🆓 1-bosqich: Barcha to'yxonalar uchun BEPUL (ishga tushirish davri)\n"
            "💳 2-bosqich: Har bir tasdiqlangan bron uchun kichik to'lov\n"
            "👑 3-bosqich: Maksimal ko'rinish uchun Premium obuna\n\n"
            "📩 Premiumni faollashtirish uchun admin bilan bog'laning:\n"
            "@TuySavdoAdmin"
        ),
        "already_premium": "👑 *Siz allaqachon Premium to'yxonasiz!*\n\nPremium xususiyatlaringiz faol.",
        "premium_activated": "👑 *Premium faollashtirildi!*\n\n{id} ID to'yxona {expiry} gacha Premiumga o'tkazildi.",
        "premium_revoked": "❌ {id} ID to'yxonadan Premium bekor qilindi.",
        "venue_not_found_admin": "{id} ID bilan to'yxona topilmadi.",
        "upgrade_btn": "👑 Premiumga o'tish",
        "premium_info_btn": "ℹ️ Premium haqida",
        "phase_info": (
            "📋 *TuySavdo monetizatsiya modeli:*\n\n"
            "🆓 *1-bosqich — Ishga tushirish (Hozirgi):*\n"
            "Hamma narsa BEPUL. Maqsadimiz to'yxona bazasini yaratish va mijozlarni jalb qilish.\n\n"
            "💳 *2-bosqich — O'sish:*\n"
            "TuySavdo orqali 10+ tasdiqlangan bron olgandan so'ng, har bir bron uchun kichik to'lov olinadi. Faqat biz mijoz keltirganda to'laysiz.\n\n"
            "👑 *3-bosqich — Premium:*\n"
            "Ko'proq mijoz uchun ixtiyoriy Premium obuna, ijtimoiy tarmoqlarda reklama va tasdiqlangan nishon.\n\n"
            "Hozir 1-bosqichdamiz — hamma narsa BEPUL! 🎉"
        ),
        "current_phase": "🆓 *Hozir 1-bosqich — Hamma narsa BEPUL!*",
        "bookings_until_fee": "📊 Sizda {count} ta tasdiqlangan bron bor. 10 tadan so'ng kichik to'lov qo'llaniladi.",
    }
}


def t(telegram_id, key, db=None, **kwargs):
    """Get translation for a key in user's language."""
    lang = "en"
    if db:
        try:
            lang = db.get_user_language(telegram_id) or "en"
        except:
            lang = "en"
    if lang not in TRANSLATIONS:
        lang = "en"
    text = TRANSLATIONS[lang].get(key, TRANSLATIONS["en"].get(key, key))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except:
            pass
    return text


def get_lang_keyboard():
    from telegram import ReplyKeyboardMarkup
    return ReplyKeyboardMarkup([
        ["🇬🇧 English", "🇺🇿 O'zbek"]
    ], resize_keyboard=True, one_time_keyboard=True)