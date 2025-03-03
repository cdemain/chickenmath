import streamlit as st

# Title
st.title("Backyard Egg Price Calculator")

# Initial Setup Costs
st.header("Initial Setup Costs")
initial_cost = 3000  # Fixed initial cost
st.write(f"Initial Expenses ($3,000 amortized over 10 years): ${initial_cost}")
amortized_initial_weekly = initial_cost / 10 / 52  # Weekly cost
st.write(f"Annual Amortized Cost: ${initial_cost / 10:.2f}/year (~${amortized_initial_weekly:.2f}/week)")

# Chicken Details
st.header("Chickens")
chicken_count = st.number_input("Number of Chickens", min_value=1, value=1, step=1)

chickens = []
total_chicken_cost_weekly = 0
total_eggs_per_week = 0

for i in range(chicken_count):
    st.subheader(f"Chicken {i + 1}")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(f"Name (optional) - Chicken {i + 1}", key=f"name_{i}")
        cost = st.number_input(f"Cost ($ over 3 years) - Chicken {i + 1}", min_value=0.0, value=0.0, key=f"cost_{i}")
    with col2:
        breed = st.text_input(f"Breed (optional) - Chicken {i + 1}", key=f"breed_{i}")
        rate = st.number_input(f"Egg Production Rate - Chicken {i + 1}", min_value=0.0, value=0.0, key=f"rate_{i}")
    
    chickens.append({"name": name, "breed": breed, "cost": cost, "rate": rate})
    total_chicken_cost_weekly += cost / 3 / 52  # Amortized weekly
    total_eggs_per_week += rate  # Will adjust based on unit below

# Egg Production Rate Unit
st.header("Egg Production")
rate_unit = st.selectbox("Rate Unit", ["Per Week", "Per Year"])
if rate_unit == "Per Year":
    total_eggs_per_week = total_eggs_per_week / 52  # Convert to weekly

# Ongoing Expenses
st.header("Ongoing Expenses")
def get_weekly_cost(label, key_prefix):
    col1, col2 = st.columns([2, 1])
    with col1:
        cost = st.number_input(f"{label} Cost", min_value=0.0, value=0.0, key=f"{key_prefix}_cost")
    with col2:
        unit = st.selectbox("Unit", ["Per Week", "Per Month", "Per Year"], key=f"{key_prefix}_unit")
    if unit == "Per Month":
        return cost / 4.33  # Approx weeks per month
    elif unit == "Per Year":
        return cost / 52
    return cost

feed_cost = get_weekly_cost("Feed", "feed")
gravel_cost = get_weekly_cost("Gravel", "gravel")
oyster_shell_cost = get_weekly_cost("Oyster Shell", "oyster")
nesting_cost = get_weekly_cost("Nesting Box Pads", "nesting")
coop_lining_cost = get_weekly_cost("Coop Lining", "coop")

# Sale Incidentals
st.header("Sale Incidentals")
def get_carton_cost(label, key_prefix):
    col1, col2 = st.columns([2, 1])
    with col1:
        cost = st.number_input(f"{label} Cost", min_value=0.0, value=0.0, key=f"{key_prefix}_cost")
    with col2:
        unit = st.selectbox("Unit", ["Per Carton", "Per 10 Cartons", "Per 100 Cartons"], key=f"{key_prefix}_unit")
    if unit == "Per 10 Cartons":
        return cost / 10
    elif unit == "Per 100 Cartons":
        return cost / 100
    return cost

carton_cost = get_carton_cost("Egg Carton", "carton")
stamp_cost = get_carton_cost("Stamp/Ink", "stamp")

# Profit Margin
st.header("Profit Margin")
profit_margin = st.number_input("Desired Profit Margin (%)", min_value=0.0, value=19.0, step=0.1)

# Calculate Selling Price
if st.button("Calculate Selling Price"):
    # Total weekly cost
    total_weekly_cost = (amortized_initial_weekly + total_chicken_cost_weekly + 
                         feed_cost + gravel_cost + oyster_shell_cost + nesting_cost + coop_lining_cost)
    
    # Cost per egg
    cost_per_egg = total_weekly_cost / total_eggs_per_week if total_eggs_per_week > 0 else 0
    incidental_cost_per_egg = (carton_cost + stamp_cost) / 12  # Per egg in a dozen
    
    # Total cost per dozen
    cost_per_dozen = (cost_per_egg + incidental_cost_per_egg) * 12
    
    # Selling price with profit margin
    selling_price_per_dozen = cost_per_dozen * (1 + profit_margin / 100)
    
    # Display result
    st.header("Result")
    st.write(f"Selling Price per Dozen: ${selling_price_per_dozen:.2f}")
else:
    st.write("Click 'Calculate Selling Price' to see the result.")
