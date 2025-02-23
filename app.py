import streamlit as st
import random
from layout import main

# A dictionary to simulate sending pin codes for verification
verification_pins = {}

st.set_page_config(layout="wide")

def send_pincode(email):
    """Simulate sending a pincode to the user's email."""
    # pincode = random.randint(1000, 9999)
    pincode = 1000
    verification_pins[email] = pincode
    st.session_state["last_pincode"] = pincode  # For demo purposes
    return pincode

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state["page"] = "login"  # Default page is login
if "email_verified" not in st.session_state:
    st.session_state["email_verified"] = False
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Function to switch pages
def navigate_to(page):
    st.session_state["page"] = page
    st.rerun()

# Function to add the header with logos
def add_header():
    st.markdown(
        """
        <style>
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 15px;
            background:white;
            border-radius:10px;
            width:100%;
            margin-left:0%;
            margin-top:-20px;

        }
        .logo {
            height: 30px;
        }
        .logo2{
            height:20px;
        }
        </style>
        <div class="header">
            <img src="https://i0.wp.com/trezo.com.br/wp-content/uploads/2023/08/logo-trezo.png?fit=696%2C697&ssl=1" alt="Logo" class="logo" widht="1500" height="1500" >
            
        </div>
        """,
        unsafe_allow_html=True
    )

# Get the current page from the query parameters or default to the session state
current_page = st.query_params.get("page", st.session_state["page"])

# Add header to all pages
add_header()

cols1, cols2, col3 = st.columns([1,2,1])
with cols2:
    
    if current_page == "login":
        st.markdown(
        """
        <style>
        .add-margin {
            margin-top:50px;

        }
        </style>
        <div class="add-margin"> </div>
        """,
        unsafe_allow_html=True
    )
        st.header("Login Page")
        st.write("Please log in to proceed.")

            # Input fields for login
        email = st.text_input("Enter your email ID:")
        password = st.text_input("Enter your password:", type="password")

        if st.button("Login"):
            if email.endswith("@trezo.com"):
                send_pincode(email)  # Simulate sending a pincode
                st.success(f"A pincode has been sent to {email}.")
                st.session_state["email_verified"] = True
                st.session_state["user_email"] = email
                navigate_to("pincode_verification")  # Redirect to pincode page
            else:
                st.error("User does not exist. Please enter a valid Email ID.")

    elif current_page == "pincode_verification" and not st.session_state["authenticated"]:
        st.markdown(
        """
        <style>
        .add-margin {
            margin-top:50px;

        }
        </style>
        <div class="add-margin"> </div>
        """,
        unsafe_allow_html=True
    )
        st.header("Pincode Verification")
        st.write(f"A pincode has been sent to {st.session_state['user_email']}. Please enter it below to proceed.")

        # Display the last sent pincode for demo purposes
        if "last_pincode" in st.session_state:
            st.info(f"(For demo purposes, your pincode is {st.session_state['last_pincode']})")

            # Input field for pincode
        pincode_input = st.text_input("Enter the pincode sent to your email:")

        if st.button("Verify Pincode"):
            if pincode_input == str(1000):
                st.success("Pincode verified successfully!")
                st.session_state["authenticated"] = True
                navigate_to("home")  # Redirect to dashboard page
            else:
                st.error("Invalid pincode. Please try again.")

if current_page == "home":
    main()
