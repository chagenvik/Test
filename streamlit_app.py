import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, date, time
from skyfield.api import load
import numpy as np

st.set_page_config(
    page_title="Solar System Time Machine",
    page_icon="🪐",
    layout="wide"
)

# -----------------------------------------
# PAGE STYLE
# -----------------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #020617;
}

h1 {
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

st.title("☀️ Solar System Time Machine")

st.caption(
    "Explore the real positions of planets for any date and time."
)

# -----------------------------------------
# LOAD NASA EPHEMERIS
# -----------------------------------------

@st.cache_resource
def load_ephemeris():
    eph = load("de421.bsp")
    ts = load.timescale()
    return eph, ts

eph, ts = load_ephemeris()

sun = eph["sun"]

planet_keys = {
    "Mercury": "mercury barycenter",
    "Venus": "venus barycenter",
    "Earth": "earth",
    "Mars": "mars barycenter",
    "Jupiter": "jupiter barycenter",
    "Saturn": "saturn barycenter",
    "Uranus": "uranus barycenter",
    "Neptune": "neptune barycenter"
}

planet_colors = {
    "Mercury": "#B8B8B8",
    "Venus": "#E5C07B",
    "Earth": "#4F8BFF",
    "Mars": "#D65A31",
    "Jupiter": "#D9A066",
    "Saturn": "#F4D06F",
    "Uranus": "#8EE7F5",
    "Neptune": "#4169E1"
}

planet_sizes = {
    "Mercury": 10,
    "Venus": 12,
    "Earth": 12,
    "Mars": 10,
    "Jupiter": 18,
    "Saturn": 17,
    "Uranus": 15,
    "Neptune": 15
}

# -----------------------------------------
# SIDEBAR
# -----------------------------------------

with st.sidebar:

    st.header("Controls")

    selected_date = st.date_input(
        "Date",
        value=date.today()
    )

    selected_time = st.time_input(
        "Time",
        value=datetime.utcnow().time()
    )

    show_orbits = st.checkbox(
        "Show Orbits",
        value=True
    )

    selected_planet = st.selectbox(
        "Planet Details",
        list(planet_keys.keys())
    )

# -----------------------------------------
# CREATE SKYFIELD TIME
# -----------------------------------------

dt = datetime.combine(
    selected_date,
    selected_time
)

t = ts.utc(
    dt.year,
    dt.month,
    dt.day,
    dt.hour,
    dt.minute,
    dt.second
)

# -----------------------------------------
# PLANET POSITIONS
# -----------------------------------------

planet_positions = {}

for name, key in planet_keys.items():

    planet = eph[key]

    position = (
        sun.at(t)
        .observe(planet)
        .position
        .au
    )

    x = position[0]
    y = position[1]

    planet_positions[name] = {
        "x": x,
        "y": y,
        "distance": np.sqrt(x**2 + y**2)
    }

# -----------------------------------------
# PLOT
# -----------------------------------------

fig = go.Figure()

# Sun

fig.add_trace(
    go.Scatter(
        x=[0],
        y=[0],
        mode="markers",
        marker=dict(
            size=25,
            color="gold"
        ),
        name="Sun"
    )
)

# Orbit circles

if show_orbits:

    for planet_name in planet_positions:

        radius = planet_positions[planet_name]["distance"]

        theta = np.linspace(
            0,
            2*np.pi,
            500
        )

        fig.add_trace(
            go.Scatter(
                x=radius*np.cos(theta),
                y=radius*np.sin(theta),
                mode="lines",
                line=dict(
                    width=1
                ),
                opacity=0.25,
                showlegend=False
            )
        )

# Planets

for planet_name, pos in planet_positions.items():

    fig.add_trace(
        go.Scatter(
            x=[pos["x"]],
            y=[pos["y"]],
            mode="markers+text",
            text=[planet_name],
            textposition="top center",
            marker=dict(
                size=planet_sizes[planet_name],
                color=planet_colors[planet_name]
            ),
            name=planet_name
        )
    )

fig.update_layout(
    template="plotly_dark",
    height=850,

    plot_bgcolor="#020617",
    paper_bgcolor="#020617",

    xaxis=dict(
        title="AU",
        zeroline=False
    ),

    yaxis=dict(
        title="AU",
        scaleanchor="x",
        scaleratio=1,
        zeroline=False
    ),

    margin=dict(
        l=10,
        r=10,
        t=20,
        b=20
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------------
# PLANET INFO
# -----------------------------------------

planet = selected_planet
distance = planet_positions[planet]["distance"]

st.subheader(f"🪐 {planet}")

col1, col2 = st.columns(2)

col1.metric(
    "Distance From Sun",
    f"{distance:.2f} AU"
)

col2.metric(
    "X,Y Position",
    f"{planet_positions[planet]['x']:.2f}, "
    f"{planet_positions[planet]['y']:.2f}"
)

st.info(
    "Planet positions are calculated using NASA JPL "
    "DE421 ephemerides through Skyfield."
)