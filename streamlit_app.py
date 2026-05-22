import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, date, time, timedelta, timezone
import pandas as pd

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Earth Time Machine",
    page_icon="🌍",
    layout="wide"
)

# ---------------------------------------------------
# STYLING
# ---------------------------------------------------

st.markdown("""
<style>
.stApp{
    background:linear-gradient(
        180deg,
        #050816,
        #0b132b
    );
}

h1{
    text-align:center;
    color:white;
}

[data-testid="stMetricValue"]{
    color:#7dd3fc;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("🌍 Earth Time Machine")

st.caption(
    "Explore Earth at any moment in time."
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.header("Time Controls")

    selected_date = st.date_input(
        "Date",
        value=date.today()
    )

    selected_time = st.time_input(
        "Time",
        value=datetime.utcnow().time()
    )

    auto_rotate = st.checkbox(
        "Animate Time",
        value=False
    )

    speed = st.slider(
        "Hours per frame",
        1,
        24,
        6
    )

# ---------------------------------------------------
# DATETIME
# ---------------------------------------------------

dt = datetime.combine(
    selected_date,
    selected_time
).replace(tzinfo=timezone.utc)

if auto_rotate:
    dt += timedelta(hours=speed)

# ---------------------------------------------------
# DAY OF YEAR
# ---------------------------------------------------

day_of_year = dt.timetuple().tm_yday

# ---------------------------------------------------
# SOLAR DECLINATION
# ---------------------------------------------------

solar_declination = (
    23.44 *
    np.sin(
        np.deg2rad(
            (360/365)*(day_of_year-81)
        )
    )
)

# ---------------------------------------------------
# SUBSOLAR LONGITUDE
# ---------------------------------------------------

utc_hours = (
    dt.hour
    + dt.minute/60
)

subsolar_lon = 180 - utc_hours*15

# ---------------------------------------------------
# TERMINATOR
# ---------------------------------------------------

lons = np.linspace(-180, 180, 720)

latitudes = []

decl = np.deg2rad(solar_declination)

for lon in lons:

    h = np.deg2rad(
        lon - subsolar_lon
    )

    lat = np.rad2deg(
        np.arctan(
            -np.cos(h)/np.tan(decl)
        )
    )

    latitudes.append(lat)

# ---------------------------------------------------
# FIGURE
# ---------------------------------------------------

fig = go.Figure()

# oceans

fig.add_trace(
    go.Scattergeo(
        lon=[],
        lat=[],
        mode="markers",
        showlegend=False
    )
)

# night terminator

fig.add_trace(
    go.Scattergeo(
        lon=lons,
        lat=latitudes,
        mode="lines",
        line=dict(
            width=3
        ),
        name="Day/Night Boundary"
    )
)

# sun position

fig.add_trace(
    go.Scattergeo(
        lon=[subsolar_lon],
        lat=[solar_declination],
        mode="markers+text",
        text=["☀️"],
        textposition="top center",
        marker=dict(
            size=18,
            color="yellow"
        ),
        name="Sun"
    )
)

fig.update_geos(
    projection_type="orthographic",
    projection_rotation=dict(
        lon=subsolar_lon
    ),
    showland=True,
    showcountries=True,
    showocean=True,
    landcolor="rgb(50,120,70)",
    oceancolor="rgb(20,40,80)",
    bgcolor="rgba(0,0,0,0)"
)

fig.update_layout(
    template="plotly_dark",
    height=700,
    margin=dict(
        l=0,
        r=0,
        t=0,
        b=0
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# MOON PHASE
# ---------------------------------------------------

known_new_moon = datetime(
    2000,
    1,
    6,
    tzinfo=timezone.utc
)

days_since = (
    dt - known_new_moon
).total_seconds() / 86400

lunation = 29.53058867

phase = (
    days_since % lunation
) / lunation

illumination = (
    1 - np.cos(2*np.pi*phase)
) / 2

if phase < 0.03:
    moon = "🌑 New Moon"
elif phase < 0.22:
    moon = "🌒 Waxing Crescent"
elif phase < 0.28:
    moon = "🌓 First Quarter"
elif phase < 0.47:
    moon = "🌔 Waxing Gibbous"
elif phase < 0.53:
    moon = "🌕 Full Moon"
elif phase < 0.72:
    moon = "🌖 Waning Gibbous"
elif phase < 0.78:
    moon = "🌗 Last Quarter"
else:
    moon = "🌘 Waning Crescent"

# ---------------------------------------------------
# SUNRISE SUNSET APPROX
# ---------------------------------------------------

daylight_hours = (
    12
    + 4*np.sin(
        np.deg2rad(
            solar_declination
        )
    )
)

# ---------------------------------------------------
# METRICS
# ---------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Solar Declination",
    f"{solar_declination:.1f}°"
)

c2.metric(
    "Subsolar Longitude",
    f"{subsolar_lon:.1f}°"
)

c3.metric(
    "Moon Illumination",
    f"{illumination*100:.0f}%"
)

c4.metric(
    "Estimated Daylight",
    f"{daylight_hours:.1f} h"
)

# ---------------------------------------------------
# MOON CARD
# ---------------------------------------------------

st.subheader("🌕 Moon Phase")

st.info(
    f"{moon}\n\n"
    f"Illumination: {illumination*100:.1f}%"
)

# ---------------------------------------------------
# SEASON
# ---------------------------------------------------

st.subheader("🌎 Earth Status")

if solar_declination > 20:
    season = "Northern Hemisphere Summer"
elif solar_declination < -20:
    season = "Northern Hemisphere Winter"
else:
    season = "Spring / Autumn Transition"

st.success(season)

# ---------------------------------------------------
# IMPORTANT DATES
# ---------------------------------------------------

events = pd.DataFrame({
    "Event":[
        "March Equinox",
        "June Solstice",
        "September Equinox",
        "December Solstice"
    ],
    "Approx Date":[
        "March 20",
        "June 21",
        "September 22",
        "December 21"
    ]
})

st.subheader("☀️ Seasonal Reference")

st.dataframe(
    events,
    use_container_width=True,
    hide_index=True
)