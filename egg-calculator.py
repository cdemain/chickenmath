import streamlit as st

# Title
st.title("Backyard Egg Price Calculator")

# Initial Setup Costs
st.header("Initial Setup Costs")
initial_cost = 3000  # Fixed initial cost
st.write(f"Initial Expenses ($3,000 to be recouped over 10 years): ${initial_cost}")

# Chicken Details
st.header("Chickens")
chicken_count = st.number_input("Number of Chickens", min_value=1, value=1, step=1)

chickens = []
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
    total_eggs_per_week += rate  # Will adjust based on unit below

# Egg Production Rate Unit
st.header("Egg Production")
rate_unit = st.selectbox("Rate Unit", ["Per Week", "Per Year"])
if rate_unit == "Per Year":
    total_eggs_per_week = total_eggs_per_week / 52  # Convert to weekly

# Calculate total eggs over relevant periods
total_eggs_3_years = total_eggs_per_week * 52 * 3  # For chicken costs (3-year amortization)
total_eggs_10_years = total_eggs_per_week * 52 * 10  # For initial cost (10-year amortization)
st.write(f"Estimated Eggs over 3 Years (for chicken costs): {total_eggs_3_years:.0f}")
st.write(f"Estimated Eggs over 10 Years (for initial cost): {total_eggs_10_years:.0f}")

# Per-egg cost from initial investment
initial_cost_per_egg = initial_cost / total_eggs_10_years if total_eggs_10_years > 0 else 0
st.write(f"Initial Cost per Egg: ${initial_cost_per_egg:.4f}")

# Per-egg cost from chickens
total_chicken_cost = sum(chicken["cost"] for chicken in chickens)
chicken_cost_per_egg = total_chicken_cost / total_eggs_3_years if total_eggs_3_years > 0 else 0
st.write(f"Chicken Cost per Egg (amortized over 3 years): ${chicken_cost_per_egg:.4f}")

# Ongoing Expenses (converted to per egg)
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

feed_cost_weekly = get_weekly_cost("Feed", "feed")
gravel_cost_weekly = get_weekly_cost("Gravel", "gravel")
oyster_shell_cost_weekly = get_weekly_cost("Oyster Shell", "oyster")
nesting_cost_weekly = get_weekly_cost("Nesting Box Pads", "nesting")
coop_lining_cost_weekly = get_weekly_cost("Coop Lining", "coop")

total_ongoing_weekly = (feed_cost_weekly + gravel_cost_weekly + oyster_shell_cost_weekly + 
                        nesting_cost_weekly + coop_lining_cost_weekly)
ongoing_cost_per_egg = total_ongoing_weekly / total_eggs_per_week if total_eggs_per_week > 0 else 0
st.write(f"Ongoing Cost per Egg: ${ongoing_cost_per_egg:.4f}")

# Sale Incidentals (per egg)
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

carton_cost_per_carton = get_carton_cost("Egg Carton", "carton")
stamp_cost_per_carton = get_carton_cost("Stamp/Ink", "stamp")
incidental_cost_per_egg = (carton_cost_per_carton + stamp_cost_per_carton) / 12  # Per egg in a dozen
st.write(f"Incidental Cost per Egg (carton + stamp): ${incidental_cost_per_egg:.4f}")

# Profit Margin
st.header("Profit Margin")
profit_margin = st.number_input("Desired Profit Margin (%)", min_value=0.0, value=19.0, step=0.1)

# Calculate Selling Price
if st.button("Calculate Selling Price"):
    # Total cost per egg
    total_cost_per_egg = (initial_cost_per_egg + chicken_cost_per_egg + 
                          ongoing_cost_per_egg + incidental_cost_per_egg)
    
    # Cost per dozen
    cost_per_dozen = total_cost_per_egg * 12
    
    # Selling price with profit margin
    selling_price_per_dozen = cost_per_dozen * (1 + profit_margin / 100)
    
    # Display result
    st.header("Result")
    st.write(f"Total Cost per Egg: ${total_cost_per_egg:.4f}")
    st.write(f"Cost per Dozen: ${cost_per_dozen:.2f}")
    st.write(f"Selling Price per Dozen (with {profit_margin}% margin): ${selling_price_per_dozen:.2f}")
else:
    st.write("Click 'Calculate Selling Price' to see the result.")
