import streamlit as st
import chess.pgn
import io
from PIL import Image, ImageDraw, ImageFilter

# --- THEMES ---
PALETTE = {
    "Deep Sea": {"bg": "#0b0e14", "line": "#38bdf8", "accent": "#818cf8"},
    "Solar": {"bg": "#1e1e2e", "line": "#f5c2e7", "accent": "#fab387"},
    "Minimalist": {"bg": "#ffffff", "line": "#222222", "accent": "#ff4b4b"}
}

def get_coords(square_index, size, margin):
    file = square_index % 8
    rank = 7 - (square_index // 8)
    x = margin + (file * (size - 2 * margin) / 7)
    y = margin + (rank * (size - 2 * margin) / 7)
    return x, y

def create_chess_art(pgn_text, theme_name):
    size, margin = 1000, 100
    theme = PALETTE[theme_name]
    img = Image.new("RGB", (size, size), theme["bg"])
    draw = ImageDraw.Draw(img, "RGBA")
    
    pgn = io.StringIO(pgn_text)
    game = chess.pgn.read_game(pgn)
    if not game: return None
    
    board = game.board()
    moves = list(game.mainline_moves())
    
    for i, move in enumerate(moves):
        start_x, start_y = get_coords(move.from_square, size, margin)
        end_x, end_y = get_coords(move.to_square, size, margin)
        
        #moves become more vibrant in the art as game progresses
        progress = i / len(moves)
        alpha = int(70 + (185 * progress))
        width = int(2 + (8 * progress))
        color = theme["line"] + hex(alpha)[2:].zfill(2)
        
        draw.line([(start_x, start_y), (end_x, end_y)], fill=color, width=width)
        
        if board.is_capture(move):
            draw.ellipse([end_x-15, end_y-15, end_x+15, end_y+15], outline=theme["accent"], width=3)
        board.push(move)

    return img.filter(ImageFilter.GaussianBlur(radius=0.5))


#UI
st.set_page_config(page_title="GM.canvas", layout="centered")
st.title("GM.canvas")
st.markdown("Use PGN to make generative art")

with st.sidebar:
    st.header("Configure")
    theme = st.selectbox("Color Theme", list(PALETTE.keys()))
    pgn_data = st.text_area("Paste PGN", placeholder="1. e4 e5 2. Nf3...", height=300)

if st.button("Generate Art") and pgn_data:
    image = create_chess_art(pgn_data, theme)
    if image:
        st.image(image, use_container_width=True)
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        st.download_button("Download Image", buf.getvalue(), "my_chess_art.png", "image/png")
    else:
        st.error("Invalid PGN format.")
