import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
from PIL import Image

# Set page config (optional)
st.set_page_config(
    page_title="Airbnb Analysis",
    page_icon="🏠",
    layout="wide"
)

# Sidebar navigation menu
select = option_menu(
    None,
    options=["HOME", "EXPLORE DATA", "INSIGHTS", "ABOUT"],
    icons=["house", "bar-chart", "toggles", "at"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"width": "100%"},
        "icon": {"color": "white", "font-size": "20px"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-10px"},
        "nav-link-selected": {"background-color": "#FD5C63"}
    }
)

# Initialize session state variables
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

if 'air_df1' not in st.session_state:
    st.session_state.air_df1 = None

# HOME TAB
if select == 'HOME':
    
    # Header section with logo and title
    st.markdown("<h1 style='text-align: center; color: #FD5C63;'>Airbnb Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size:20px;'>Explore and Analyze Airbnb Listings with Interactive Visualizations</p>", unsafe_allow_html=True)
    
    
    col1, col2 = st.columns(2)
    with col1: # Project Overview Section
        st.subheader(':red[Project Overview]')
        st.markdown("In this project, we aim to explore and analyze Airbnb listings to gain insights into the short-term rental market. By examining factors such as pricing, availability, and guest reviews, we will identify trends and patterns that influence rental success. Utilizing data visualization techniques, we will present our findings, enabling potential hosts and guests to make informed decisions. This analysis will leverage various data sources to provide a comprehensive understanding of the Airbnb landscape.")
        
    with col2: # Add a logo or image (optional)
        image = Image.open('H:/Python/Airbnb Project/Airbnb logo.jpg')  # Update the path to your image
        st.image(image, use_column_width=True)

    # File Uploader Section
    st.write("## Upload Your Airbnb Dataset (CSV Format)")
    uploaded_file = st.file_uploader("Upload your Airbnb CSV file", type=["csv"])

    # Display file upload status
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file  # Store uploaded file in session state
        st.session_state.air_df1 = pd.read_csv(uploaded_file)  # Read CSV and store in session state
        st.success("File uploaded successfully!✅ You can now explore the data.")
        st.write(f"**Filename:** {uploaded_file.name}")
        
        # Preview of uploaded file (first 10 rows)
        st.write("### Preview of Uploaded Data")
        st.dataframe(st.session_state.air_df1.head(10))
    else:
        st.info("Awaiting file upload... Please upload a CSV file to get started.")

# EXPLORE DATA TAB
elif select == 'EXPLORE DATA':
    if st.session_state.uploaded_file is not None:
        st.markdown("### Explore Airbnb listings across the world.")
        # Geospatial Analysis (World)
        def geoGraph():
            st.subheader(":blue[Geospatial Distribution of Listings across the world]")
            if 'longitude' in st.session_state.air_df1.columns and 'latitude' in st.session_state.air_df1.columns:
                fig = px.scatter_mapbox(
                    st.session_state.air_df1, lon='longitude', lat='latitude', 
                    color='price', size='calculated_host_listings_count', 
                    color_continuous_scale='rainbow', hover_name='neighbourhood', 
                    range_color=(0, 200), mapbox_style='carto-positron', zoom=10
                )
                fig.update_layout(width=1200, height=600, title='Airbnb Listings across the world')
                st.plotly_chart(fig)
            else:
                st.error("Longitude and Latitude columns not found in the dataset.")
        
        geoGraph()

        # Country Filter Section
        st.markdown("### :green[Please use the dropdown box to explore listings country-wise.]")
        def country_filter(country):
            country_df = st.session_state.air_df1[st.session_state.air_df1['neighbourhood_group'] == country]
            country_df.reset_index(drop=True, inplace=True)
            fig = px.scatter_mapbox(
                country_df, lat='latitude', lon='longitude', color='price', 
                size='calculated_host_listings_count', hover_name='name', 
                hover_data=['room_type', 'price', 'availability_365'], 
                color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10, mapbox_style="carto-positron"
            )
            fig.update_layout(width=1150, height=800, title=f'Airbnb Listings across {country}')
            st.plotly_chart(fig)
            return country_df

        country = st.selectbox("Select the country you want to explore", st.session_state.air_df1['neighbourhood_group'].unique())
        cf = country_filter(country)
    else:
        st.warning("Please upload a file to explore the data.")

# INSIGHTS TAB
elif select == 'INSIGHTS':
    if st.session_state.uploaded_file is not None:
        st.subheader(':red[Price Analysis]')

        col1, col2 = st.columns(2)
        
        with col1:
            # 1. Average Price by Room Type
            st.write("### Average Price by Room Type")
            avg_price_room_type = st.session_state.air_df1.groupby('room_type')['price'].mean().reset_index()
            fig_price_room_type = px.bar(
                avg_price_room_type, x='room_type', y='price', color='room_type',
                title='Average Price by Room Type', labels={'price': 'Average Price (in USD)', 'room_type': 'Room Type'},
                height=400
            )
            st.plotly_chart(fig_price_room_type)

        with col2:
            # 2. Price Distribution (Histogram)
            st.write("### Price Distribution")
            fig_price_dist = px.histogram(
                st.session_state.air_df1, x='price', nbins=50, title='Price Distribution of Listings',
                labels={'price': 'Price (in USD)'}, color_discrete_sequence=['#636EFA'], height=400
            )
            st.plotly_chart(fig_price_dist)

        col1, col2 = st.columns(2)
        with col1:
            # 3. Price vs. Room Type and Availability
            st.write("### Price vs. Room Type and Availability")
            fig_price_room_availability = px.scatter(
                st.session_state.air_df1, x='availability_365', y='price', color='room_type', hover_data=['name', 'neighbourhood'],
                labels={'availability_365': 'Availability (days)', 'price': 'Price (in USD)', 'room_type': 'Room Type'},
                title='Price vs. Room Type and Availability', height=400
            )
            st.plotly_chart(fig_price_room_availability)

        with col2:
            # 4. Price vs. Number of Reviews
            st.write("### Price vs. Number of Reviews")
            fig_price_reviews = px.scatter(
                st.session_state.air_df1, x='number_of_reviews', y='price', color='room_type', hover_data=['name', 'neighbourhood'],
                labels={'number_of_reviews': 'Number of Reviews', 'price': 'Price (in USD)'},
                title='Price vs. Number of Reviews', height=400
            )
            st.plotly_chart(fig_price_reviews)
    else:
        st.warning("Please upload a file to view insights.")

# ABOUT TAB
elif select == 'ABOUT':
    st.subheader(":red[About this Project:]")
    st.write("The Airbnb Analysis project delves into the dynamics of the short-term rental market, focusing on key aspects such as property types, pricing strategies, and customer reviews. By leveraging data from various sources, we aim to uncover insights that can assist hosts in optimizing their listings and enhancing guest experiences. This project employs advanced data visualization techniques to present findings in an accessible manner, making it a valuable resource for both current and prospective Airbnb hosts. Ultimately, our goal is to contribute to a deeper understanding of the Airbnb ecosystem and facilitate informed decision-making.")
    
    st.subheader(":red[PowerBI Dashboard:]")
    st.image(Image.open(""))

    st.subheader(":red[Contact Details:]")
    st.write("**Author:** Akash P")
    st.write("**Contact:** iaka5h@outlook.com")
    st.write("**LinkedIN:** [linkedin.com/iaka5h](https://www.linkedin.com/in/iaka5h/)")
    st.write("**GitHub:** [github.com/iaka5h](https://github.com/iAka5h)")
   