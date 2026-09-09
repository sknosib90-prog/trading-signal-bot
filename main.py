import streamlit as st
from datetime import datetime
from uuid import uuid4

st.set_page_config(
    page_title="Diamond Hub | Diamond Recharge",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

GAMES = [
    {
        "id": "free-fire",
        "name": "Free Fire",
        "publisher": "Garena",
        "image": "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=900&auto=format&fit=crop&q=85",
        "description": "Fast and secure diamond recharge for Free Fire.",
        "packages": [("100 Diamonds", 95), ("310 Diamonds", 275), ("520 Diamonds", 450), ("1060 Diamonds", 890), ("2180 Diamonds", 1780)],
        "visible": True,
    },
    {
        "id": "mobile-legends",
        "name": "Mobile Legends",
        "publisher": "Moonton",
        "image": "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=900&auto=format&fit=crop&q=85",
        "description": "Instant diamond top-up for your Mobile Legends account.",
        "packages": [("86 Diamonds", 90), ("172 Diamonds", 175), ("257 Diamonds", 260), ("706 Diamonds", 695), ("1412 Diamonds", 1365)],
        "visible": True,
    },
    {
        "id": "pubg-mobile",
        "name": "PUBG Mobile",
        "publisher": "Level Infinite",
        "image": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=900&auto=format&fit=crop&q=85",
        "description": "Purchase UC securely with quick delivery.",
        "packages": [("60 UC", 95), ("325 UC", 455), ("660 UC", 895), ("1800 UC", 2260), ("3850 UC", 4490)],
        "visible": True,
    },
    {
        "id": "call-of-duty",
        "name": "Call of Duty Mobile",
        "publisher": "Activision",
        "image": "https://images.unsplash.com/photo-1593305841991-05c297ba4575?w=900&auto=format&fit=crop&q=85",
        "description": "Official-style CP recharge with easy ordering.",
        "packages": [("80 CP", 95), ("420 CP", 450), ("880 CP", 875), ("2400 CP", 2250), ("5000 CP", 4450)],
        "visible": True,
    },
    {
        "id": "valorant",
        "name": "Valorant",
        "publisher": "Riot Games",
        "image": "https://images.unsplash.com/photo-1552820728-8b83bb6b773f?w=900&auto=format&fit=crop&q=85",
        "description": "Get Valorant Points for your favorite skins.",
        "packages": [("125 VP", 115), ("420 VP", 345), ("700 VP", 565), ("1375 VP", 1100), ("2400 VP", 1850)],
        "visible": True,
    },
    {
        "id": "genshin-impact",
        "name": "Genshin Impact",
        "publisher": "HoYoverse",
        "image": "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=900&auto=format&fit=crop&q=85",
        "description": "Genesis Crystal recharge made simple.",
        "packages": [("60 Crystals", 95), ("300 Crystals", 465), ("980 Crystals", 1430), ("1980 Crystals", 2860), ("3280 Crystals", 4670)],
        "visible": True,
    },
]

if "games" not in st.session_state:
    st.session_state.games = GAMES
if "orders" not in st.session_state:
    st.session_state.orders = []
if "selected_game" not in st.session_state:
    st.session_state.selected_game = None
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

st.markdown(
    """
    <style>
        .stApp { background: #070b18; color: #f8fafc; }
        .block-container { max-width: 1240px; padding-top: 1.1rem; padding-bottom: 3rem; }
        #MainMenu, footer, header { visibility: hidden; }
        .topbar { padding: 16px 0 27px; display:flex; justify-content:space-between; align-items:center; }
        .brand { font-size:25px; font-weight:800; letter-spacing:-.8px; color:#fff; }
        .brand span { color:#35c8ff; }
        .eyebrow { color:#79ddff; font-size:13px; font-weight:700; letter-spacing:1.3px; text-transform:uppercase; }
        .hero { background: radial-gradient(circle at 78% 15%, rgba(47,181,255,.23), transparent 27%), linear-gradient(135deg,#131b40 0%,#0b1230 52%,#081326 100%); border:1px solid rgba(112,207,255,.20); border-radius:28px; padding:58px 52px; margin:5px 0 42px; overflow:hidden; }
        .hero h1 { font-size:52px; line-height:1.05; letter-spacing:-2.4px; margin:12px 0 18px; color:#fff; }
        .hero p { color:#b5c4df; font-size:18px; line-height:1.65; max-width:650px; }
        .trust { display:inline-block; margin-top:21px; color:#dceaff; background:rgba(255,255,255,.08); border:1px solid rgba(255,255,255,.1); padding:10px 15px; border-radius:99px; font-size:14px; }
        .section-title { font-size:29px; color:#fff; margin:0 0 7px; font-weight:750; letter-spacing:-.8px; }
        .section-subtitle { color:#8fa1bd; margin:0 0 23px; }
        .game-card { background:#111a30; border:1px solid #213153; border-radius:20px; overflow:hidden; min-height:325px; margin-bottom:16px; box-shadow:0 15px 30px rgba(0,0,0,.15); }
        .game-card img { width:100%; height:150px; object-fit:cover; display:block; }
        .game-content { padding:16px; }
        .game-name { color:#fff; font-weight:750; font-size:18px; margin:0; }
        .game-publisher { color:#83cfff; font-size:13px; margin:4px 0 9px; }
        .game-description { color:#9badc8; font-size:13px; line-height:1.5; min-height:38px; }
        .feature { background:linear-gradient(145deg,rgba(19,31,58,.95),rgba(13,20,40,.95)); padding:22px; min-height:144px; border:1px solid #22355c; border-radius:18px; }
        .feature-icon { font-size:27px; margin-bottom:8px; }.feature h3{margin:0 0 7px;color:#fff;font-size:16px}.feature p{margin:0;color:#9badc8;font-size:13px;line-height:1.5}
        .footer { border-top:1px solid #1e2e4d; color:#8092ad; margin-top:50px; padding:28px 0; font-size:13px; text-align:center; }
        .order-box { background:#101a31; border:1px solid #2b4776; padding:25px; border-radius:20px; }
        .admin-label { color:#78d9ff; font-weight:700; font-size:14px; }
        .stButton button { border-radius:10px !important; border:1px solid rgba(88,204,255,.35) !important; background:linear-gradient(135deg,#168cdb,#2bcbf7) !important; color:#fff !important; font-weight:700 !important; transition:all .2s ease !important; }
        .stButton button:hover { transform:translateY(-2px); box-shadow:0 8px 20px rgba(25,176,255,.25); }
        .stTextInput input, .stSelectbox div[data-baseweb='select'] > div { border-radius:10px !important; background:#0b1327 !important; border-color:#2b416b !important; color:#fff !important; }
        @media(max-width:700px) { .hero { padding:38px 25px; }.hero h1 { font-size:37px; } }
    </style>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([4, 1])
with left:
    st.markdown('<div class="brand">💎 DIAMOND<span>HUB</span></div>', unsafe_allow_html=True)
with right:
    if st.button("Admin Panel", use_container_width=True):
        st.session_state.show_admin = True

if st.session_state.get("show_admin", False):
    with st.sidebar:
        st.markdown("## 🔐 Admin Panel")
        if not st.session_state.admin_logged_in:
            password = st.text_input("Admin password", type="password")
            if st.button("Log in", use_container_width=True):
                if password == "admin123":
                    st.session_state.admin_logged_in = True
                    st.success("Admin access enabled.")
                else:
                    st.error("Incorrect password.")
            st.caption("Demo password: admin123")
        else:
            st.success("Administrator mode active")
            st.markdown("### Manage applications")
            for game in st.session_state.games[:]:
                a, b = st.columns([3, 1])
                with a:
                    visible = st.checkbox(game["name"], value=game["visible"], key=f"visible_{game['id']}")
                    game["visible"] = visible
                with b:
                    if st.button("Remove", key=f"remove_{game['id']}"):
                        st.session_state.games.remove(game)
                        st.rerun()
            st.markdown("---")
            st.markdown("### Add new application")
            with st.form("add_game"):
                new_name = st.text_input("Application name")
                new_publisher = st.text_input("Publisher")
                new_image = st.text_input("Image URL")
                new_packages = st.text_input("Packages (example: 100=95, 500=450)")
                if st.form_submit_button("Add application", use_container_width=True):
                    if new_name and new_image and new_packages:
                        try:
                            packages = []
                            for item in new_packages.split(","):
                                amount, price = item.strip().split("=")
                                packages.append((amount.strip(), int(price.strip())))
                            st.session_state.games.append({
                                "id": str(uuid4()), "name": new_name, "publisher": new_publisher or "Game Publisher",
                                "image": new_image, "description": "Secure and instant digital recharge.",
                                "packages": packages, "visible": True,
                            })
                            st.success("Application added successfully.")
                            st.rerun()
                        except (ValueError, AttributeError):
                            st.error("Use this package format: 100 Diamonds=95, 500 Diamonds=450")
                    else:
                        st.error("Please complete name, image URL and package prices.")
            st.markdown("---")
            st.markdown(f"### Orders ({len(st.session_state.orders)})")
            if st.session_state.orders:
                for order in st.session_state.orders[-5:][::-1]:
                    st.caption(f"#{order['id']} · {order['game']} · ৳{order['price']} · {order['status']}")
            if st.button("Log out", use_container_width=True):
                st.session_state.admin_logged_in = False
                st.rerun()

st.markdown(
    """
    <section class="hero">
      <div class="eyebrow">✦ Bangladesh's smart recharge platform</div>
      <h1>Your game. Your diamonds.<br><span style="color:#59d5ff">Delivered instantly.</span></h1>
      <p>Choose your favorite game, select a diamond package, and complete your recharge request in a few simple steps. Fast, secure and available every day.</p>
      <div class="trust">⭐ Trusted recharge service &nbsp; • &nbsp; ⚡ Quick processing &nbsp; • &nbsp; 🔒 Secure orders</div>
    </section>
    """,
    unsafe_allow_html=True,
)

if st.session_state.selected_game:
    selected = next((game for game in st.session_state.games if game["id"] == st.session_state.selected_game), None)
    if selected:
        if st.button("← Back to all applications"):
            st.session_state.selected_game = None
            st.rerun()
        st.markdown(f"## {selected['name']} Recharge")
        st.caption(f"{selected['publisher']} · Select a package and provide your player information")
        package_names = [f"{amount} — ৳{price}" for amount, price in selected["packages"]]
        with st.form("checkout_form"):
            first, second = st.columns(2)
            with first:
                player_id = st.text_input("Player ID / User ID", placeholder="Enter your game account ID")
            with second:
                selected_package = st.selectbox("Choose diamond package", package_names)
            third, fourth = st.columns(2)
            with third:
                contact = st.text_input("WhatsApp number", placeholder="01XXXXXXXXX")
            with fourth:
                payment = st.selectbox("Payment method", ["bKash", "Nagad", "Rocket", "Bank transfer"])
            st.info("After you submit the request, the payment information and order confirmation will be shown to you.")
            if st.form_submit_button("Continue to payment", use_container_width=True):
                if player_id and contact:
                    package_index = package_names.index(selected_package)
                    amount, price = selected["packages"][package_index]
                    order_id = str(uuid4())[:8].upper()
                    st.session_state.orders.append({
                        "id": order_id, "game": selected["name"], "package": amount,
                        "price": price, "player_id": player_id, "contact": contact,
                        "payment": payment, "status": "Pending payment", "created_at": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                    })
                    st.success(f"Order #{order_id} created successfully. Send ৳{price} through {payment} and use your order ID as the payment reference.")
                    st.balloons()
                else:
                    st.error("Please enter your Player ID and WhatsApp number.")
else:
    visible_games = [game for game in st.session_state.games if game["visible"]]
    st.markdown('<h2 class="section-title">Choose your application</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Select a game to view available diamond packages and prices.</p>', unsafe_allow_html=True)

    if visible_games:
        for start in range(0, len(visible_games), 3):
            columns = st.columns(3)
            for column, game in zip(columns, visible_games[start:start + 3]):
                with column:
                    st.markdown(
                        f'''<div class="game-card">
                            <img src="{game['image']}" alt="{game['name']}">
                            <div class="game-content">
                                <p class="game-name">{game['name']}</p>
                                <p class="game-publisher">{game['publisher']}</p>
                                <p class="game-description">{game['description']}</p>
                            </div>
                        </div>''',
                        unsafe_allow_html=True,
                    )
                    if st.button("View diamond packages →", key=f"select_{game['id']}", use_container_width=True):
                        st.session_state.selected_game = game["id"]
                        st.rerun()
    else:
        st.info("No applications are currently available. Please check again later.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Why DiamondHub?</h2>', unsafe_allow_html=True)
    feature_columns = st.columns(4)
    features = [
        ("⚡", "Quick requests", "Your recharge request is processed as quickly as possible."),
        ("🔒", "Safe ordering", "Your player information is used only to complete your order."),
        ("💳", "Easy payments", "Pay with bKash, Nagad, Rocket or bank transfer."),
        ("💬", "Customer support", "Our support team is available when you need help."),
    ]
    for column, (icon, title, text) in zip(feature_columns, features):
        with column:
            st.markdown(f'<div class="feature"><div class="feature-icon">{icon}</div><h3>{title}</h3><p>{text}</p></div>', unsafe_allow_html=True)

st.markdown('<div class="footer">💎 <b>DIAMONDHUB</b> &nbsp;|&nbsp; Professional digital recharge platform &nbsp;|&nbsp; © 2025 All rights reserved.</div>', unsafe_allow_html=True)
