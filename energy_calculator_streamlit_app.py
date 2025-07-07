import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Energy Consumption Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E8B57;
        font-size: 2.5em;
        margin-bottom: 1em;
    }
    .section-header {
        color: #4682B4;
        font-size: 1.5em;
        margin-top: 1em;
        margin-bottom: 0.5em;
    }
    .info-box {
        background-color: #f0f8ff;
        padding: 1em;
        border-radius: 10px;
        border-left: 5px solid #4682B4;
        margin: 1em 0;
    }
    .result-box {
        background-color: #f5fffa;
        padding: 1.5em;
        border-radius: 10px;
        border: 2px solid #2E8B57;
        margin: 1em 0;
        text-align: center;
    }
    .user-details {
        background-color: #f8f9fa;
        padding: 1em;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin: 1em 0;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">⚡ Energy Consumption Calculator</h1>', unsafe_allow_html=True)

# Initialize session state
if 'calculated' not in st.session_state:
    st.session_state.calculated = False

# Sidebar for user inputs
st.sidebar.markdown("## 📝 Enter Your Details")

# Collect user details
name = st.sidebar.text_input("Enter your name:", placeholder="Your Name")
age = st.sidebar.number_input("Enter your age:", min_value=1, max_value=120, value=25)
city = st.sidebar.text_input("Enter your city:", placeholder="Your City")
area = st.sidebar.text_input("Enter your area name:", placeholder="Your Area")

# Habitation type
habitation_type = st.sidebar.selectbox(
    "Are you living in a Flat or a House?",
    ["Select", "Flat", "House"]
)

# BHK type
bhk_type = st.sidebar.selectbox(
    "Which type of home do you have?",
    ["Select", "1BHK", "2BHK", "3BHK"]
)

st.sidebar.markdown("## 🏠 Appliances")

# Appliances
ac_present = st.sidebar.selectbox("Do you have an AC?", ["Select", "Yes", "No"])
fridge_present = st.sidebar.selectbox("Do you have a Fridge?", ["Select", "Yes", "No"])
washing_machine_present = st.sidebar.selectbox("Do you have a Washing Machine?", ["Select", "Yes", "No"])

# Calculate button
calculate_button = st.sidebar.button("🔍 Calculate Energy Consumption", type="primary")

# Function to calculate energy consumption
def calculate_energy(bhk_type, ac_present, fridge_present, washing_machine_present):
    cal_energy = 0
    breakdown = {}
    
    # Calculate base energy consumption based on BHK
    if bhk_type.lower() == "1bhk":
        lights_fans = (2 * 0.4 + 2 * 0.8) * 30  # 2 lights, 2 fans, 30 days
        breakdown["Lights & Fans"] = lights_fans
        cal_energy += lights_fans
    elif bhk_type.lower() == "2bhk":
        lights_fans = (3 * 0.4 + 3 * 0.8) * 30  # 3 lights, 3 fans, 30 days
        breakdown["Lights & Fans"] = lights_fans
        cal_energy += lights_fans
    elif bhk_type.lower() == "3bhk":
        lights_fans = (4 * 0.4 + 4 * 0.8) * 30  # 4 lights, 4 fans, 30 days
        breakdown["Lights & Fans"] = lights_fans
        cal_energy += lights_fans
    
    # Add appliances energy consumption
    if ac_present.lower() == "yes":
        ac_energy = 3 * 30  # AC adds 3 units per day for 30 days
        breakdown["Air Conditioner"] = ac_energy
        cal_energy += ac_energy
    
    if fridge_present.lower() == "yes":
        fridge_energy = 4 * 30  # Fridge adds 4 units per day for 30 days
        breakdown["Refrigerator"] = fridge_energy
        cal_energy += fridge_energy
    
    if washing_machine_present.lower() == "yes":
        wm_energy = 2 * 30  # Washing Machine adds 2 units per day for 30 days
        breakdown["Washing Machine"] = wm_energy
        cal_energy += wm_energy
    
    return cal_energy, breakdown

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Check if all required fields are filled
    all_fields_filled = (
        name and 
        bhk_type != "Select" and 
        habitation_type != "Select" and
        ac_present != "Select" and
        fridge_present != "Select" and
        washing_machine_present != "Select"
    )
    
    if calculate_button and all_fields_filled:
        st.session_state.calculated = True
        st.session_state.user_data = {
            'name': name,
            'age': age,
            'city': city,
            'area': area,
            'habitation_type': habitation_type,
            'bhk_type': bhk_type,
            'ac_present': ac_present,
            'fridge_present': fridge_present,
            'washing_machine_present': washing_machine_present
        }
    
    if st.session_state.calculated and 'user_data' in st.session_state:
        data = st.session_state.user_data
        
        # Calculate energy
        total_energy, energy_breakdown = calculate_energy(
            data['bhk_type'], 
            data['ac_present'], 
            data['fridge_present'], 
            data['washing_machine_present']
        )
        
        # Display user details
        st.markdown('<div class="section-header">👤 User Details</div>', unsafe_allow_html=True)
        
        user_details_html = f"""
        <div class="user-details">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1em;">
                <div>
                    <strong>Name:</strong> {data['name']}<br>
                    <strong>Age:</strong> {data['age']}<br>
                    <strong>City:</strong> {data['city']}
                </div>
                <div>
                    <strong>Area:</strong> {data['area']}<br>
                    <strong>Habitation Type:</strong> {data['habitation_type']}<br>
                    <strong>BHK Type:</strong> {data['bhk_type'].upper()}
                </div>
            </div>
        </div>
        """
        st.markdown(user_details_html, unsafe_allow_html=True)
        
        # Display energy consumption result
        st.markdown('<div class="section-header">⚡ Energy Consumption Result</div>', unsafe_allow_html=True)
        
        result_html = f"""
        <div class="result-box">
            <h2 style="color: #2E8B57; margin-bottom: 0.5em;">
                📊 Estimated Monthly Energy Consumption
            </h2>
            <h1 style="color: #FF6347; margin: 0; font-size: 3em;">
                {total_energy:.1f} units
            </h1>
            <p style="color: #666; margin-top: 0.5em;">
                Based on your home configuration and appliances
            </p>
        </div>
        """
        st.markdown(result_html, unsafe_allow_html=True)
        
        # Energy breakdown
        if energy_breakdown:
            st.markdown('<div class="section-header">📊 Energy Breakdown</div>', unsafe_allow_html=True)
            
            # Create DataFrame for better display
            breakdown_df = pd.DataFrame(
                list(energy_breakdown.items()), 
                columns=['Appliance', 'Energy (units)']
            )
            
            # Display breakdown table
            st.dataframe(
                breakdown_df, 
                use_container_width=True,
                hide_index=True
            )
            
            # Create pie chart
            fig_pie = px.pie(
                breakdown_df,
                values='Energy (units)',
                names='Appliance',
                title="Energy Consumption Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Create bar chart
            fig_bar = px.bar(
                breakdown_df,
                x='Appliance',
                y='Energy (units)',
                title="Monthly Energy Consumption by Appliance",
                color='Energy (units)',
                color_continuous_scale='viridis'
            )
            fig_bar.update_layout(
                xaxis_title="Appliance Type",
                yaxis_title="Energy Consumption (units)",
                showlegend=False,
                height=400
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Energy efficiency tips
        st.markdown('<div class="section-header">💡 Energy Efficiency Tips</div>', unsafe_allow_html=True)
        
        tips_html = """
        <div class="info-box">
            <h4>🌟 Tips to Reduce Energy Consumption:</h4>
            <ul>
                <li>💡 Use LED bulbs instead of incandescent bulbs</li>
                <li>🌡️ Set AC temperature to 24°C or higher</li>
                <li>❄️ Keep refrigerator temperature at optimal levels</li>
                <li>🔌 Unplug devices when not in use</li>
                <li>🪟 Use natural light during the day</li>
                <li>🌊 Use washing machine with full loads</li>
            </ul>
        </div>
        """
        st.markdown(tips_html, unsafe_allow_html=True)
        
    elif calculate_button and not all_fields_filled:
        st.error("⚠️ Please fill in all the required fields in the sidebar before calculating.")
    
    else:
        # Welcome message
        welcome_html = """
        <div class="info-box">
            <h3>👋 Welcome to the Energy Consumption Calculator!</h3>
            <p>This tool helps you estimate your monthly energy consumption based on your home type and appliances.</p>
            <p><strong>How to use:</strong></p>
            <ol>
                <li>Fill in your personal details in the sidebar</li>
                <li>Select your home type (BHK)</li>
                <li>Choose your appliances</li>
                <li>Click "Calculate Energy Consumption"</li>
            </ol>
        </div>
        """
        st.markdown(welcome_html, unsafe_allow_html=True)
        
        # Energy calculation methodology
        st.markdown('<div class="section-header">📋 How We Calculate</div>', unsafe_allow_html=True)
        
        methodology_html = """
        <div class="info-box">
            <h4>📊 Energy Calculation Methodology:</h4>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="background-color: #f8f9fa;">
                    <th style="border: 1px solid #dee2e6; padding: 8px; text-align: left;">Item</th>
                    <th style="border: 1px solid #dee2e6; padding: 8px; text-align: left;">Daily Consumption</th>
                    <th style="border: 1px solid #dee2e6; padding: 8px; text-align: left;">Monthly (30 days)</th>
                </tr>
                <tr>
                    <td style="border: 1px solid #dee2e6; padding: 8px;">Light (per unit)</td>
                    <td style="border: 1px solid #dee2e6; padding: 8px;">0.4 units</td>
                    <td style="border: 1px solid #dee2e6; padding: 8px;">12 units</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #dee2e6; padding: 8px;">Fan (per unit)</td>
                    <td style="border: 1px solid #dee2e6; padding: 8px;">0.8 units</td>
                    <td style="border: 1px solid #dee2e6; padding: 8px;">24 units</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #dee2e6; padding: 8px;">Air Conditioner</td>
                    <td style="border: 1px solid #dee2e6; padding: 8px;">3 units</td>
                    <td style="border: 1px solid #dee2e6; padding: 8px;">90 units</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #dee2e6; padding: 8px;">Refrigerator</td>
                    <td style="border: 1px solid #dee2e6; padding: 8px;">4 units</td>
                    <td style="border: 1px solid #dee2e6; padding: 8px;">120 units</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #dee2e6; padding: 8px;">Washing Machine</td>
                    <td style="border: 1px solid #dee2e6; padding: 8px;">2 units</td>
                    <td style="border: 1px solid #dee2e6; padding: 8px;">60 units</td>
                </tr>
            </table>
            <p style="margin-top: 1em;"><strong>BHK Configuration:</strong></p>
            <ul>
                <li><strong>1BHK:</strong> 2 lights + 2 fans</li>
                <li><strong>2BHK:</strong> 3 lights + 3 fans</li>
                <li><strong>3BHK:</strong> 4 lights + 4 fans</li>
            </ul>
        </div>
        """
        st.markdown(methodology_html, unsafe_allow_html=True)

with col2:
    # Display current selections
    st.markdown('<div class="section-header">🔧 Current Selections</div>', unsafe_allow_html=True)
    
    current_selections = f"""
    <div class="info-box">
        <p><strong>Name:</strong> {name if name else 'Not entered'}</p>
        <p><strong>Age:</strong> {age}</p>
        <p><strong>City:</strong> {city if city else 'Not entered'}</p>
        <p><strong>Area:</strong> {area if area else 'Not entered'}</p>
        <p><strong>Habitation:</strong> {habitation_type}</p>
        <p><strong>BHK Type:</strong> {bhk_type}</p>
        <hr>
        <p><strong>AC:</strong> {ac_present}</p>
        <p><strong>Fridge:</strong> {fridge_present}</p>
        <p><strong>Washing Machine:</strong> {washing_machine_present}</p>
    </div>
    """
    st.markdown(current_selections, unsafe_allow_html=True)
    
    # Validation status
    st.markdown('<div class="section-header">✅ Validation Status</div>', unsafe_allow_html=True)
    
    validation_items = [
        ("Name", name != ""),
        ("City", city != ""),
        ("Area", area != ""),
        ("Habitation Type", habitation_type != "Select"),
        ("BHK Type", bhk_type != "Select"),
        ("AC Status", ac_present != "Select"),
        ("Fridge Status", fridge_present != "Select"),
        ("Washing Machine Status", washing_machine_present != "Select")
    ]
    
    validation_html = "<div class='info-box'>"
    for item, status in validation_items:
        icon = "✅" if status else "❌"
        validation_html += f"<p>{icon} {item}</p>"
    validation_html += "</div>"
    
    st.markdown(validation_html, unsafe_allow_html=True)
    
    # Progress indicator
    completed_fields = sum(1 for _, status in validation_items if status)
    total_fields = len(validation_items)
    progress = completed_fields / total_fields
    
    st.markdown('<div class="section-header">📈 Progress</div>', unsafe_allow_html=True)
    st.progress(progress)
    st.write(f"Completed: {completed_fields}/{total_fields} fields")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2em;">
    <p>⚡ Energy Consumption Calculator | Built with Streamlit</p>
    <p><em>This calculator provides estimates based on standard consumption patterns.</em></p>
</div>
""", unsafe_allow_html=True)