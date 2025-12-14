import pandas as pd

pg_df = pd.read_csv("pg_data.csv")

def get_recommended_pgs(
    max_rent=None,
    min_rating=None,
    max_distance=None,
    gender_pref=None,
    room_type=None,
    needs_wifi=False,
    needs_meals=False,
    needs_ac=False,
    top_k=3
):
    df = pg_df.copy()

    # Availability (only normalize, don't filter hard unless sure)
    if "Availability" in df.columns:
        df["Availability"] = df["Availability"].astype(str).str.lower()
        # uncomment if your data really has "available"
        # df = df[df["Availability"] == "available"]

    if max_rent is not None:
        df = df[df["Rent"] <= max_rent]

    if min_rating is not None and "Rating" in df.columns:
        df = df[df["Rating"] >= min_rating]

    if max_distance is not None and "Distance_km" in df.columns:
        df = df[df["Distance_km"] <= max_distance]

    if gender_pref is not None and "Gender_Preference" in df.columns:
        df["Gender_Preference"] = df["Gender_Preference"].astype(str).str.lower()
        df = df[df["Gender_Preference"].str.contains(gender_pref.lower())]

    if room_type is not None and "Room_Type" in df.columns:
        df["Room_Type"] = df["Room_Type"].astype(str).str.lower()
        df = df[df["Room_Type"].str.contains(room_type.lower())]

    # Amenities – be forgiving
    def filter_yes(df_local, col_name, flag):
        if flag and col_name in df_local.columns:
            df_local[col_name] = df_local[col_name].astype(str).str.lower()
            df_local = df_local[df_local[col_name].str.contains("yes")]
        return df_local

    df = filter_yes(df, "WiFi", needs_wifi)
    df = filter_yes(df, "Meals", needs_meals)
    df = filter_yes(df, "AC", needs_ac)

    if df.empty:
        return []

    def score(row):
        rent_score = -row["Rent"]
        rating_score = row.get("Rating", 3) * 200
        dist_score = -row.get("Distance_km", 1) * 50
        verified_score = 200 if str(row.get("Verified", "No")).lower().startswith("y") else 0
        reviews = row.get("Customer_Reviews", 0)
        review_score = min(reviews, 100) * 2
        return rent_score + rating_score + dist_score + verified_score + review_score

    df["score"] = df.apply(score, axis=1)
    df = df.sort_values("score", ascending=False)

    cols = [c for c in df.columns if c != "score"]
    return df[cols].head(top_k).to_dict(orient="records")
