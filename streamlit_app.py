import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math

def find_clashing_pairs(chromosome):
    clashes = []
    for i in range(len(chromosome)):
        for j in range(i + 1, len(chromosome)):
            row1, col1 = chromosome[i], i
            row2, col2 = chromosome[j], j
            if row1 == row2 or abs(row1 - row2) == abs(col1 - col2):
                clashes.append(((row1, col1), (row2, col2)))
    return clashes

def draw_chessboard(chromosome):
    board_size = len(chromosome)
    board = np.zeros((board_size, board_size))

    for row in range(board_size):
        for col in range(board_size):
            board[row, col] = (row + col) % 2

    clash_pairs = find_clashing_pairs(chromosome)
    clash_positions = set(pos for pair in clash_pairs for pos in pair)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(board, cmap='gray', extent=[0, board_size, 0, board_size])

    # Draw outer border
    border = plt.Rectangle((0, 0), board_size, board_size,
                           edgecolor='black', facecolor='none', linewidth=2)
    ax.add_patch(border)

    for (r1, c1), (r2, c2) in clash_pairs:
        x1, y1 = c1 + 0.5, r1 + 0.5
        x2, y2 = c2 + 0.5, r2 + 0.5
        ax.plot([x1, x2], [y1, y2], color='orange', linewidth=12, alpha=0.35)

    for col, row in enumerate(chromosome):
        color = 'orange' if (row, col) in clash_positions else 'green'
        ax.text(col + 0.5, row + 0.5, '♛', fontsize=38,
                ha='center', va='center', color=color)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')

    for i in range(board_size):
        ax.text(-0.3, i + 0.5, str(i), va='center', ha='right', fontsize=10)
        ax.text(i + 0.5, -0.3, str(i), va='top', ha='center', fontsize=10)

    total_clashes = len(clash_pairs)
    max_clash = math.comb(board_size, 2)
    ax.set_title(f"{str(chromosome)}\nFitness: {max_clash - total_clashes}", fontsize=14)
    return fig

st.title("N-Queens Clash Visualizer")


col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input("Enter Chromosome", value="1,2,6,0,7,5,3,4", label_visibility="collapsed")

with col2:
    generate = st.button("Generate")


if user_input and generate:
    try:
        chromosome = list(map(int, user_input.strip().split(',')))
        board_size = len(chromosome)

        if any(not (0 <= val < board_size) for val in chromosome):
            st.error(f"Each value must be between 0 and {board_size - 1}")
        else:
            fig = draw_chessboard(chromosome)
            col1, col2, col3 = st.columns([0.5, 3, 0.5])
            with col2:
                st.pyplot(fig)

    except ValueError:
        st.error("Invalid input! Please enter N comma-separated integers.")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; font-size: 13px;'>"
    "Created by <strong>Md. Khaliduzzaman Khan - KKS</strong>"
    "</div>",
    unsafe_allow_html=True
)