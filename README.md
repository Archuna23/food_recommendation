# Food Recommendation System (Content-Based Filtering)

Flask + Python backend, HTML/CSS/JS frontend.
Cosine similarity use panni user preferences-ku best 3 foods recommend pannum.

## Folder structure
```
food_recommender_app/
├── app.py               # Flask backend + recommendation logic
├── requirements.txt     # Python libraries
├── templates/
│   └── index.html       # Frontend page
└── static/
    ├── style.css        # Styling
    └── script.js        # Frontend logic (calls /api/recommend)
```

## How to run
```bash
pip install -r requirements.txt
python app.py
```
Browser-la open pannunga: http://127.0.0.1:5000

## How it works
1. User: Vegetarian (Yes/No) + Spicy, Healthy, Protein, Fast food (1-10) select pannuvaanga.
2. Frontend `POST /api/recommend` ku JSON anuppum.
3. `app.py` user vector `[veg, spicy, healthy, protein, fast_food]` create panni,
   `cosine_similarity` vachu ellaa foods-oda similarity calculate pannum.
4. Vegetarian = Yes na, veg foods mattum filter aagum.
5. Top 3 foods + full ranking JSON-a thirumbum, frontend display pannum.

## Dataset maatha
`app.py`-la `data` dictionary-la new foods add pannalaam
(ellaa lists-um same length-la irukkanum).
