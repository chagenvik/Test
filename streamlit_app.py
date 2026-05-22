import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="Interactive Solar System",
    page_icon="🪐",
    layout="wide"
)

st.title("☀️ Interactive Solar System")

# ------------------------------------
# Planet Data
# ------------------------------------
PLANETS = {
    "Mercury": {
        "distance": 0.39,
        "period": 88,
        "size": 6,
        "color": "#B0B0B0"
    },
    "Venus": {
        "distance": 0.72,
        "period": 225,
        "size": 10,
        "color": "#E8C27A"
    },
    "Earth": {
        "distance": 1.0,
        "period": 365,
        "size": 10,
        "color": "#3B82F6"
    },
    "Mars": {
        "distance": 1.52,
        "period": 687,
        "size": 8,
        "color": "#D65A31"
    },
    "Jupiter": {
        "distance": 5.2,
        "period": 4333,
        "size": 25,
        "color": "#D9A066"
    },
    "Saturn": {
        "distance": 9.54,
        "period": 10759,
        "size": 22,
        "color": "#F5D76E"
    },
    "Uranus": {
        "distance": 19.2,
        "period": 30687,
        "size": 16,
        "color": "#6BE6FF"
    },
    "Neptune": {
        "distance": 30.1,
        "period": 60190,
        "size": 16,
        "color": "#4169E1"
    }
}

# ------------------------------------
# Sidebar Controls
# ------------------------------------
with st.sidebar:

    st.header("⚙️ Controls")

    simulation_day = st.slider(
        "Simulation Day",
        0,
        10000,
        1000
    )

    scale_factor = st.slider(
        "Orbit Scale",
        1.0,
        5.0,
        2.0
    )

    show_orbits = st.checkbox(
        "Show Orbits",
        value=True
    )

    selected_planet = st.selectbox(
        "Planet Information",
        list(PLANETS.keys())
    )

# ------------------------------------
# Create Figure
# ------------------------------------
fig = go.Figure()

# Sun
fig.add_trace(
    go.Scatter3d(
        x=[0],
        y=[0],
        z=[0],
        mode="markers",
        marker=dict(
            size=35,
            color="gold"
        ),
        name="Sun"
    )
)

# ------------------------------------
# Planets
# ------------------------------------
for name, p in PLANETS.items():

    radius = p["distance"] * scale_factor

    angle = (
        2
        * np.pi
        * simulation_day
        / p["period"]
    )

    x = radius * np.cos(angle)
    y = radius * np.sin(angle)
    z = 0

    # Orbit ring
    if show_orbits:

        t = np.linspace(
            0,
            2*np.pi,
            300
        )

        fig.add_trace(
            go.Scatter3d(
                x=radius*np.cos(t),
                y=radius*np.sin(t),
                z=np.zeros_like(t),
                mode="lines",
                line=dict(
                    width=2
                ),
                opacity=0.3,
                showlegend=False
            )
        )

    # Planet
    fig.add_trace(
        go.Scatter3d(
            x=[x],
            y=[y],
            z=[z],
            mode="markers+text",
            text=[name],
            textposition="top center",
            marker=dict(
                size=p["size"],
                color=p["color"]
            ),
            name=name
        )
    )

# ------------------------------------
# Layout
# ------------------------------------
fig.update_layout(
    template="plotly_dark",
    height=900,

    scene=dict(
        aspectmode="data",

        xaxis=dict(
            visible=False
        ),
        yaxis=dict(
            visible=False
        ),
        zaxis=dict(
            visible=False
        ),

        bgcolor="black",

        camera=dict(
            eye=dict(
                x=1.5,
                y=1.5,
                z=0.8
            )
        )
    ),

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

# ------------------------------------
# Planet Info
# ------------------------------------
planet = PLANETS[selected_planet]

st.subheader(f"🪐 {selected_planet}")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Distance from Sun",
    f"{planet['distance']} AU"
)

col2.metric(
    "Orbital Period",
    f"{planet['period']} days"
)

col3.metric(
    "Relative Size",
    planet["size"]
)