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
# st.write("DEBUG: Page configured.")

# --- Font Awesome CDN (for icons in the redesigned solution) ---
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">', unsafe_allow_html=True)
# st.write("DEBUG: Font Awesome CDN linked.")

# --- Session State Initialization ---
# st.write("DEBUG: Initializing session state...")
# General
if 'mode' not in st.session_state:
    st.session_state.mode = "Practice"  # Practice | Challenge
    # st.write("DEBUG: Session state 'mode' initialized to Practice.")
if 'current_module' not in st.session_state:
    st.session_state.current_module = "IPv4 Subnetting Practice"
    # st.write("DEBUG: Session state 'current_module' initialized to IPv4 Subnetting Practice.")

# For Subnetting Practice Module (Practice & Challenge)
if 'current_subnet_question' not in st.session_state:
    st.session_state.current_subnet_question = None
    # st.write("DEBUG: Session state 'current_subnet_question' initialized to None.")
if 'user_practice_answers' not in st.session_state: # Store user's practice answers
    st.session_state.user_practice_answers = {}
    # st.write("DEBUG: Session state 'user_practice_answers' initialized to {}.")
if 'practice_submission_feedback' not in st.session_state: # Store feedback after practice submission
    st.session_state.practice_submission_feedback = None
    # st.write("DEBUG: Session state 'practice_submission_feedback' initialized to None.")
if 'show_full_solution_practice' not in st.session_state:
    st.session_state.show_full_solution_practice = False
    # st.write("DEBUG: Session state 'show_full_solution_practice' initialized to False.")
if 'practice_questions_generated' not in st.session_state:
    st.session_state.practice_questions_generated = 0
    # st.write("DEBUG: Session state 'practice_questions_generated' initialized to 0.")


# For Challenge Mode Specifics
if 'challenge_active' not in st.session_state:
    st.session_state.challenge_active = False
    # st.write("DEBUG: Session state 'challenge_active' initialized to False.")
if 'challenge_start_time' not in st.session_state:
    st.session_state.challenge_start_time = 0.0
    # st.write("DEBUG: Session state 'challenge_start_time' initialized to 0.0.")
if 'challenge_duration_seconds' not in st.session_state:
    st.session_state.challenge_duration_seconds = 60 # Default 1 minute
    # st.write("DEBUG: Session state 'challenge_duration_seconds' initialized to 60.")
if 'challenge_timer_display' not in st.session_state: # Placeholder for timer display
    st.session_state.challenge_timer_display = None
    # st.write("DEBUG: Session state 'challenge_timer_display' initialized to None.")
if 'challenge_correct_score' not in st.session_state:
    st.session_state.challenge_correct_score = 0
    # st.write("DEBUG: Session state 'challenge_correct_score' initialized to 0.")
if 'challenge_incorrect_score' not in st.session_state:
    st.session_state.challenge_incorrect_score = 0
    # st.write("DEBUG: Session state 'challenge_incorrect_score' initialized to 0.")
if 'challenge_questions_attempted' not in st.session_state:
    st.session_state.challenge_questions_attempted = 0
    # st.write("DEBUG: Session state 'challenge_questions_attempted' initialized to 0.")
# st.write("DEBUG: Session state initialization complete.")

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
# st.write("DEBUG: Dark theme CSS applied.")

# --- Helper Functions ---
IP_CLASS_OPTIONS = [
    "Public Class A", "Public Class B", "Public Class C",
    "Private Class A", "Private Class B", "Private Class C",
    "D (Multicast)", "E (Experimental)", "Loopback", "Link-Local (APIPA)",
    "Unspecified (0.0.0.0)", "Limited Broadcast (255.255.255.255)", "Special/Other"
]
# st.write("DEBUG: IP_CLASS_OPTIONS defined.")

def get_ip_class_simple(ip_address_obj):
    # st.write(f"DEBUG: get_ip_class_simple called with ip_address_obj: {ip_address_obj}")
    try:
        first_octet = ip_address_obj.packed[0]
        # st.write(f"DEBUG: get_ip_class_simple - first_octet: {first_octet}")
        if ip_address_obj.is_multicast: return "D (Multicast)"
        if ip_address_obj.is_loopback: return "Loopback"
        if ip_address_obj.is_link_local: return "Link-Local (APIPA)"
        if str(ip_address_obj) == "0.0.0.0": return "Unspecified (0.0.0.0)"
        if str(ip_address_obj) == "255.255.255.255": return "Limited Broadcast (255.255.255.255)"

        is_private = ip_address_obj.is_private
        # st.write(f"DEBUG: get_ip_class_simple - is_private: {is_private}")
        cls_letter = ""
        if 1 <= first_octet <= 126: cls_letter = "A"
        elif 128 <= first_octet <= 191: cls_letter = "B"
        elif 192 <= first_octet <= 223: cls_letter = "C"
        elif 240 <= first_octet <= 254: return "E (Experimental)"
        # st.write(f"DEBUG: get_ip_class_simple - cls_letter (pre-private check): {cls_letter}")

        if is_private:
            # st.write(f"DEBUG: get_ip_class_simple - Checking private ranges for class {cls_letter}")
            if cls_letter == "A" and ip_address_obj.packed[0] == 10: return "Private Class A"
            if cls_letter == "B" and ip_address_obj.packed[0] == 172 and 16 <= ip_address_obj.packed[1] <= 31 : return "Private Class B"
            if cls_letter == "C" and ip_address_obj.packed[0] == 192 and ip_address_obj.packed[1] == 168 : return "Private Class C"
        elif cls_letter:
            return f"Public Class {cls_letter}"
        # st.write(f"DEBUG: get_ip_class_simple - Falling back to Special/Other for {ip_address_obj}")
        return "Special/Other"
    except Exception as e:
        st.write(f"ERROR: get_ip_class_simple failed for {ip_address_obj}: {e}")
        return "Error determining class (simple)"

def get_ip_class_detailed(ip_address_obj):
    # st.write(f"DEBUG: get_ip_class_detailed called with ip_address_obj: {ip_address_obj}")
    try:
        first_octet = ip_address_obj.packed[0]
        # st.write(f"DEBUG: get_ip_class_detailed - first_octet: {first_octet}")
        if ip_address_obj.is_multicast: return "D (Multicast)"
        if ip_address_obj.is_loopback: return "Loopback Address (e.g., 127.0.0.1)"
        if ip_address_obj.is_link_local: return "Link-Local Address (APIPA, 169.254.0.0/16)"
        if ip_address_obj.is_private:
            cls_simple = ""
            if 10 == first_octet: cls_simple = "A"
            elif 172 == first_octet and 16 <= ip_address_obj.packed[1] <= 31: cls_simple = "B"
            elif 192 == first_octet and 168 == ip_address_obj.packed[1]: cls_simple = "C"
            # st.write(f"DEBUG: get_ip_class_detailed - Private, nominal class {cls_simple}")
            return f"Private Use Address (RFC 1918, nominally Class {cls_simple} block)"
        if ip_address_obj.is_reserved: return "Reserved (IETF Protocol)"
        if ip_address_obj.is_global:
            # st.write(f"DEBUG: get_ip_class_detailed - Global address, checking ranges.")
            if 1 <= first_octet <= 126: return "Public (Historically Class A range)"
            if 128 <= first_octet <= 191: return "Public (Historically Class B range)"
            if 192 <= first_octet <= 223: return "Public (Historically Class C range)"
        if 240 <= first_octet <= 255 and str(ip_address_obj) != "255.255.255.255": return "E (Experimental / Future Use)"
        if str(ip_address_obj) == "0.0.0.0": return "Unspecified Address (0.0.0.0)"
        if str(ip_address_obj) == "255.255.255.255": return "Limited Broadcast Address (255.255.255.255)"
        # st.write(f"DEBUG: get_ip_class_detailed - Falling back to Special Purpose or Unknown for {ip_address_obj}")
        return "Special Purpose or Unknown"
    except Exception as e:
        st.write(f"ERROR: get_ip_class_detailed failed for {ip_address_obj}: {e}")
        return "Error determining class (detailed)"


def get_binary_representation(ip_or_mask_str):
    # st.write(f"DEBUG: get_binary_representation called with: '{ip_or_mask_str}'")
    try:
        ip_or_mask_str = ip_or_mask_str.replace(" ", "")
        if '.' in ip_or_mask_str:
            parts = ip_or_mask_str.split('.')
            if len(parts) != 4:
                # st.write("DEBUG: get_binary_representation - Invalid Format (not 4 parts)")
                return "Invalid Format"
            octets = []
            for part in parts:
                if not (len(part) == 8 and all(c in '01' for c in part)):
                    # This might be a decimal IP, try converting it
                    try:
                        ipaddress.ip_address(ip_or_mask_str) # Validate if it's a decimal IP
                        st.write(f"DEBUG: get_binary_representation - Input '{ip_or_mask_str}' is decimal, converting.")
                        return ".".join(format(int(octet), '08b') for octet in ip_or_mask_str.split("."))
                    except ValueError:
                        st.write(f"DEBUG: get_binary_representation - Invalid Binary Octet or invalid decimal IP: {part}")
                        return "Invalid Binary Octet"
                octets.append(part)
            return ".".join(octets)
        elif all(c in '01' for c in ip_or_mask_str) and len(ip_or_mask_str) == 32:
            st.write("DEBUG: get_binary_representation - Input is 32-bit binary string.")
            return f"{ip_or_mask_str[0:8]}.{ip_or_mask_str[8:16]}.{ip_or_mask_str[16:24]}.{ip_or_mask_str[24:32]}"
        else:
            # Assume it's a standard IP string to be converted
            ipaddress.ip_address(ip_or_mask_str) # Validate
            st.write(f"DEBUG: get_binary_representation - Input '{ip_or_mask_str}' is decimal, converting.")
            return ".".join(format(int(octet), '08b') for octet in ip_or_mask_str.split("."))
    except ValueError as ve:
        st.write(f"DEBUG: get_binary_representation - ValueError: {ve} for input '{ip_or_mask_str}'")
        return "Invalid IP/Mask for Binary"
    except Exception as e:
        st.write(f"DEBUG: get_binary_representation - General Exception: {e} for input '{ip_or_mask_str}'")
        return "Conversion Error"

def generate_random_ip_scenario():
    st.write("DEBUG: generate_random_ip_scenario called.")
    try:
        scenario_type_weights = ["standard_subnet"]*6 + ["edge_cidr"]*3 + ["specific_ip"]*1
        scenario_type = random.choice(scenario_type_weights)
        st.write(f"DEBUG: generate_random_ip_scenario - scenario_type: {scenario_type}")

        ip_str = ""
        cidr = 0

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
            st.write(f"DEBUG: generate_random_ip_scenario - specific_ip: {ip_str}/{cidr}")
        else:
            first_octet = random.randint(1, 223)
            if first_octet == 169 and random.randint(0,255) == 254: # Avoid 169.254.x.x directly
                 first_octet = random.randint(1,168) # Regenerate if it falls into APIPA range for general cases

            ip_str = f"{first_octet}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}" # Avoid .0 or .255 as host part initially

            if scenario_type == "edge_cidr":
                possible_cidrs = [0, 1, 2, 3, 4, 5, 6, 7, 30, 31, 32]
                uncommon_cidrs = [9,10,11,13,14,15,17,18,19,21] # Less common but valid
                cidr = random.choice(possible_cidrs + uncommon_cidrs + [random.randint(20,29)])
                st.write(f"DEBUG: generate_random_ip_scenario - edge_cidr chosen: /{cidr} for IP base {ip_str}")
            else: # standard_subnet
                common_cidrs = list(range(8, 31)) # /8 to /30
                weights = [1]*len(common_cidrs)
                for i, c_val in enumerate(common_cidrs):
                    if c_val in [8,16,24]: weights[i] = 4 # Classful more common
                    if c_val in [25,26,27,28,29,30]: weights[i] = 2 # Common small subnets
                cidr = random.choices(common_cidrs, weights=weights, k=1)[0]
                st.write(f"DEBUG: generate_random_ip_scenario - standard_subnet cidr chosen: /{cidr} for IP base {ip_str}")

        st.write(f"DEBUG: generate_random_ip_scenario - Attempting to create interface for {ip_str}/{cidr}")
        ip_interface = None
        network_obj = None

        try:
            # Handle cases where generated IP might be network or broadcast for the given CIDR
            if cidr == 0 and ip_str != "0.0.0.0":
                st.write(f"DEBUG: generate_random_ip_scenario - CIDR is 0, IP is not 0.0.0.0. Forcing IP to 0.0.0.0 for /0.")
                ip_interface = ipaddress.IPv4Interface(f"0.0.0.0/{cidr}")
            elif cidr < 31: # For /31 and /32, network/broadcast can be valid host IPs
                temp_net_for_check = ipaddress.IPv4Network(f"{ip_str}/{cidr}", strict=False)
                if ip_str == str(temp_net_for_check.network_address) or ip_str == str(temp_net_for_check.broadcast_address):
                    st.write(f"DEBUG: generate_random_ip_scenario - IP {ip_str} is network/broadcast for /{cidr}. Adjusting.")
                    hosts_in_temp_net = list(temp_net_for_check.hosts())
                    if hosts_in_temp_net:
                        ip_str = str(random.choice(hosts_in_temp_net))
                        st.write(f"DEBUG: generate_random_ip_scenario - Adjusted IP to a host: {ip_str}")
                    # If no hosts (e.g. /31, /32 where net/bcast are the hosts), ip_str might remain as is, which is fine.
            ip_interface = ipaddress.IPv4Interface(f"{ip_str}/{cidr}")
            network_obj = ip_interface.network
            st.write(f"DEBUG: generate_random_ip_scenario - Successfully created interface: {ip_interface}, network: {network_obj}")

        except ValueError as e_ip:
            st.write(f"WARN: generate_random_ip_scenario - ValueError creating interface for {ip_str}/{cidr}: {e_ip}. Retrying with base network.")
            try:
                # Fallback: Create a network with the CIDR and pick an IP from it
                base_network = ipaddress.IPv4Network(f"0.0.0.0/{cidr}", strict=False) # Use 0.0.0.0 as placeholder
                if base_network.num_addresses > 2 :
                    hosts = list(base_network.hosts())
                    if hosts: ip_str = str(random.choice(hosts))
                    else: ip_str = str(base_network.network_address) # Should not happen if num_addresses > 2
                elif base_network.num_addresses == 2: # /31 case
                    ip_str = str(base_network.network_address) # Pick one of the two
                else: # /32 or /0
                    ip_str = str(base_network.network_address)

                ip_interface = ipaddress.IPv4Interface(f"{ip_str}/{cidr}")
                network_obj = ip_interface.network
                st.write(f"DEBUG: generate_random_ip_scenario - Fallback successful. New IP: {ip_str}, Interface: {ip_interface}, Network: {network_obj}")
            except ValueError as e_ip_fallback:
                st.write(f"ERROR: generate_random_ip_scenario - Critical ValueError on fallback for /{cidr}: {e_ip_fallback}. RECURSING.")
                return generate_random_ip_scenario() # Recursive call if still fails
        except Exception as e_gen:
            st.write(f"ERROR: generate_random_ip_scenario - Unexpected exception during IP/Network object creation: {e_gen}. RECURSING.")
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
            usable_hosts_count = 2 # Both addresses are usable
            first_usable_ip_str = str(network_obj.network_address)
            last_usable_ip_str = str(network_obj.broadcast_address) # In /31, these are the two usable IPs
        elif num_total_addresses > 2:
            usable_hosts_count = num_total_addresses - 2
            hosts_list = list(network_obj.hosts())
            if hosts_list: # Ensure there are hosts
                first_usable_ip_str = str(hosts_list[0])
                last_usable_ip_str = str(hosts_list[-1])
            else: # Should not happen if num_total_addresses > 2
                st.write(f"WARN: generate_random_ip_scenario - num_total_addresses > 2 ({num_total_addresses}) but no hosts found for {network_obj}. This is unexpected.")
                usable_hosts_count = 0 # Safety
        elif num_total_addresses == 2 and cidr != 31: # e.g. /30 has 4 total, 2 usable. /31 is handled above.
             usable_hosts_count = 0 # This case should be covered by num_total_addresses > 2, but for safety.
        elif num_total_addresses == 1 and cidr != 32: # e.g. /0 if it was miscalculated, /32 handled above
            usable_hosts_count = 0

        st.write(f"DEBUG: generate_random_ip_scenario - Usable hosts calculation: count={usable_hosts_count}, first={first_usable_ip_str}, last={last_usable_ip_str}")

        question_data = {
            "given_ip_str": str(ip_interface.ip), # Use the IP from the interface, as ip_str might have been adjusted
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
            "correct_binary_given_ip": get_binary_representation(str(ip_interface.ip)),
            "correct_binary_subnet_mask": get_binary_representation(str(network_obj.netmask)),
            "num_total_addresses": num_total_addresses,
        }
        st.write(f"DEBUG: generate_random_ip_scenario - Returning question data: {question_data['given_ip_str']}/{question_data['cidr']}")
        return question_data
    except Exception as e:
        st.write(f"ERROR: generate_random_ip_scenario - Outer exception: {e}. RECURSING to avoid app crash.")
        # Potentially log more details about the state before recursing
        return generate_random_ip_scenario()


def reset_practice_form_state():
    st.write("DEBUG: reset_practice_form_state called.")
    st.session_state.user_practice_answers = {}
    st.session_state.practice_submission_feedback = None
    st.session_state.show_full_solution_practice = False
    st.write("DEBUG: reset_practice_form_state - state reset.")

def request_new_practice_question():
    st.write("DEBUG: request_new_practice_question called.")
    try:
        st.session_state.current_subnet_question = generate_random_ip_scenario()
        reset_practice_form_state()
        st.session_state.practice_questions_generated += 1
        st.write(f"DEBUG: request_new_practice_question - New question generated. Count: {st.session_state.practice_questions_generated}")
    except Exception as e:
        st.write(f"ERROR: request_new_practice_question - Failed to generate new practice question: {e}")
        st.error(f"An error occurred while generating a new question: {e}. Please try again.")
        # Potentially reset current_subnet_question to None or handle differently
    st.rerun()

def request_new_challenge_question():
    st.write("DEBUG: request_new_challenge_question called.")
    try:
        st.session_state.current_subnet_question = generate_random_ip_scenario()
        st.write("DEBUG: request_new_challenge_question - New challenge question generated.")
    except Exception as e:
        st.write(f"ERROR: request_new_challenge_question - Failed to generate new challenge question: {e}")
        st.error(f"An error occurred while generating a new challenge question: {e}. The challenge might need to be restarted.")
        st.session_state.challenge_active = False # Potentially stop the challenge
    st.rerun()


# --- UI Rendering ---
st.write("DEBUG: Starting UI Rendering.")
# Sidebar
with st.sidebar:
    st.write("DEBUG: Rendering Sidebar.")
    st.markdown("<h1>📡 Networking Toolkit</h1>", unsafe_allow_html=True)

    selected_mode = st.radio(
        "🎯 Mode Select:",
        ["Practice", "Challenge"],
        index=["Practice", "Challenge"].index(st.session_state.mode),
        key="mode_select_radio"
    )
    if selected_mode != st.session_state.mode:
        st.write(f"DEBUG: Mode changed from {st.session_state.mode} to {selected_mode}. Rerunning.")
        st.session_state.mode = selected_mode
        # Reset challenge state if switching out of challenge mode or to a different mode
        if st.session_state.mode != "Challenge" and st.session_state.challenge_active:
            st.session_state.challenge_active = False
            st.write("DEBUG: Switched out of active Challenge mode. Resetting challenge_active.")
        # If switching to Practice, and no question, generate one
        if st.session_state.mode == "Practice" and st.session_state.current_subnet_question is None:
            st.write("DEBUG: Switched to Practice, no current question. Requesting new one.")
            # Can't call request_new_practice_question here directly due to rerun, set flag or handle in main
    
    st.write(f"DEBUG: Sidebar - Current mode: {st.session_state.mode}")
    st.markdown("---")

    st.subheader("📚 Learning Modules")
    module_options = [ "IPv4 Subnetting Practice", "Resource Hub" ]
    selected_module = st.radio(
        "Choose a module:", module_options, index=module_options.index(st.session_state.current_module)
    )
    if selected_module != st.session_state.current_module:
        st.write(f"DEBUG: Module changed from {st.session_state.current_module} to {selected_module}. Rerunning.")
        st.session_state.current_module = selected_module
        # If switching to Practice and no question, handle as above or in main logic
        if st.session_state.current_module == "IPv4 Subnetting Practice" and st.session_state.mode == "Practice" and st.session_state.current_subnet_question is None:
             st.write("DEBUG: Switched to Practice module, no current question. Will be handled by main logic.")


    st.write(f"DEBUG: Sidebar - Current module: {st.session_state.current_module}")
    st.markdown("---")
    if st.session_state.mode == "Practice":
        st.caption(f"Practice Questions This Session: {st.session_state.practice_questions_generated}")
    elif st.session_state.mode == "Challenge" and st.session_state.challenge_active:
        st.caption(f"Attempted: {st.session_state.challenge_questions_attempted}")
        st.caption(f"Correct: {st.session_state.challenge_correct_score} | Incorrect: {st.session_state.challenge_incorrect_score}")
    st.write("DEBUG: Sidebar rendering complete.")

# Main content area
st.title("🌐 IP Addressing & Networking Mastery")
st.write(f"DEBUG: Main content - Mode: {st.session_state.mode}, Module: {st.session_state.current_module}")

# --- Module: IPv4 Subnetting Practice ---
if st.session_state.current_module == "IPv4 Subnetting Practice":
    st.write("DEBUG: IPv4 Subnetting Practice module selected.")

    if st.session_state.current_subnet_question is None:
        st.write("DEBUG: current_subnet_question is None. Attempting to generate/request.")
        if st.session_state.mode == "Practice":
            st.write("DEBUG: Mode is Practice, calling request_new_practice_question.")
            # This will call rerun, so subsequent code in this block might not run in this pass
            request_new_practice_question()
        elif st.session_state.mode == "Challenge" and not st.session_state.challenge_active:
            st.write("DEBUG: Mode is Challenge (inactive), generating initial question.")
            try:
                st.session_state.current_subnet_question = generate_random_ip_scenario()
            except Exception as e_gen_init_chal:
                st.write(f"ERROR: Failed to generate initial challenge question: {e_gen_init_chal}")
                st.error("Could not generate a question for the challenge setup.")
                # No rerun here, allow UI to show error
        elif st.session_state.mode == "Challenge" and st.session_state.challenge_active:
            st.write("DEBUG: Mode is Challenge (active), calling request_new_challenge_question.")
            # This will call rerun
            request_new_challenge_question()

    q = st.session_state.current_subnet_question
    st.write(f"DEBUG: Current question 'q' is {'set' if q else 'None'}.")

    if q is None and st.session_state.mode == "Challenge" and not st.session_state.challenge_active:
        # This case might occur if the initial generation in the block above failed without a rerun
        st.write("DEBUG: q is None in inactive Challenge mode post-initial check. Attempting generation again.")
        try:
            st.session_state.current_subnet_question = generate_random_ip_scenario()
            q = st.session_state.current_subnet_question
            st.write(f"DEBUG: Re-attempted generation for inactive challenge. q is now {'set' if q else 'None'}.")
            if q is None: st.warning("DEBUG: Failed to generate question for inactive challenge even on re-attempt.")
        except Exception as e_gen_init_chal_retry:
            st.write(f"ERROR: Failed to generate initial challenge question (retry): {e_gen_init_chal_retry}")
            st.error("Could not generate a question for the challenge setup (retry).")


    # --- PRACTICE MODE ---
    if st.session_state.mode == "Practice":
        st.write("DEBUG: Entering Practice Mode UI rendering.")
        st.header("🧠 IPv4 Subnetting Practice")
        st.markdown("Test your subnetting skills! Enter your answers and check your work.")

        if st.button("🔄 Generate New Question", type="primary", use_container_width=True, key="practice_new_q_button"):
            st.write("DEBUG: 'Generate New Question' (Practice) button clicked.")
            request_new_practice_question() # This will rerun

        if q is None:
            st.write("ERROR: Practice mode - q is None. Stopping rendering for this section.")
            st.error("Error generating question. Please try clicking 'Generate New Question'.")
            st.stop() # Stop further rendering in this specific path if q is None

        st.write(f"DEBUG: Practice Mode - Question {st.session_state.practice_questions_generated}: IP {q['given_ip_str']}/{q['cidr']}")
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
        st.markdown("---")

        practice_form_key = f"practice_answer_form_{st.session_state.practice_questions_generated}"
        st.write(f"DEBUG: Practice form key: {practice_form_key}")

        with st.form(key=practice_form_key):
            st.write("DEBUG: Practice form rendering.")
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
            st.write("DEBUG: Practice form rendered.")

        if practice_submit_button:
            st.write("DEBUG: Practice form submitted.")
            st.write(f"DEBUG: User practice answers (raw from form): {u_ans_temp}")
            st.session_state.user_practice_answers = u_ans_temp.copy()
            u_ans = st.session_state.user_practice_answers
            st.write(f"DEBUG: User practice answers (copied to session state): {u_ans}")

            feedback = {}
            all_correct_practice = True

            def validate_ip_string_practice_local(user_input, correct_value):
                st.write(f"DEBUG: validate_ip_string_practice_local - User: '{user_input}', Correct: '{correct_value}'")
                is_correct = user_input.strip() == correct_value
                return is_correct, user_input.strip(), correct_value

            def validate_binary_string_practice_local(user_input, correct_value):
                st.write(f"DEBUG: validate_binary_string_practice_local - User: '{user_input}', Correct: '{correct_value}'")
                user_input_clean = user_input.strip()
                user_formatted = get_binary_representation(user_input_clean) # Uses the helper
                st.write(f"DEBUG: validate_binary_string_practice_local - User_formatted: '{user_formatted}'")

                is_correct_binary = True
                user_display = user_input_clean

                if not user_input_clean:
                    user_display = "Not Attempted"
                    is_correct_binary = False # Or handle as per requirements for blank optional fields
                elif user_formatted in ["Invalid Format", "Invalid Binary Octet", "Conversion Error", "Invalid IP/Mask for Binary"]:
                    is_correct_binary = False
                    user_display = f"{user_input_clean} ({user_formatted})"
                else:
                    is_correct_binary = user_formatted == correct_value
                    user_display = user_formatted

                return is_correct_binary, user_display, correct_value

            try:
                is_sm_correct, user_sm_val, correct_sm_val = validate_ip_string_practice_local(u_ans.get('subnet_mask',''), q['correct_subnet_mask_str'])
                if not is_sm_correct: all_correct_practice = False
                feedback['subnet_mask'] = (is_sm_correct, user_sm_val, correct_sm_val)

                is_na_correct, user_na_val, correct_na_val = validate_ip_string_practice_local(u_ans.get('network_address',''), q['correct_network_address_str'])
                if not is_na_correct: all_correct_practice = False
                feedback['network_address'] = (is_na_correct, user_na_val, correct_na_val)

                is_ba_correct, user_ba_val, correct_ba_val = validate_ip_string_practice_local(u_ans.get('broadcast_address',''), q['correct_broadcast_address_str'])
                if not is_ba_correct: all_correct_practice = False
                feedback['broadcast_address'] = (is_ba_correct, user_ba_val, correct_ba_val)

                user_uhc = u_ans.get('usable_hosts_count')
                is_uhc_correct = (user_uhc is not None) and (int(user_uhc) == q['correct_usable_hosts_count'])
                if not is_uhc_correct: all_correct_practice = False
                feedback['usable_hosts_count'] = (is_uhc_correct, str(user_uhc) if user_uhc is not None else "Not Answered", q['correct_usable_hosts_count'])

                is_fuip_correct, user_fuip_val, correct_fuip_val = validate_ip_string_practice_local(u_ans.get('first_usable_ip',''), q['correct_first_usable_ip_str'])
                if not is_fuip_correct: all_correct_practice = False
                feedback['first_usable_ip'] = (is_fuip_correct, user_fuip_val, correct_fuip_val)

                is_luip_correct, user_luip_val, correct_luip_val = validate_ip_string_practice_local(u_ans.get('last_usable_ip',''), q['correct_last_usable_ip_str'])
                if not is_luip_correct: all_correct_practice = False
                feedback['last_usable_ip'] = (is_luip_correct, user_luip_val, correct_luip_val)

                is_class_correct = u_ans.get('ip_class_type','') == q['correct_ip_class_type_str']
                if not is_class_correct: all_correct_practice = False
                feedback['ip_class_type'] = (is_class_correct, u_ans.get('ip_class_type','') or "Not Selected", q['correct_ip_class_type_str'])

                is_bip_correct, user_bip_val, correct_bip_val = validate_binary_string_practice_local(u_ans.get('binary_given_ip',''), q['correct_binary_given_ip'])
                if not is_bip_correct: all_correct_practice = False
                feedback['binary_given_ip'] = (is_bip_correct, user_bip_val, correct_bip_val)

                is_bsm_correct, user_bsm_val, correct_bsm_val = validate_binary_string_practice_local(u_ans.get('binary_subnet_mask',''), q['correct_binary_subnet_mask'])
                if not is_bsm_correct: all_correct_practice = False
                feedback['binary_subnet_mask'] = (is_bsm_correct, user_bsm_val, correct_bsm_val)

                st.session_state.practice_submission_feedback = feedback
                st.write(f"DEBUG: Practice feedback generated: {feedback}")
                st.write(f"DEBUG: Practice all_correct_practice: {all_correct_practice}")

                if all_correct_practice:
                    st.balloons()
                    st.success("🎉 All answers are correct! Well done!")
                else:
                    st.error("Hmm, some answers need another look. Review the feedback below.")
                st.session_state.show_full_solution_practice = True
                st.write("DEBUG: show_full_solution_practice set to True.")

            except Exception as e_val:
                st.write(f"ERROR: Exception during practice answer validation: {e_val}")
                st.error(f"An error occurred while checking your answers: {e_val}. Please ensure all inputs are in the correct format.")
                st.session_state.practice_submission_feedback = None # Reset feedback on error
                st.session_state.show_full_solution_practice = False


        if st.session_state.practice_submission_feedback:
            st.write("DEBUG: Displaying practice submission feedback.")
            st.markdown("---")
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
            st.write("DEBUG: Displaying full solution for practice question.")
            st.markdown("---")
            st.subheader("✅ Full Solution & Details")

            usable_hosts_str_display = "N/A"
            try:
                if q['cidr'] == 32:
                    usable_hosts_str_display = f"<span class='code-block'>{q['correct_first_usable_ip_str']}</span> (Host Route)"
                elif q['cidr'] == 31:
                    usable_hosts_str_display = f"<span class='code-block'>{q['correct_first_usable_ip_str']}</span>, <span class='code-block'>{q['correct_last_usable_ip_str']}</span> (Point-to-Point Link)"
                elif q['correct_usable_hosts_count'] > 0:
                    usable_hosts_str_display = f"<span class='code-block'>{q['correct_first_usable_ip_str']}</span> – <span class='code-block'>{q['correct_last_usable_ip_str']}</span>"
                else:
                    usable_hosts_str_display = "None"
            except KeyError as ke:
                st.write(f"ERROR: KeyError in solution display (usable_hosts_str_display): {ke}. Question data 'q' might be incomplete: {q}")
                usable_hosts_str_display = "Error displaying range"
            except Exception as e_sol_disp:
                st.write(f"ERROR: Exception in solution display (usable_hosts_str_display): {e_sol_disp}")
                usable_hosts_str_display = "Error displaying range"


            # Removed solution-box div
            st.markdown("<div class='solution-section-header'><i class='fas fa-network-wired'></i> Network Overview</div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            try:
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
            except KeyError as ke:
                st.write(f"ERROR: KeyError in solution display (Network Overview): {ke}. Question data 'q' might be incomplete: {q}")
                st.error("Error displaying some solution details.")
            except Exception as e_sol_net:
                st.write(f"ERROR: Exception in solution display (Network Overview): {e_sol_net}")
                st.error("Error displaying some solution details.")


            st.markdown("<div class='solution-section-header'><i class='fas fa-desktop'></i> Host Information</div>", unsafe_allow_html=True)
            col3, col4 = st.columns(2)
            try:
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
            except KeyError as ke:
                st.write(f"ERROR: KeyError in solution display (Host Information): {ke}. Question data 'q' might be incomplete: {q}")
                st.error("Error displaying some host information details.")
            except Exception as e_sol_host:
                st.write(f"ERROR: Exception in solution display (Host Information): {e_sol_host}")
                st.error("Error displaying some host information details.")


            st.markdown("<div class='solution-section-header'><i class='fas fa-code'></i> Binary Representations</div>", unsafe_allow_html=True)
            try:
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
            except KeyError as ke:
                st.write(f"ERROR: KeyError in solution display (Binary Representations): {ke}. Question data 'q' might be incomplete: {q}")
                st.error("Error displaying some binary representation details.")
            except Exception as e_sol_bin:
                st.write(f"ERROR: Exception in solution display (Binary Representations): {e_sol_bin}")
                st.error("Error displaying some binary representation details.")

            with st.expander("📘 Step-by-Step Explanation", expanded=False):
                st.write("DEBUG: Expanding Step-by-Step Explanation.")
                try:
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
                except KeyError as ke:
                    st.write(f"ERROR: KeyError in explanation generation: {ke}. Question data 'q' might be incomplete: {q}")
                    st.error("Could not generate parts of the explanation.")
                except Exception as e_exp:
                    st.write(f"ERROR: Exception in explanation generation: {e_exp}")
                    st.error("An error occurred while generating the explanation.")
        st.write("DEBUG: Practice Mode UI rendering complete.")


    # --- CHALLENGE MODE ---
    elif st.session_state.mode == "Challenge":
        st.write("DEBUG: Entering Challenge Mode UI rendering.")
        st.header("🏆 Subnetting Challenge Mode 🏆")
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        if not st.session_state.challenge_active:
            st.write("DEBUG: Challenge is not active. Displaying setup options.")
            st.info("Select a duration and press 'Start Challenge' to test your speed and accuracy!")
            duration_options_map = {"30 Seconds": 30, "1 Minute": 60, "2 Minutes": 120, "5 Minutes": 300}
            selected_duration_label = st.selectbox(
                "Challenge Duration:",
                list(duration_options_map.keys()),
                index=1
            )
            st.session_state.challenge_duration_seconds = duration_options_map[selected_duration_label]
            st.write(f"DEBUG: Challenge duration selected: {st.session_state.challenge_duration_seconds} seconds.")

            if st.button("🚀 Start Challenge!", type="primary", use_container_width=True):
                st.write("DEBUG: 'Start Challenge!' button clicked.")
                st.session_state.challenge_active = True
                st.session_state.challenge_start_time = time.time()
                st.session_state.challenge_correct_score = 0
                st.session_state.challenge_incorrect_score = 0
                st.session_state.challenge_questions_attempted = 0
                st.write("DEBUG: Challenge state initialized for start.")
                if st.session_state.current_subnet_question is None :
                    st.write("DEBUG: No current subnet question at challenge start, generating one.")
                    try:
                        st.session_state.current_subnet_question = generate_random_ip_scenario()
                    except Exception as e_gen_chal_start:
                        st.write(f"ERROR: Failed to generate question on challenge start: {e_gen_chal_start}")
                        st.error("Failed to start challenge: Could not generate a question.")
                        st.session_state.challenge_active = False # Revert active state
                        st.rerun() # Rerun to show setup again
                request_new_challenge_question() # This will get a new q and rerun

        else: # Challenge is active
            st.write("DEBUG: Challenge is active.")
            if q is None:
                st.write("ERROR: Challenge active but q is None. This should not happen. Restarting challenge setup.")
                st.error("Error in challenge: No question loaded. Restarting challenge setup.")
                st.session_state.challenge_active = False
                st.rerun()
                st.stop() # Stop further execution in this path

            time_now = time.time()
            time_elapsed = time_now - st.session_state.challenge_start_time
            time_remaining = st.session_state.challenge_duration_seconds - time_elapsed
            st.write(f"DEBUG: Challenge Timer - Elapsed: {time_elapsed:.2f}s, Remaining: {time_remaining:.2f}s")

            if time_remaining <= 0:
                st.write("DEBUG: Challenge time is up.")
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
                    st.write("DEBUG: 'Try Another Challenge?' button clicked.")
                    st.session_state.challenge_active = False # Ensure it's false
                    st.rerun()
                st.stop() # Stop further processing for this active challenge iteration

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

            st.write(f"DEBUG: Challenge Mode - Question {st.session_state.challenge_questions_attempted + 1}: IP {q['given_ip_str']}/{q['cidr']}")
            st.markdown(f"#### Question {st.session_state.challenge_questions_attempted + 1}:")
            st.markdown(f"**Given IP Address / CIDR:** `{q['given_ip_str']}/{q['cidr']}`")
            st.markdown("*(Calculate all fields below)*")
            st.markdown("---")

            challenge_form_key = f"challenge_answer_form_{st.session_state.challenge_questions_attempted}"
            st.write(f"DEBUG: Challenge form key: {challenge_form_key}")

            with st.form(key=challenge_form_key):
                st.write("DEBUG: Challenge form rendering.")
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
                st.write("DEBUG: Challenge form rendered.")

            if challenge_submit_button:
                st.write("DEBUG: Challenge form submitted.")
                st.write(f"DEBUG: User challenge answers (raw from form): {c_ans}")
                st.session_state.challenge_questions_attempted += 1
                is_current_q_fully_correct_challenge = True

                try:
                    if not (c_ans.get('subnet_mask','').strip() == q['correct_subnet_mask_str']): is_current_q_fully_correct_challenge = False
                    if not (c_ans.get('network_address','').strip() == q['correct_network_address_str']): is_current_q_fully_correct_challenge = False
                    if not (c_ans.get('broadcast_address','').strip() == q['correct_broadcast_address_str']): is_current_q_fully_correct_challenge = False

                    user_c_uhc = c_ans.get('usable_hosts_count')
                    if not ((user_c_uhc is not None) and (int(user_c_uhc) == q['correct_usable_hosts_count'])): is_current_q_fully_correct_challenge = False

                    if not (c_ans.get('first_usable_ip','').strip() == q['correct_first_usable_ip_str']): is_current_q_fully_correct_challenge = False
                    if not (c_ans.get('last_usable_ip','').strip() == q['correct_last_usable_ip_str']): is_current_q_fully_correct_challenge = False
                    if not (c_ans.get('ip_class_type','') == q['correct_ip_class_type_str']): is_current_q_fully_correct_challenge = False

                    if c_ans.get('binary_given_ip','').strip():
                        user_bin_ip = get_binary_representation(c_ans['binary_given_ip'].strip())
                        st.write(f"DEBUG: Challenge binary_given_ip check - User: '{user_bin_ip}', Correct: '{q['correct_binary_given_ip']}'")
                        if not (user_bin_ip == q['correct_binary_given_ip'] and user_bin_ip not in ["Invalid Format", "Invalid Binary Octet", "Conversion Error", "Invalid IP/Mask for Binary"]):
                            is_current_q_fully_correct_challenge = False

                    if c_ans.get('binary_subnet_mask','').strip():
                        user_bin_mask = get_binary_representation(c_ans['binary_subnet_mask'].strip())
                        st.write(f"DEBUG: Challenge binary_subnet_mask check - User: '{user_bin_mask}', Correct: '{q['correct_binary_subnet_mask']}'")
                        if not (user_bin_mask == q['correct_binary_subnet_mask'] and user_bin_mask not in ["Invalid Format", "Invalid Binary Octet", "Conversion Error", "Invalid IP/Mask for Binary"]):
                            is_current_q_fully_correct_challenge = False

                    st.write(f"DEBUG: Challenge question correctness: {is_current_q_fully_correct_challenge}")

                    if is_current_q_fully_correct_challenge:
                        st.session_state.challenge_correct_score += 1
                        st.toast("✅ Correct!", icon="🎉")
                    else:
                        st.session_state.challenge_incorrect_score += 1
                        st.toast("❌ Incorrect. Next question!", icon="😥")
                    st.write(f"DEBUG: Challenge Scores - Correct: {st.session_state.challenge_correct_score}, Incorrect: {st.session_state.challenge_incorrect_score}")

                except KeyError as ke_chal_val:
                    st.write(f"ERROR: KeyError during challenge answer validation: {ke_chal_val}. Question 'q' might be missing keys: {q}")
                    st.error("An error occurred validating answers due to missing question data.")
                    st.session_state.challenge_incorrect_score += 1 # Penalize for error
                except Exception as e_chal_val:
                    st.write(f"ERROR: Exception during challenge answer validation: {e_chal_val}")
                    st.error(f"An error occurred while checking your challenge answers: {e_chal_val}. Marked as incorrect.")
                    st.session_state.challenge_incorrect_score += 1 # Penalize for error

                request_new_challenge_question() # This will rerun

            if st.session_state.challenge_active: # If still active after potential form submission rerun
                st.write("DEBUG: Challenge active, short sleep and rerun for timer update.")
                time.sleep(0.8) # Adjust as needed, was 0.8
                st.rerun()
        st.write("DEBUG: Challenge Mode UI rendering complete for this pass.")


# --- Module: Resource Hub ---
elif st.session_state.current_module == "Resource Hub":
    st.write("DEBUG: Resource Hub module selected.")
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
    st.write("DEBUG: Resource Hub content displayed.")

# --- Footer ---
st.write("DEBUG: Rendering Footer.")
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
st.write("DEBUG: Application script finished.")