#!/usr/bin/env python
import argparse
import os
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend"

sys.path.insert(0, str(BACKEND))

from preprocessing import preprocess_data
from app.services.Forest import RandomForest

def train_and_save_model(data_path: str, output_path: str):
    print("1. Đang đọc và tiền xử lý dữ liệu...")
    
    # 1. Gọi file preprocessing của bạn
    # Lưu ý: file preprocessing.py của bạn đã tự động xóa các cột leakage ('Churn Value', 'Churn Score',...) 
    df_final, le_target, target_col = preprocess_data(data_path)
    
    # 2. Tách X và y
    y_df = df_final[target_col]
    X_df = df_final.drop(columns=[target_col])
    
    X = X_df.values
    y = y_df.values
    feature_names = list(X_df.columns)

    print(f"Kích thước tập dữ liệu: X = {X.shape}, y = {y.shape}")

    # 3. Chia tập dữ liệu (80% Huấn luyện, 20% Kiểm tra)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Số lượng mẫu huấn luyện: {X_train.shape[0]}")
    print(f"Số lượng mẫu kiểm tra: {X_test.shape[0]}\n")

    # 4. Undersampling
    print("Đang cân bằng dữ liệu bằng phương pháp Undersampling...")
    idx_class_0 = np.where(y_train == 0)[0]
    idx_class_1 = np.where(y_train == 1)[0]
    
    np.random.seed(42)
    # Lấy 3000 mẫu lớp 0
    idx_class_0_downsampled = np.random.choice(idx_class_0, size=3000, replace=False)
    
    downsampled_indices = np.concatenate([idx_class_0_downsampled, idx_class_1])
    np.random.shuffle(downsampled_indices)
    
    X_train_downsampled = X_train[downsampled_indices]
    y_train_downsampled = y_train[downsampled_indices]
    
    print(f"Kích thước tập Train cũ : Lớp 0 có {len(idx_class_0)}, Lớp 1 có {len(idx_class_1)}")
    print(f"Kích thước tập Train mới: Lớp 0 có {np.sum(y_train_downsampled == 0)}, Lớp 1 có {np.sum(y_train_downsampled == 1)}\n")

    # 5. Khởi tạo và huấn luyện mô hình với tham số của bạn
    print("2. Đang huấn luyện mô hình RandomForest...")
    rf_model = RandomForest(
        n_estimators=200,    
        max_depth=7,        
        max_feature=None,     
        min_sample=9,        
        random_state=42,
        class_weight={0: 1, 1: 1.2} 
    )

    rf_model.fit(X_train_downsampled, y_train_downsampled)

    # In đặc trưng quan trọng
    importances = rf_model.feature_importances()
    feat_imp = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
    feat_imp = feat_imp.sort_values(by='Importance', ascending=False)
    
    print("\n--- TOP 3 ĐẶC TRƯNG QUAN TRỌNG NHẤT ---")
    print(feat_imp.head(10))
    print("\n--- CÁC ĐẶC TRƯNG VÔ DỤNG (NÊN XÓA BỎ) ---")
    print(feat_imp.tail(3))

    # 6. Đánh giá hiệu suất
    print("\n" + "="*45)
    print("3. KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH TRÊN TẬP TEST")
    print("="*45)
    
    acc = rf_model.accuracy(X_test, y_test)
    prec = rf_model.precision(X_test, y_test)
    rec = rf_model.recall(X_test, y_test)
    f1 = rf_model.f1_score(X_test, y_test)
    cm = rf_model.confusion_matrix(X_test, y_test)
    oob_acc = rf_model.oob_score(X_train_downsampled, y_train_downsampled)
    
    print(f"Accuracy  (Độ chính xác tổng thể): {acc:.4f}")
    print(f"Precision (Độ chuẩn xác)         : {prec:.4f}")
    print(f"Recall    (Độ bao phủ)           : {rec:.4f}")
    print(f"F1-Score                         : {f1:.4f}")
    print(f"OOB Accuracy (Độ chính xác OOB) : {oob_acc:.4f}")
    
    print("\nConfusion Matrix (Ma trận nhầm lẫn):")
    print("              Dự đoán 0   Dự đoán 1")
    print(f"Thực tế 0:      {cm[0][0]}         {cm[0][1]}")
    print(f"Thực tế 1:      {cm[1][0]}         {cm[1][1]}")

    # 7. Đóng gói và lưu mô hình
    print("\n" + "="*45)
    print("4. ĐANG LƯU MÔ HÌNH...")
    
    saved_package = {
        'model': rf_model,
        'X_test': X_test,
        'y_test': y_test,
        'feature_names': feature_names
    }
    
    out_path = Path(output_path)
    # Tự động tạo thư mục ml_models nếu chưa có
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(out_path, 'wb') as file:
        pickle.dump(saved_package, file)
        
    print(f"Đã Lưu mô hình thành công vào file '{out_path}'.")

    # thêm bước lưu các cái thồn số performan 
    # Chuyển Feature Importance thành danh sách có tên feature
    feature_importance = [
        {
            "feature": feature,
            "importance": float(score)
        }
        for feature, score in zip(feature_names, importances)
    ]

    # Sắp xếp giảm dần
    feature_importance.sort(
        key=lambda x: x["importance"],
        reverse=True
    )
    model_performance = {
        "accuracy": float(acc),
        "precision": float(prec),
        "recall": float(rec),
        "f1_score": float(f1),
        "oob_score": float(oob_acc),

        "confusion_matrix": {
            "true_negative": int(cm[0][0]),
            "false_positive": int(cm[0][1]),
            "false_negative": int(cm[1][0]),
            "true_positive": int(cm[1][1])
        },

        "feature_importance": feature_importance,

        "model_information": {
            "algorithm": "Custom Random Forest",
            "n_estimators": rf_model.n_estimators,
            "max_depth": rf_model.max_depth,
            "min_sample": rf_model.min_sample,
            "max_feature": rf_model.max_feature,
            "random_state": rf_model.random_state,
            "train_samples": int(X_train_downsampled.shape[0]),
            "test_samples": int(X_test.shape[0]),
            "feature_count": len(feature_names)
        }
    }
    import json

    performance_path = out_path.parent / "model_performance.json"

    with open(performance_path, "w", encoding="utf-8") as file:
        json.dump(
            model_performance,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Đã lưu Model Performance: {performance_path}")



def main():
    parser = argparse.ArgumentParser(description="Train custom Random Forest model for Churn")
    parser.add_argument(
        '--data', 
        type=str, 
        default='backend/ml_models/Telco_customer_churn.xlsx', 
        help='Đường dẫn tới file dữ liệu gốc'
    )
    parser.add_argument(
        '--output', 
        type=str, 
        default='backend/ml_models/rf_churn_model.pkl', 
        help='Đường dẫn lưu file pkl'
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.data):
        print(f"Lỗi: Không tìm thấy file dữ liệu tại {args.data}")
        return 1
        
    train_and_save_model(args.data, args.output)

if __name__ == "__main__":
    main()