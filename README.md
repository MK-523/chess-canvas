This app is an attempt to make chess games into digital art and transition into NFTs. Treating Chess PGN files as time-series datasets helps the engine map piece movements onto a coordinate plane. 

Technical Architecture:
- parsing PGN files through the python-chess library
- used a temporal rendering algorithm
  1. the variable is the move index (move number/final move number)
  2. when the index is closer to 0, the lines appear faint; when it's closer to 1, the lines are bold; the line width also widens over time
  3. Lines are semi transparent so when the same square is visited multiple times, the colors stack on top of each other

Installation and Usage:
git clone https://github.com/MK-523/chess-canvas.git
cd chess-canvas
pip install -r requirements.txt
streamlit run app.py
