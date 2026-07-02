import pandas as pd
from sklearn.preprocessing import LabelEncoder


def preprocess_data(file_path):

    # =====================================================
    # 1. ĐỌC FILE
    # =====================================================
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    # Chuẩn hóa tên cột
    df.columns = df.columns.str.strip()
    raw_columns = list(df.columns)

    # =====================================================
    # 2. TÌM CỘT NHÃN
    # =====================================================
    target_col = "Churn Label"

    if target_col not in df.columns:
        possible_cols = [
            c for c in df.columns
            if "churn" in c.lower()
            and all(x not in c.lower()
                    for x in ["value", "score", "reason"])
        ]

        if possible_cols:
            target_col = possible_cols[0]
        else:
            raise KeyError(
                f"Không tìm thấy cột mục tiêu.\n"
                f"Các cột hiện có: {df.columns.tolist()}"
            )

    # =====================================================
    # 3. LOẠI BỎ DATA LEAKAGE + CỘT VÔ DỤNG
    # =====================================================
    cols_to_drop = [

        # Leakage
        "Churn Value",
        "Churn Score",
        "Churn Reason",

        # ID
        "CustomerID",

        # Địa lý quá chi tiết
        "City",
        "Zip Code",
        "Latitude",
        "Longitude",
        "Lat Long",

        # Zero variance
        "Count",
        "Country",
        "State"
    ]

    existing_cols = [c for c in cols_to_drop if c in df.columns]

    if existing_cols:
        df = df.drop(columns=existing_cols)

    # =====================================================
    # 4. XỬ LÝ TOTAL CHARGES
    # =====================================================
    total_charge_col = next(
        (
            c for c in df.columns
            if "total" in c.lower()
            and "charge" in c.lower()
        ),
        None
    )

    if total_charge_col:
        df[total_charge_col] = pd.to_numeric(
            df[total_charge_col],
            errors="coerce"
        ).fillna(0)

    # =====================================================
    # 5. MÃ HÓA NHÃN
    # =====================================================
    le_target = LabelEncoder()

    df[target_col] = le_target.fit_transform(
        df[target_col].astype(str)
    )

    # =====================================================
    # 6. TÁCH X / y
    # =====================================================
    y = df[target_col]

    X = df.drop(columns=[target_col])

    # =====================================================
    # 7. ONE HOT ENCODING
    # =====================================================
    X = pd.get_dummies(
        X,
        drop_first=True,
        dtype=int
    )

    # =====================================================
    # 8. XÓA CÁC DUMMY GẦN NHƯ TRÙNG LẶP
    # =====================================================
    useless_dummies = [
        c for c in X.columns
        if (
            "No internet service" in c
            or "No phone service" in c
        )
    ]

    if useless_dummies:
        X = X.drop(columns=useless_dummies)

    # =====================================================
    # 9. GHÉP LẠI
    # =====================================================
    df_final = pd.concat([X, y], axis=1)
    feature_names = list(X.columns)

    return (
        df_final,
        {target_col: le_target},
        target_col,
        feature_names,
        raw_columns
    )