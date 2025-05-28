import streamlit as st
import ipaddress
import random
import time # For challenge mode timer

# --- Page Configuration (must be the first Streamlit command) ---
st.set_page_config(
    page_title="IP Networking Mastery",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Font Awesome CDN (for icons in the redesigned solution) ---
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">', unsafe_allow_html=True)


# --- Session State Initialization ---
# General
if 'mode' not in st.session_state:
    st.session_state.mode = "Practice"  # Practice | Challenge
if 'current_module' not in st.session_state:
    st.session_state.current_module = "IPv4 Subnetting Practice"

# For Subnetting Practice Module (Practice & Challenge)
if 'current_subnet_question' not in st.session_state:
    st.session_state.current_subnet_question = None
if 'user_practice_answers' not in st.session_state: # Store user's practice answers
    st.session_state.user_practice_answers = {}
if 'practice_submission_feedback' not in st.session_state: # Store feedback after practice submission
    st.session_state.practice_submission_feedback = None
if 'show_full_solution_practice' not in st.session_state:
    st.session_state.show_full_solution_practice = False
if 'practice_questions_generated' not in st.session_state:
    st.session_state.practice_questions_generated = 0


# For Challenge Mode Specifics
if 'challenge_active' not in st.session_state:
    st.session_state.challenge_active = False
if 'challenge_start_time' not in st.session_state:
    st.session_state.challenge_start_time = 0.0
if 'challenge_duration_seconds' not in st.session_state:
    st.session_state.challenge_duration_seconds = 60 # Default 1 minute
if 'challenge_timer_display' not in st.session_state: # Placeholder for timer display
    st.session_state.challenge_timer_display = None
if 'challenge_correct_score' not in st.session_state:
    st.session_state.challenge_correct_score = 0
if 'challenge_incorrect_score' not in st.session_state:
    st.session_state.challenge_incorrect_score = 0
if 'challenge_questions_attempted' not in st.session_state:
    st.session_state.challenge_questions_attempted = 0


# --- Theme Configuration (DARK MODE ONLY) & CSS ---
DARK_THEME_CSS = """
    <style>
        /* Dark Theme Styles */
        body { color: #E0E0E0; background-color: #121212; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;}
        .stApp { background-color: #121212; }
        .stSidebar { background-color: #1E1E1E !important; }

        /* REMOVED: .question-box, .answer-box, .explanation-box, .input-form-box specific styling */
        /* Content will now sit directly on the page background or within Streamlit's default component styling */

        .stButton>button {
            background-color: #007ACC; color: white; font-weight: 600;
            padding: 0.7em 1.4em; border-radius: 8px; border: 1px solid #005A99;
            box-shadow: 0 3px 6px rgba(0,0,0,0.25); transition: background-color 0.3s ease, transform 0.1s ease;
        }
        .stButton>button:hover { background-color: #005A99; transform: scale(1.02); }
        .stButton>button:active { transform: scale(0.98); }
        
        .stButton>button.primary { background-color: #00A36C; border: 1px solid #007A50;}
        .stButton>button.primary:hover { background-color: #007A50; }

        h1 { color: #4D9EFF; text-align: center; padding-bottom: 0.5em; font-weight: 700; }
        h2 { color: #C0C0C0; border-bottom: 2px solid #007ACC; padding-bottom: 0.4em; margin-top: 1.8em; font-weight: 600;}
        /* Reduced margin for h3 (st.subheader) */
        h3 { 
            color: #A0A0A0; 
            margin-top: 0.8em !important; /* Reduced top margin */
            margin-bottom: 0.6em !important; /* Adjusted bottom margin */
            font-weight: 500;
        }
        h4 { color: #80BFFF; } 

        .stRadio > label > div > p { color: #E0E0E0 !important; }
        .stTextInput > div > div > input, 
        .stTextArea > div > textarea,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div { 
            background-color: #2C2C2C !important; 
            color: #E0E0E0 !important; 
            border: 1px solid #444444 !important; 
            border-radius: 8px !important;
        }
        .stSelectbox > div > div > div[data-baseweb="select"] > div { color: #E0E0E0 !important; }
        .stSelectbox > div > div:hover { border-color: #007ACC !important; }


        .stExpander header { color: #4D9EFF; font-weight: bold; }
        .stExpander { border: 1px solid #333333; border-radius: 8px; margin-top:1em; } /* Added margin-top to expander */
        
        .footer { text-align: center; padding: 2em 0; font-size: 0.9em; color: #888888; }
        .code-block { 
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
            padding: 0.6em 0.8em; border-radius: 6px; word-break: break-all; 
            display: inline-block; border: 1px solid rgba(128,128,128,0.2);
            background-color: rgba(200, 200, 200, 0.1);
        }
        .stAlert { border-radius: 8px; background-color: #2C2C2C; color: #E0E0E0; border-color: #444; }

        .stApp > header { display: none; } 
        .stSidebar .stButton>button { width: 100%; margin-bottom: 0.6em; }
        .stSidebar .stRadio > label { 
            padding: 0.6em 0.8em; font-weight: 500; border-radius: 6px;
            transition: background-color 0.2s ease; margin-bottom: 0.2em;
        }
        .stSidebar .stRadio > label:hover { background-color: rgba(255,255,255,0.06); }
        .stSidebar h1 { font-size: 1.8em; color: #4D9EFF; text-align: left; margin-bottom: 0.8em;}

        .feedback-item { padding: 0.8em; border-radius: 6px; margin-bottom: 0.5em; border-left-width: 5px; border-left-style: solid; }
        .feedback-item.correct { border-left-color: #4CAF50; background-color: rgba(76, 175, 80, 0.1); }
        .feedback-item.incorrect { border-left-color: #F44336; background-color: rgba(244, 67, 54, 0.1); }
        .feedback-item strong { display: inline-block; min-width: 180px; } 
        
        .challenge-stats-bar { 
            font-size: 1.2em; font-weight: bold; margin-bottom: 1em; text-align: center;
            padding: 0.8em; background-color: #1E1E1E; border-radius: 8px;
            border: 1px solid #333;
            display: flex; justify-content: space-around; align-items: center;
        }
        .challenge-stats-bar span { margin: 0 10px; }
        .timer-display { color: #FFC107; font-size: 1.3em;}
        .score-display-correct { color: #4CAF50; }
        .score-display-incorrect { color: #F44336; }

        /* --- CSS for Redesigned Solution Items (no longer in a box) --- */
        /* .solution-box CSS removed */
        
        .solution-section-header { /* New class for h5 if needed, or target h5 directly */
            color: #6FA8DC; 
            margin-top: 1.2em; /* Space above section header */
            margin-bottom: 0.8em;
            padding-bottom: 0.3em;
            border-bottom: 1px solid #444;
            font-weight: 600;
            display: flex; 
            align-items: center; 
        }
        .solution-section-header i { 
            margin-right: 0.5em;
            color: #6FA8DC; 
        }
        .solution-item {
            padding: 0.6em 0;
            margin-bottom: 0.4em;
            display: flex; 
            flex-wrap: wrap; 
            align-items: center; 
        }
        .solution-item strong {
            color: #B0B0B0; 
            min-width: 200px; 
            margin-right: 0.8em;
            font-weight: 500;
        }
        .solution-item span:not(.code-block) { 
            color: #E0E0E0;
            font-weight: 500;
        }
        .solution-item .code-block { 
            background-color: rgba(77, 158, 255, 0.1); 
            border: 1px solid rgba(77, 158, 255, 0.3);
            padding: 0.4em 0.7em;
            font-size: 0.95em;
        }
        .prominent-code { 
            font-weight: bold !important;
            color: #79C0FF !important; 
            background-color: rgba(77, 158, 255, 0.15) !important;
            border-color: rgba(77, 158, 255, 0.5) !important;
            padding: 0.5em 0.8em !important;
        }
        .solution-item.full-width {
            display: block; 
        }
        .solution-item.full-width strong {
            display: block;
            margin-bottom: 0.3em;
        }
        .solution-hr {
            border: none;
            border-top: 1px dashed #444;
            margin-top: 1em;
            margin-bottom: 1.5em;
        }
        .binary-item .code-block { 
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
            letter-spacing: 0.5px; 
            font-size: 0.9em;
            display: block; 
            width: fit-content; 
        }

    </style>
"""
st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)

# --- Helper Functions ---
IP_CLASS_OPTIONS = [
    "Public Class A", "Public Class B", "Public Class C",
    "Private Class A", "Private Class B", "Private Class C",
    "D (Multicast)", "E (Experimental)", "Loopback", "Link-Local (APIPA)",
    "Unspecified (0.0.0.0)", "Limited Broadcast (255.255.255.255)", "Special/Other"
]

def get_ip_class_simple(ip_address_obj): 
    first_octet = ip_address_obj.packed[0]
    if ip_address_obj.is_multicast: return "D (Multicast)"
    if ip_address_obj.is_loopback: return "Loopback"
    if ip_address_obj.is_link_local: return "Link-Local (APIPA)"
    if str(ip_address_obj) == "0.0.0.0": return "Unspecified (0.0.0.0)"
    if str(ip_address_obj) == "255.255.255.255": return "Limited Broadcast (255.255.255.255)"

    is_private = ip_address_obj.is_private
    cls_letter = ""
    if 1 <= first_octet <= 126: cls_letter = "A"
    elif 128 <= first_octet <= 191: cls_letter = "B"
    elif 192 <= first_octet <= 223: cls_letter = "C"
    elif 240 <= first_octet <= 254: return "E (Experimental)"

    if is_private:
        if cls_letter == "A" and ip_address_obj.packed[0] == 10: return "Private Class A"
        if cls_letter == "B" and ip_address_obj.packed[0] == 172 and 16 <= ip_address_obj.packed[1] <= 31 : return "Private Class B"
        if cls_letter == "C" and ip_address_obj.packed[0] == 192 and ip_address_obj.packed[1] == 168 : return "Private Class C"
    elif cls_letter:
        return f"Public Class {cls_letter}"
    return "Special/Other"

def get_ip_class_detailed(ip_address_obj): 
    first_octet = ip_address_obj.packed[0]
    if ip_address_obj.is_multicast: return "D (Multicast)"
    if ip_address_obj.is_loopback: return "Loopback Address (e.g., 127.0.0.1)"
    if ip_address_obj.is_link_local: return "Link-Local Address (APIPA, 169.254.0.0/16)"
    if ip_address_obj.is_private:
        cls_simple = ""
        if 10 == first_octet: cls_simple = "A"
        elif 172 == first_octet and 16 <= ip_address_obj.packed[1] <= 31: cls_simple = "B"
        elif 192 == first_octet and 168 == ip_address_obj.packed[1]: cls_simple = "C"
        return f"Private Use Address (RFC 1918, nominally Class {cls_simple} block)"
    if ip_address_obj.is_reserved: return "Reserved (IETF Protocol)"
    if ip_address_obj.is_global:
        if 1 <= first_octet <= 126: return "Public (Historically Class A range)"
        if 128 <= first_octet <= 191: return "Public (Historically Class B range)"
        if 192 <= first_octet <= 223: return "Public (Historically Class C range)"
    if 240 <= first_octet <= 255 and str(ip_address_obj) != "255.255.255.255": return "E (Experimental / Future Use)"
    if str(ip_address_obj) == "0.0.0.0": return "Unspecified Address (0.0.0.0)"
    if str(ip_address_obj) == "255.255.255.255": return "Limited Broadcast Address (255.255.255.255)"
    return "Special Purpose or Unknown"


def get_binary_representation(ip_or_mask_str): 
    try:
        ip_or_mask_str = ip_or_mask_str.replace(" ", "")
        if '.' in ip_or_mask_str: 
            parts = ip_or_mask_str.split('.')
            if len(parts) != 4: return "Invalid Format"
            octets = []
            for part in parts:
                if not (len(part) == 8 and all(c in '01' for c in part)):
                    return "Invalid Binary Octet"
                octets.append(part)
            return ".".join(octets)
        elif all(c in '01' for c in ip_or_mask_str) and len(ip_or_mask_str) == 32: 
            return f"{ip_or_mask_str[0:8]}.{ip_or_mask_str[8:16]}.{ip_or_mask_str[16:24]}.{ip_or_mask_str[24:32]}"
        else: 
            ipaddress.ip_address(ip_or_mask_str) 
            return ".".join(format(int(octet), '08b') for octet in ip_or_mask_str.split("."))
    except ValueError: 
        return "Invalid IP/Mask for Binary"
    except Exception:
        return "Conversion Error"

def generate_random_ip_scenario():
    scenario_type_weights = ["standard_subnet"]*6 + ["edge_cidr"]*3 + ["specific_ip"]*1
    scenario_type = random.choice(scenario_type_weights)

    if scenario_type == "specific_ip":
        edge_ips = [
            ("0.0.0.0", random.choice([0, 8, 16, 24, 32])),
            ("127.0.0.1", random.choice([8, 32])),
            ("169.254.10.20", random.choice([16, 24, 32])),
            (f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}", random.choice([8, random.randint(9,30)])),
            (f"172.{random.randint(16,31)}.{random.randint(0,255)}.{random.randint(0,255)}", random.choice([12, random.randint(13,30)])),
            (f"192.168.{random.randint(0,255)}.{random.randint(0,255)}", random.choice([16, random.randint(17,30)])),
            ("224.0.0.1", random.choice([4, 24, 32])),
            ("255.255.255.255", 32)
        ]
        ip_str, cidr = random.choice(edge_ips)
    else:
        first_octet = random.randint(1, 223)
        if first_octet == 169 and random.randint(0,255) == 254:
             first_octet = random.randint(1,168)

        ip_str = f"{first_octet}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

        if scenario_type == "edge_cidr":
            possible_cidrs = [0, 1, 2, 3, 4, 5, 6, 7, 30, 31, 32]
            uncommon_cidrs = [9,10,11,13,14,15,17,18,19,21] 
            cidr = random.choice(possible_cidrs + uncommon_cidrs + [random.randint(20,29)])
        else:
            common_cidrs = list(range(8, 31)) 
            weights = [1]*len(common_cidrs)
            for i, c_val in enumerate(common_cidrs):
                if c_val in [8,16,24]: weights[i] = 4 
                if c_val in [25,26,27,28,29,30]: weights[i] = 2 
            cidr = random.choices(common_cidrs, weights=weights, k=1)[0]

    try:
        if cidr == 0 and ip_str != "0.0.0.0":
            ip_interface = ipaddress.IPv4Interface(f"0.0.0.0/{cidr}") 
        elif cidr < 31 and ip_str == str(ipaddress.IPv4Network(f"{ip_str}/{cidr}", strict=False).network_address):
            temp_net = ipaddress.IPv4Network(f"{ip_str}/{cidr}", strict=False)
            if len(list(temp_net.hosts())) > 0:
                ip_str = str(random.choice(list(temp_net.hosts())))
            ip_interface = ipaddress.IPv4Interface(f"{ip_str}/{cidr}")

        elif cidr < 31 and ip_str == str(ipaddress.IPv4Network(f"{ip_str}/{cidr}", strict=False).broadcast_address):
            temp_net = ipaddress.IPv4Network(f"{ip_str}/{cidr}", strict=False)
            if len(list(temp_net.hosts())) > 0:
                ip_str = str(random.choice(list(temp_net.hosts())))
            ip_interface = ipaddress.IPv4Interface(f"{ip_str}/{cidr}")
        else:
            ip_interface = ipaddress.IPv4Interface(f"{ip_str}/{cidr}")
        network_obj = ip_interface.network
    except ValueError: 
        try:
            base_network = ipaddress.IPv4Network(f"0.0.0.0/{cidr}", strict=False)
            if base_network.num_addresses > 2 :
                hosts = list(base_network.hosts())
                if hosts: ip_str = str(random.choice(hosts))
                else: ip_str = str(base_network.network_address)
            else: ip_str = str(base_network.network_address)
            
            ip_interface = ipaddress.IPv4Interface(f"{ip_str}/{cidr}")
            network_obj = ip_interface.network
        except ValueError:
            return generate_random_ip_scenario() 

    num_total_addresses = network_obj.num_addresses
    usable_hosts_count = 0
    first_usable_ip_str = "N/A"
    last_usable_ip_str = "N/A"

    if cidr == 32:
        usable_hosts_count = 1
        first_usable_ip_str = str(network_obj.network_address)
        last_usable_ip_str = str(network_obj.network_address)
    elif cidr == 31: 
        usable_hosts_count = 2
        first_usable_ip_str = str(network_obj.network_address)
        last_usable_ip_str = str(network_obj.broadcast_address)
    elif num_total_addresses > 2:
        usable_hosts_count = num_total_addresses - 2
        hosts_list = list(network_obj.hosts())
        first_usable_ip_str = str(hosts_list[0])
        last_usable_ip_str = str(hosts_list[-1])
    elif num_total_addresses == 2 and cidr != 31: 
        usable_hosts_count = 0 
    elif num_total_addresses == 1 and cidr != 32:
        usable_hosts_count = 0
    
    return {
        "given_ip_str": ip_str,
        "cidr": cidr,
        "ip_interface_obj": ip_interface,
        "network_obj": network_obj,
        "correct_subnet_mask_str": str(network_obj.netmask),
        "correct_network_address_str": str(network_obj.network_address),
        "correct_broadcast_address_str": str(network_obj.broadcast_address),
        "correct_ip_class_type_str": get_ip_class_simple(ip_interface.ip),
        "correct_usable_hosts_count": usable_hosts_count,
        "correct_first_usable_ip_str": first_usable_ip_str,
        "correct_last_usable_ip_str": last_usable_ip_str,
        "correct_binary_given_ip": get_binary_representation(ip_str), 
        "correct_binary_subnet_mask": get_binary_representation(str(network_obj.netmask)),
        "num_total_addresses": num_total_addresses,
    }

def reset_practice_form_state():
    st.session_state.user_practice_answers = {}
    st.session_state.practice_submission_feedback = None
    st.session_state.show_full_solution_practice = False

def request_new_practice_question():
    st.session_state.current_subnet_question = generate_random_ip_scenario()
    reset_practice_form_state()
    st.session_state.practice_questions_generated += 1
    st.rerun() 

def request_new_challenge_question(): 
    st.session_state.current_subnet_question = generate_random_ip_scenario()
    st.rerun()


# --- UI Rendering ---
# Sidebar
with st.sidebar:
    st.markdown("<h1>📡 Networking Toolkit</h1>", unsafe_allow_html=True)
    
    st.session_state.mode = st.radio(
        "🎯 Mode Select:",
        ["Practice", "Challenge"],
        index=["Practice", "Challenge"].index(st.session_state.mode),
        key="mode_select_radio" 
    )
    st.markdown("---")

    st.subheader("📚 Learning Modules")
    module_options = [ "IPv4 Subnetting Practice", "Resource Hub" ] 
    st.session_state.current_module = st.radio(
        "Choose a module:", module_options, index=module_options.index(st.session_state.current_module)
    )
    st.markdown("---")
    if st.session_state.mode == "Practice":
        st.caption(f"Practice Questions This Session: {st.session_state.practice_questions_generated}")
    elif st.session_state.mode == "Challenge" and st.session_state.challenge_active:
        st.caption(f"Attempted: {st.session_state.challenge_questions_attempted}")
        st.caption(f"Correct: {st.session_state.challenge_correct_score} | Incorrect: {st.session_state.challenge_incorrect_score}")


# Main content area
st.title("🌐 IP Addressing & Networking Mastery")

# --- Module: IPv4 Subnetting Practice ---
if st.session_state.current_module == "IPv4 Subnetting Practice":
    
    if st.session_state.current_subnet_question is None:
        if st.session_state.mode == "Practice":
            request_new_practice_question() 
        elif st.session_state.mode == "Challenge" and not st.session_state.challenge_active:
            st.session_state.current_subnet_question = generate_random_ip_scenario()
        elif st.session_state.mode == "Challenge" and st.session_state.challenge_active:
            request_new_challenge_question() 

    q = st.session_state.current_subnet_question
    if q is None and st.session_state.mode == "Challenge" and not st.session_state.challenge_active:
        st.session_state.current_subnet_question = generate_random_ip_scenario()
        q = st.session_state.current_subnet_question


    # --- PRACTICE MODE ---
    if st.session_state.mode == "Practice":
        st.header("🧠 IPv4 Subnetting Practice")
        st.markdown("Test your subnetting skills! Enter your answers and check your work.")

        if st.button("🔄 Generate New Question", type="primary", use_container_width=True, key="practice_new_q_button"):
            request_new_practice_question() 

        if q is None: 
            st.error("Error generating question. Please try again.")
            st.stop()

        # Removed question-box div
        st.markdown(f"#### Question {st.session_state.practice_questions_generated}:")
        st.markdown(f"**Given IP Address / CIDR:** `{q['given_ip_str']}/{q['cidr']}`")
        st.markdown(f"""
        **Calculate the following:**
        - Subnet Mask
        - Network Address
        - Broadcast Address
        - Number of Usable Host IPs
        - First Usable IP Address
        - Last Usable IP Address
        - IP Address Class/Type (Simplified)
        - Binary representation of the Given IP 
        - Binary representation of the Subnet Mask
        """)
        st.markdown("---") # Added a separator

        practice_form_key = f"practice_answer_form_{st.session_state.practice_questions_generated}"
        
        with st.form(key=practice_form_key):
            # Removed input-form-box div
            st.subheader(f"✏️ Your Answers for Given IP: {q['given_ip_str']}/{q['cidr']}")
            
            u_ans_temp = {} 
            
            cols1 = st.columns(2)
            u_ans_temp['subnet_mask'] = cols1[0].text_input("Subnet Mask (e.g., 255.255.255.0)", key=f"p_sm_{practice_form_key}")
            u_ans_temp['network_address'] = cols1[1].text_input("Network Address (e.g., 192.168.1.0)", key=f"p_na_{practice_form_key}")
            
            cols2 = st.columns(2)
            u_ans_temp['broadcast_address'] = cols2[0].text_input("Broadcast Address (e.g., 192.168.1.255)", key=f"p_ba_{practice_form_key}")
            u_ans_temp['usable_hosts_count'] = cols2[1].number_input("Number of Usable Host IPs", min_value=0, step=1, value=None, key=f"p_uhc_{practice_form_key}")
            
            cols3 = st.columns(2)
            u_ans_temp['first_usable_ip'] = cols3[0].text_input("First Usable IP", key=f"p_fuip_{practice_form_key}")
            u_ans_temp['last_usable_ip'] = cols3[1].text_input("Last Usable IP", key=f"p_luip_{practice_form_key}")
            
            u_ans_temp['ip_class_type'] = st.selectbox("IP Address Class/Type", options=[""] + IP_CLASS_OPTIONS, index=0, key=f"p_ict_{practice_form_key}")
            
            st.markdown("---")
            st.markdown("##### Binary Representations (e.g., 11000000.10101000...):")
            cols4 = st.columns(2)
            u_ans_temp['binary_given_ip'] = cols4[0].text_input("Binary of Given IP", key=f"p_bip_{practice_form_key}")
            u_ans_temp['binary_subnet_mask'] = cols4[1].text_input("Binary of Subnet Mask", key=f"p_bsm_{practice_form_key}")
            
            practice_submit_button = st.form_submit_button(label="✔️ Submit My Answers")

        if practice_submit_button:
            st.session_state.user_practice_answers = u_ans_temp.copy() 
            u_ans = st.session_state.user_practice_answers 
            
            feedback = {}
            all_correct_practice = True 

            def validate_ip_string_practice_local(user_input, correct_value):
                is_correct = user_input.strip() == correct_value
                return is_correct, user_input.strip(), correct_value

            def validate_binary_string_practice_local(user_input, correct_value):
                user_input_clean = user_input.strip()
                user_formatted = get_binary_representation(user_input_clean) 
                
                is_correct_binary = True 
                user_display = user_input_clean

                if not user_input_clean: 
                    user_display = "Not Attempted"
                elif user_formatted in ["Invalid Format", "Invalid Binary Octet", "Conversion Error", "Invalid IP/Mask for Binary"]:
                    is_correct_binary = False
                    user_display = f"{user_input_clean} ({user_formatted})"
                else: 
                    is_correct_binary = user_formatted == correct_value
                    user_display = user_formatted
                
                return is_correct_binary, user_display, correct_value
            
            is_sm_correct, user_sm_val, correct_sm_val = validate_ip_string_practice_local(u_ans['subnet_mask'], q['correct_subnet_mask_str'])
            if not is_sm_correct: all_correct_practice = False
            feedback['subnet_mask'] = (is_sm_correct, user_sm_val, correct_sm_val)

            is_na_correct, user_na_val, correct_na_val = validate_ip_string_practice_local(u_ans['network_address'], q['correct_network_address_str'])
            if not is_na_correct: all_correct_practice = False
            feedback['network_address'] = (is_na_correct, user_na_val, correct_na_val)

            is_ba_correct, user_ba_val, correct_ba_val = validate_ip_string_practice_local(u_ans['broadcast_address'], q['correct_broadcast_address_str'])
            if not is_ba_correct: all_correct_practice = False
            feedback['broadcast_address'] = (is_ba_correct, user_ba_val, correct_ba_val)
            
            user_uhc = u_ans.get('usable_hosts_count') 
            is_uhc_correct = (user_uhc is not None) and (int(user_uhc) == q['correct_usable_hosts_count'])
            if not is_uhc_correct: all_correct_practice = False
            feedback['usable_hosts_count'] = (is_uhc_correct, str(user_uhc) if user_uhc is not None else "Not Answered", q['correct_usable_hosts_count'])

            is_fuip_correct, user_fuip_val, correct_fuip_val = validate_ip_string_practice_local(u_ans['first_usable_ip'], q['correct_first_usable_ip_str'])
            if not is_fuip_correct: all_correct_practice = False
            feedback['first_usable_ip'] = (is_fuip_correct, user_fuip_val, correct_fuip_val)
            
            is_luip_correct, user_luip_val, correct_luip_val = validate_ip_string_practice_local(u_ans['last_usable_ip'], q['correct_last_usable_ip_str'])
            if not is_luip_correct: all_correct_practice = False
            feedback['last_usable_ip'] = (is_luip_correct, user_luip_val, correct_luip_val)
            
            is_class_correct = u_ans['ip_class_type'] == q['correct_ip_class_type_str']
            if not is_class_correct: all_correct_practice = False
            feedback['ip_class_type'] = (is_class_correct, u_ans['ip_class_type'] or "Not Selected", q['correct_ip_class_type_str'])
            
            is_bip_correct, user_bip_val, correct_bip_val = validate_binary_string_practice_local(u_ans['binary_given_ip'], q['correct_binary_given_ip'])
            if not is_bip_correct: all_correct_practice = False
            feedback['binary_given_ip'] = (is_bip_correct, user_bip_val, correct_bip_val)

            is_bsm_correct, user_bsm_val, correct_bsm_val = validate_binary_string_practice_local(u_ans['binary_subnet_mask'], q['correct_binary_subnet_mask'])
            if not is_bsm_correct: all_correct_practice = False
            feedback['binary_subnet_mask'] = (is_bsm_correct, user_bsm_val, correct_bsm_val)

            st.session_state.practice_submission_feedback = feedback
            if all_correct_practice:
                st.balloons()
                st.success("🎉 All answers are correct! Well done!")
            else:
                st.error("Hmm, some answers need another look. Review the feedback below.")
            st.session_state.show_full_solution_practice = True


        if st.session_state.practice_submission_feedback:
            st.markdown("---") # Separator
            st.subheader("🔍 Feedback on Your Answers:")
            feedback_data = st.session_state.practice_submission_feedback
            for key, (correct, user_val, correct_val) in feedback_data.items():
                label = key.replace('_', ' ').title()
                status_icon = "✅" if correct else "❌"
                item_class = "correct" if correct else "incorrect"
                
                if user_val == "Not Attempted" and key.startswith("binary"):
                     st.markdown(f"<div class='feedback-item'><strong>{label}:</strong> Not Attempted. Correct was <code class='code-block'>{correct_val}</code>.</div>", unsafe_allow_html=True)
                elif user_val == "Not Answered" and key == "usable_hosts_count":
                    st.markdown(f"<div class='feedback-item {item_class}'><strong>{label}:</strong> {status_icon} Not Answered. Correct was <code class='code-block'>{correct_val}</code>.</div>", unsafe_allow_html=True)
                elif user_val == "Not Selected" and key == "ip_class_type":
                    st.markdown(f"<div class='feedback-item {item_class}'><strong>{label}:</strong> {status_icon} Not Selected. Correct was <code class='code-block'>{correct_val}</code>.</div>", unsafe_allow_html=True)
                elif correct:
                    st.markdown(f"<div class='feedback-item {item_class}'><strong>{label}:</strong> {status_icon} Your answer <code class='code-block'>{user_val}</code> is correct!</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='feedback-item {item_class}'><strong>{label}:</strong> {status_icon} Your answer is incorrect. Correct answer: <code class='code-block'>{correct_val}</code>.</div>", unsafe_allow_html=True)
        
        if st.session_state.show_full_solution_practice and q:
            st.markdown("---") # Separator
            st.subheader("✅ Full Solution & Details")

            usable_hosts_str_display = "N/A"
            if q['cidr'] == 32:
                usable_hosts_str_display = f"<span class='code-block'>{q['correct_first_usable_ip_str']}</span> (Host Route)"
            elif q['cidr'] == 31:
                usable_hosts_str_display = f"<span class='code-block'>{q['correct_first_usable_ip_str']}</span>, <span class='code-block'>{q['correct_last_usable_ip_str']}</span> (Point-to-Point Link)"
            elif q['correct_usable_hosts_count'] > 0:
                usable_hosts_str_display = f"<span class='code-block'>{q['correct_first_usable_ip_str']}</span> – <span class='code-block'>{q['correct_last_usable_ip_str']}</span>"
            else:
                usable_hosts_str_display = "None"

            # Removed solution-box div
            st.markdown("<div class='solution-section-header'><i class='fas fa-network-wired'></i> Network Overview</div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                    <div class='solution-item'>
                        <strong>Given IP / CIDR:</strong>
                        <span class='code-block prominent-code'>{q['given_ip_str']}/{q['cidr']}</span>
                    </div>
                    <div class='solution-item'>
                        <strong>Network Address:</strong>
                        <span class='code-block prominent-code'>{q['correct_network_address_str']}</span>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                    <div class='solution-item'>
                        <strong>Subnet Mask:</strong>
                        <span class='code-block prominent-code'>{q['correct_subnet_mask_str']}</span>
                    </div>
                    <div class='solution-item'>
                        <strong>Broadcast Address:</strong>
                        <span class='code-block prominent-code'>{q['correct_broadcast_address_str']}</span>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown(f"""
                <div class='solution-item full-width'>
                    <strong>IP Type/Class (Detailed): {get_ip_class_detailed(q['ip_interface_obj'].ip)}</strong>
                </div>
            """, unsafe_allow_html=True)
            # st.markdown("<hr class='solution-hr'>", unsafe_allow_html=True)

            st.markdown("<div class='solution-section-header'><i class='fas fa-desktop'></i> Host Information</div>", unsafe_allow_html=True)
            col3, col4 = st.columns(2)
            with col3:
                st.markdown(f"""
                    <div class='solution-item'>
                        <strong>Total Addresses in Subnet:</strong>
                        <span>{q['num_total_addresses']}</span>
                    </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                    <div class='solution-item'>
                        <strong>Number of Usable IPs:</strong>
                        <span>{q['correct_usable_hosts_count']}</span>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown(f"""
                <div class='solution-item'>
                    <strong>Usable IP Range:</strong>
                    {usable_hosts_str_display}
                </div>
            """, unsafe_allow_html=True)
            # st.markdown("<hr class='solution-hr'>", unsafe_allow_html=True)

            st.markdown("<div class='solution-section-header'><i class='fas fa-code'></i> Binary Representations</div>", unsafe_allow_html=True)
            st.markdown(f"""
                <div class='solution-item binary-item'>
                    <strong>Given IP:</strong>
                    <span class='code-block binary-code'>{q['correct_binary_given_ip']}</span>
                </div>
                <div class='solution-item binary-item'>
                    <strong>Subnet Mask:</strong>
                    <span class='code-block binary-code'>{q['correct_binary_subnet_mask']}</span>
                </div>
                <div class='solution-item binary-item'>
                    <strong>Network Address:</strong>
                    <span class='code-block binary-code'>{get_binary_representation(q['correct_network_address_str'])}</span>
                </div>
                <div class='solution-item binary-item'>
                    <strong>Broadcast Address:</strong>
                    <span class='code-block binary-code'>{get_binary_representation(q['correct_broadcast_address_str'])}</span>
                </div>
            """, unsafe_allow_html=True)
            
            with st.expander("📘 Step-by-Step Explanation", expanded=False):
                explanation_usable_hosts_str_for_exp = "N/A" 
                if q['cidr'] == 32: explanation_usable_hosts_str_for_exp = f"{q['correct_first_usable_ip_str']} (Host Route)"
                elif q['cidr'] == 31: explanation_usable_hosts_str_for_exp = f"{q['correct_first_usable_ip_str']}, {q['correct_last_usable_ip_str']} (Point-to-Point Link)"
                elif q['correct_usable_hosts_count'] > 0: explanation_usable_hosts_str_for_exp = f"{q['correct_first_usable_ip_str']} - {q['correct_last_usable_ip_str']}"
                else: explanation_usable_hosts_str_for_exp = "None"

                explanation_md = f"""
                **1. Given Information:**
                   - IP Address: `{q['given_ip_str']}`
                   - CIDR Prefix: `/{q['cidr']}` (This means the first `{q['cidr']}` bits of the mask are '1's).

                **2. Calculating the Subnet Mask:**
                   - A `/{q['cidr']}` prefix translates to a mask of: `{q['correct_subnet_mask_str']}`.
                   - Binary: `{q['correct_binary_subnet_mask']}`.

                **3. Determining the Network Address:**
                   - This is found by performing a bitwise AND operation between the Given IP and the Subnet Mask.
                   - Result: `{q['correct_network_address_str']}`.
                   - Binary: `{get_binary_representation(q['correct_network_address_str'])}`.

                **4. Determining the Broadcast Address:**
                   - This is the last address in the subnet. It's the Network Address with all host bits set to '1'.
                   - Result: `{q['correct_broadcast_address_str']}`.
                   - Binary: `{get_binary_representation(q['correct_broadcast_address_str'])}`.

                **5. Host Calculations:**
                   - Number of host bits (`h`): `32 - CIDR = 32 - {q['cidr']} = {32 - q['cidr']}`.
                   - Total addresses in this subnet: `2^h = 2^{32 - q['cidr']} = {q['num_total_addresses']}`.
                   - **Usable Host IPs:** `{q['correct_usable_hosts_count']}`.
                   - **Usable IP Range:** {explanation_usable_hosts_str_for_exp}.
                     - *Note on /31 (RFC 3021):* Both addresses are usable for point-to-point links.
                     - *Note on /32:* Represents a single host; that host IP is the only usable one.

                **6. IP Address Type/Class:**
                   - Based on its range, `{q['given_ip_str']}` is: `{get_ip_class_detailed(q['ip_interface_obj'].ip)}`.
                """
                st.markdown(explanation_md)


    # --- CHALLENGE MODE ---
    elif st.session_state.mode == "Challenge":
        st.header("🏆 Subnetting Challenge Mode 🏆")
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        if not st.session_state.challenge_active:
            st.info("Select a duration and press 'Start Challenge' to test your speed and accuracy!")
            duration_options_map = {"30 Seconds": 30, "1 Minute": 60, "2 Minutes": 120, "5 Minutes": 300}
            selected_duration_label = st.selectbox(
                "Challenge Duration:", 
                list(duration_options_map.keys()), 
                index=1 
            )
            st.session_state.challenge_duration_seconds = duration_options_map[selected_duration_label]

            if st.button("🚀 Start Challenge!", type="primary", use_container_width=True):
                st.session_state.challenge_active = True
                st.session_state.challenge_start_time = time.time()
                st.session_state.challenge_correct_score = 0
                st.session_state.challenge_incorrect_score = 0
                st.session_state.challenge_questions_attempted = 0
                if st.session_state.current_subnet_question is None : 
                    st.session_state.current_subnet_question = generate_random_ip_scenario()
                request_new_challenge_question() 
        
        else: # Challenge is active
            if q is None: 
                st.error("Error in challenge. Restarting challenge setup.")
                st.session_state.challenge_active = False 
                st.rerun()
                st.stop()

            time_now = time.time()
            time_elapsed = time_now - st.session_state.challenge_start_time
            time_remaining = st.session_state.challenge_duration_seconds - time_elapsed

            if time_remaining <= 0:
                st.session_state.challenge_active = False 
                st.balloons()
                st.success(f"🎉 Challenge Over! Time's Up! 🎉")
                st.markdown(f"""
                ### Your Final Score:
                - **Total Questions Attempted:** {st.session_state.challenge_questions_attempted}
                - <span class="score-display-correct">**Correct Answers:** {st.session_state.challenge_correct_score}</span>
                - <span class="score-display-incorrect">**Incorrect Answers:** {st.session_state.challenge_incorrect_score}</span>
                """, unsafe_allow_html=True)
                if st.button("Try Another Challenge?", use_container_width=True):
                    st.session_state.challenge_active = False 
                    st.rerun()
                st.stop()

            timer_str = f"{int(time_remaining // 60)}:{int(time_remaining % 60):02d}"
            st.markdown(
                f"<div class='challenge-stats-bar'>"
                f"<span class='timer-display'>⏳ {timer_str}</span>"
                f"<span>Attempted: {st.session_state.challenge_questions_attempted}</span>"
                f"<span class='score-display-correct'>✔️ Correct: {st.session_state.challenge_correct_score}</span>"
                f"<span class='score-display-incorrect'>❌ Incorrect: {st.session_state.challenge_incorrect_score}</span>"
                f"</div>",
                unsafe_allow_html=True
            )
            # Removed question-box div for challenge mode too
            st.markdown(f"#### Question {st.session_state.challenge_questions_attempted + 1}:")
            st.markdown(f"**Given IP Address / CIDR:** `{q['given_ip_str']}/{q['cidr']}`")
            st.markdown("*(Calculate all fields below)*")
            st.markdown("---") # Added separator

            challenge_form_key = f"challenge_answer_form_{st.session_state.challenge_questions_attempted}"
            
            with st.form(key=challenge_form_key):
                # Removed input-form-box div for challenge mode
                c_ans = {} 
                
                c_cols1 = st.columns(2)
                c_ans['subnet_mask'] = c_cols1[0].text_input("Subnet Mask", key=f"c_sm_{challenge_form_key}")
                c_ans['network_address'] = c_cols1[1].text_input("Network Address", key=f"c_na_{challenge_form_key}")
                
                c_cols2 = st.columns(2)
                c_ans['broadcast_address'] = c_cols2[0].text_input("Broadcast Address", key=f"c_ba_{challenge_form_key}")
                c_ans['usable_hosts_count'] = c_cols2[1].number_input("Usable Hosts Count", min_value=0, step=1, value=None, key=f"c_uhc_{challenge_form_key}")
                
                c_cols3 = st.columns(2)
                c_ans['first_usable_ip'] = c_cols3[0].text_input("First Usable IP", key=f"c_fuip_{challenge_form_key}")
                c_ans['last_usable_ip'] = c_cols3[1].text_input("Last Usable IP", key=f"c_luip_{challenge_form_key}")
                
                c_ans['ip_class_type'] = st.selectbox("IP Class/Type", options=[""] + IP_CLASS_OPTIONS, index=0, key=f"c_ict_{challenge_form_key}")
                
                st.markdown("---")
                st.markdown("##### Binary Rep (Optional but checked if filled):")
                c_cols4 = st.columns(2)
                c_ans['binary_given_ip'] = c_cols4[0].text_input("Binary Given IP", key=f"c_bip_{challenge_form_key}")
                c_ans['binary_subnet_mask'] = c_cols4[1].text_input("Binary Subnet Mask", key=f"c_bsm_{challenge_form_key}")
                
                challenge_submit_button = st.form_submit_button(label="➡️ Submit & Next Question")

            if challenge_submit_button:
                st.session_state.challenge_questions_attempted += 1
                is_current_q_fully_correct_challenge = True

                if not (c_ans['subnet_mask'].strip() == q['correct_subnet_mask_str']): is_current_q_fully_correct_challenge = False
                if not (c_ans['network_address'].strip() == q['correct_network_address_str']): is_current_q_fully_correct_challenge = False
                if not (c_ans['broadcast_address'].strip() == q['correct_broadcast_address_str']): is_current_q_fully_correct_challenge = False
                
                user_c_uhc = c_ans.get('usable_hosts_count')
                if not ((user_c_uhc is not None) and (int(user_c_uhc) == q['correct_usable_hosts_count'])): is_current_q_fully_correct_challenge = False
                
                if not (c_ans['first_usable_ip'].strip() == q['correct_first_usable_ip_str']): is_current_q_fully_correct_challenge = False
                if not (c_ans['last_usable_ip'].strip() == q['correct_last_usable_ip_str']): is_current_q_fully_correct_challenge = False
                if not (c_ans['ip_class_type'] == q['correct_ip_class_type_str']): is_current_q_fully_correct_challenge = False

                if c_ans['binary_given_ip'].strip(): 
                    user_bin_ip = get_binary_representation(c_ans['binary_given_ip'].strip())
                    if not (user_bin_ip == q['correct_binary_given_ip'] and user_bin_ip not in ["Invalid Format", "Invalid Binary Octet", "Conversion Error", "Invalid IP/Mask for Binary"]): 
                        is_current_q_fully_correct_challenge = False
                
                if c_ans['binary_subnet_mask'].strip():
                    user_bin_mask = get_binary_representation(c_ans['binary_subnet_mask'].strip())
                    if not (user_bin_mask == q['correct_binary_subnet_mask'] and user_bin_mask not in ["Invalid Format", "Invalid Binary Octet", "Conversion Error", "Invalid IP/Mask for Binary"]):
                        is_current_q_fully_correct_challenge = False

                if is_current_q_fully_correct_challenge:
                    st.session_state.challenge_correct_score += 1
                    st.toast("✅ Correct!", icon="🎉")
                else:
                    st.session_state.challenge_incorrect_score += 1
                    st.toast("❌ Incorrect. Next question!", icon="😥")
                
                request_new_challenge_question() 

            if st.session_state.challenge_active:
                time.sleep(0.8) 
                st.rerun()


# --- Module: Resource Hub ---
elif st.session_state.current_module == "Resource Hub":
    st.header("📚 Resource Hub")
    st.markdown("""
    Here are some valuable resources for deepening your understanding of IP addressing and networking:

    **Key RFCs (Request for Comments):**
    - [RFC 791: Internet Protocol (IPv4)](https://tools.ietf.org/html/rfc791)
    - [RFC 1918: Address Allocation for Private Internets](https://tools.ietf.org/html/rfc1918)
    - [RFC 3021: Using 31-Bit Prefixes on IPv4 Point-to-Point Links](https://tools.ietf.org/html/rfc3021)
    - [RFC 4632: Classless Inter-domain Routing (CIDR)](https://tools.ietf.org/html/rfc4632)
    - [RFC 5735: Special Use IPv4 Addresses](https://tools.ietf.org/html/rfc5735)

    **Online Subnetting Guides & Practice:**
    - [Cisco: IP Addressing and Subnetting for New Users](https://www.cisco.com/c/en/us/support/docs/ip/routing-information-protocol-rip/13788-3.html)
    - [Practical Networking](https://www.practicalnetworking.net/)
    """)

# --- Footer ---
st.markdown("<hr style='margin: 2em 0;'>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="footer">
        🛠️ Created with Streamlit & ❤️ by Shakti Swaroop Sahu (https://github.com/prosws2210)
        <br>
        <i>Master the art of IP networking!</i>
    </div>
    """, unsafe_allow_html=True
)