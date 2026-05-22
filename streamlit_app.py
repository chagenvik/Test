import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="3D Function Explorer",
    page_icon="🚀",
    layout="wide"
)

# -------------------------------------------------
# Styling
# -------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        135deg,
        #050816 0%,
        #0a0f2c 100%
    );
}

h1 {
    text-align: center;
    color: #00e5ff;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 Interactive 3D Function Explorer")

# -------------------------------------------------
# Sidebar Controls
# -------------------------------------------------
with st.sidebar:

    st.header("Controls")

    function_name = st.selectbox(
        "Choose Function",
        [
            "Wave",
            "Ripple",
            "Peaks",
            "Saddle",
            "Gaussian",
            "Spiral"
        ]
    )

    colorscale = st.selectbox(
        "Color Theme",
        [
            "Turbo",
            "Viridis",
            "Plasma",
            "Inferno",
            "Magma",
            "Rainbow",
            "Electric",
            "Jet"
        ]
    )

    amplitude = st.slider(
        "Amplitude",
        0.1,
        10.0,
        2.0,
        0.1
    )

    frequency = st.slider(
        "Frequency",
        0.1,
        10.0,
        2.0,
        0.1
    )

    resolution = st.slider(
        "Resolution",
        30,
        200,
        100
    )

# -------------------------------------------------
# Mesh
# -------------------------------------------------
x = np.linspace(-5, 5, resolution)
y = np.linspace(-5, 5, resolution)

X, Y = np.meshgrid(x, y)

R = np.sqrt(X**2 + Y**2)

# -------------------------------------------------
# Functions
# -------------------------------------------------
if function_name == "Wave":
    Z = amplitude * np.sin(frequency * X) * np.cos(frequency * Y)

elif function_name == "Ripple":
    Z = amplitude * np.sin(frequency * R)

elif function_name == "Peaks":
    Z = (
        3*(1-X)**2*np.exp(-(X**2) - (Y+1)**2)
        - 10*(X/5 - X**3 - Y**5)*np.exp(-X**2-Y**2)
        - 1/3*np.exp(-(X+1)**2 - Y**2)
    )

elif function_name == "Saddle":
    Z = amplitude * (X**2 - Y**2) / 10

elif function_name == "Gaussian":
    Z = amplitude * np.exp(-(X**2 + Y**2) / frequency)

elif function_name == "Spiral":
    theta = np.arctan2(Y, X)
    Z = amplitude * np.sin(frequency * R + theta * 4)

# -------------------------------------------------
# Plot
# -------------------------------------------------
fig = go.Figure()

fig.add_trace(
    go.Surface(
        x=X,
        y=Y,
        z=Z,
        colorscale=colorscale,
        lighting=dict(
            ambient=0.5,
            diffuse=1.0,
            specular=1.0,
            roughness=0.2,
            fresnel=0.5
        ),
        contours={
            "z": {
                "show": True,
                "width": 1
            }
        }
    )
)

fig.update_layout(
    template="plotly_dark",
    height=850,
    margin=dict(l=0, r=0, t=0, b=0),

    scene=dict(
        aspectmode="cube",

        camera=dict(
            eye=dict(x=1.5, y=1.5, z=1.0)
        ),

        xaxis_title="X",
        yaxis_title="Y",
        zaxis_title="Z",

        bgcolor="rgba(0,0,0,0)"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.info(
    "Drag with the mouse to rotate, scroll to zoom, "
    "and change the function or parameters from the sidebar."
)