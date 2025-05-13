
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw
import numpy as np

st.set_page_config(layout="wide")
st.title("📐 Floor Plan Sketch Board with Reference Grid Below")

# Sidebar settings
st.sidebar.header("🛠️ Canvas Settings")
stroke_width = st.sidebar.slider("Stroke width: ", 1, 10, 2)
stroke_color = st.sidebar.color_picker("Stroke color: ", "#000000")
bg_color = st.sidebar.color_picker("Canvas background color:", "#ffffff")
drawing_mode = st.sidebar.selectbox("Drawing tool:", ["freedraw", "rect", "circle"])
realtime_update = st.sidebar.checkbox("Update in realtime", True)
show_labels = st.sidebar.checkbox("Enable Room Labels", True)

# Canvas
canvas_result = st_canvas(
    fill_color="rgba(0, 0, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    update_streamlit=realtime_update,
    height=600,
    width=800,
    drawing_mode=drawing_mode,
    key="canvas",
)

# Room dimension display
pixels_per_meter = 50
room_labels = {}

if canvas_result and canvas_result.json_data is not None:
    for idx, obj in enumerate(canvas_result.json_data["objects"]):
        if obj["type"] == "rect":
            left = obj["left"]
            top = obj["top"]
            width = obj["width"]
            height = obj["height"]

            width_m = width / pixels_per_meter
            height_m = height / pixels_per_meter

            st.markdown(
                f"📏 **Room {idx+1}** — Width: `{width_m:.2f} m` | Height: `{height_m:.2f} m`"
            )

            if show_labels:
                label = st.text_input(f"Label for Room {idx+1}", key=f"label_{idx}")
                room_labels[f"Room_{idx+1}"] = {
                    "label": label,
                    "position": [int(left), int(top)],
                    "size_m": [round(width_m, 2), round(height_m, 2)]
                }

if room_labels:
    st.subheader("🏷 Room Labels Summary")
    st.json(room_labels)

# Create grid image to display below canvas
def generate_grid_image(width=800, height=600, interval=50):
    image = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(image)
    for x in range(0, width, interval):
        draw.line([(x, 0), (x, height)], fill=(220, 220, 220), width=1)
    for y in range(0, height, interval):
        draw.line([(0, y), (width, y)], fill=(220, 220, 220), width=1)
    return image

# Show grid image
st.markdown("### 📎 Reference Grid (1m x 1m)")
grid_img = generate_grid_image()
st.image(grid_img, caption="Use this grid as a visual reference for drawing.")
