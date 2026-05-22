import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(
    page_title="Neon 3D Universe",
    page_icon="🌌",
    layout="wide"
)

# --------------------------
# Custom CSS
# --------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        135deg,
        #050510 0%,
        #0f1020 50%,
        #1a0033 100%
    );
}

h1 {
    text-align: center;
    color: #00ffff !important;
    text-shadow: 0px 0px 20px cyan;
}

[data-testid="stSidebar"] {
    background-color: rgba(10,10,30,0.9);
}
</style>
""", unsafe_allow_html=True)

st.title("🌌 Neon 3D Universe")

st.markdown(
    "<center><h4 style='color:#ff00ff;'>Interactive Animated Mathematical Galaxy</h4></center>",
    unsafe_allow_html=True
)

# --------------------------
# Controls
# --------------------------
with st.sidebar:
    st.header("🎛 Controls")

    speed = st.slider(
        "Animation Speed",
        0.01,
        0.30,
        0.08
    )

    amplitude = st.slider(
        "Wave Height",
        0.5,
        5.0,
        2.0
    )

    resolution = st.slider(
        "Resolution",
        30,
        120,
        70
    )

    colorscale = st.selectbox(
        "Colors",
        [
            "Turbo",
            "Viridis",
            "Plasma",
            "Inferno",
            "Magma",
            "Rainbow"
        ]
    )

# --------------------------
# Plot Container
# --------------------------
plot_placeholder = st.empty()

# --------------------------
# Animation Loop
# --------------------------
t = 0

while True:

    x = np.linspace(-5, 5, resolution)
    y = np.linspace(-5, 5, resolution)

    X, Y = np.meshgrid(x, y)

    R = np.sqrt(X**2 + Y**2)

    Z = (
        amplitude
        * np.sin(R * 2 - t)
        * np.cos(X + t/2)
        + np.sin(Y * 2 + t)
    )

    fig = go.Figure()

    fig.add_trace(
        go.Surface(
            x=X,
            y=Y,
            z=Z,
            colorscale=colorscale,
            showscale=False
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=750,
        margin=dict(l=0, r=0, b=0, t=0),

        scene=dict(
            bgcolor="rgba(0,0,0,0)",

            camera=dict(
                eye=dict(
                    x=1.8*np.cos(t*0.15),
                    y=1.8*np.sin(t*0.15),
                    z=1.2
                )
            ),

            xaxis=dict(
                backgroundcolor="black",
                gridcolor="cyan",
                zerolinecolor="cyan"
            ),

            yaxis=dict(
                backgroundcolor="black",
                gridcolor="magenta",
                zerolinecolor="magenta"
            ),

            zaxis=dict(
                backgroundcolor="black",
                gridcolor="yellow",
                zerolinecolor="yellow"
            )
        )
    )

    plot_placeholder.plotly_chart(
        fig,
        use_container_width=True
    )

    t += speed
    time.sleep(0.03)