# Forest.py
from .Tree import DecisionTree
import numpy as np

#khai báo cấu trúc của Randum forrest
class RandomForest:
    # Khai báo đầu vào của cây  Contructer
    # n_estimators là số lượng cây  của rừng 
    # max_depth là độ xây của mỗi cây
    # max_feature để xây dựng cây quyết định ngẫu nhiên hơn, cho chọn giới hạn các đặc trưng khi xây dựng cây quyết định
    # trees là danh sách các cây của rừng 
    # min_sample là số lượng mẫu tối thiểu để chia node, nếu số lượng mẫu nhỏ hơn min_sample thì sẽ không chia nữa và tạo node lá
    # random_state để đảm bảo tính tái lập của kết quả, nếu có giá trị thì sẽ sử dụng nó để tạo seed cho quá trình sinh ngẫu nhiên, giúp kết quả có thể tái lập được khi chạy lại mã nguồn với cùng một random_state.
    #  Nếu random_state là None, quá trình sinh ngẫu nhiên sẽ không được kiểm soát và kết quả có thể khác nhau mỗi lần chạy.
    # oob_indices để lưu trữ các chỉ số của mẫu không được chọn trong quá trình sinh ngẫu nhiên (out-of-bag samples)=> có thể dùng để đánh giá mô hình mà không cần tập kiểm tra riêng biệt
    # feature_importances_ để lưu giữ tầm quan trọng của đặc trưng => dùng để đánh giá feature
    # class_weight để lưu giữ trọng số của các lớp => dùng để xử lý dữ liệu mất cân bằng
    def __init__(self, n_estimators= 10, max_depth=5, max_feature=None, min_sample=5,  random_state=None,class_weight={0:1, 1:1}):
        self.n_estimators=n_estimators
        self.max_depth=max_depth
        self.max_feature=max_feature
        self.min_sample=min_sample
        self.random_state=random_state
        self.feature_importances_ = None
        self.class_weight = class_weight
        self.trees=[]
        self.oob_indices = [] 

    # sau khi khai báo xong contractor của rừng
    #xây dựng một hàm dùng để sinh các tập  dự liệu ngẫu nhiên 
    #bootrap_sample sinh có hoàn lại 
    def _bootstrap_sample(self, X, y):
        # lấy số hàng của dữ liệu  đầu vào 
        n_samples=X.shape[0]

        # lấy ngẫu nhiên n mẫu đánh chỉ số từ  0- n-1 mẫu của X
        # lấy bootstrap  có hoàn lại 
        # chỉ lấy chỉ số
        indices= np.random.choice(n_samples,n_samples,replace=True)

        # trả về dữ liệu sau khi  sinh ngẫu nhiên
        # Trả về cả dữ liệu X và y tương ứng với các chỉ số đã chọn
        # cùng với các chỉ số đó để có thể theo dõi được mẫu nào đã được chọn trong quá trình sinh ngẫu nhiên.
        return X[indices],y[indices],indices
    

    # xây dựng hàm fit huấn luyện forest
    def fit(self, X, y):
        self.trees=[]
        self.oob_indices = []

        # nếu random_state khác None thì sẽ sử dụng nó để tạo seed cho quá trình sinh ngẫu nhiên, giúp kết quả có thể tái lập được khi chạy lại mã nguồn với cùng một random_state.
        if self.random_state is not None:
            np.random.seed(self.random_state)

        for _ in range(self.n_estimators):
            # sinh ngẫu nhiên tập huấn luyện
            X_sample, y_sample ,indices = self._bootstrap_sample(X,y)
            
            # Lưu các mẫu ko  được chọn vào oob_indices
            # setdiff1d trả về phép trừ 2 mảng lấy các phần tử trong a mà không có trong b
            oob_idx = np.setdiff1d(np.arange(len(X)),indices)
            self.oob_indices.append(oob_idx)


            # huấn luyện cây dự vào dữ liệu vừa thêm vào 
            tree=DecisionTree(max_depth=self.max_depth, max_feature=self.max_feature, min_sample=self.min_sample,class_weight=self.class_weight)
            tree.fit(X_sample,y_sample)

            # lưu cây vào trong danh sách trees
            self.trees.append(tree)


        # tính importance của cả rừng
        self.feature_importances_ = np.zeros(X.shape[1])

        for tree in self.trees:
            self.feature_importances_ += tree.feature_importances_

        self.feature_importances_ /= self.n_estimators

        
    # Xây dựng hàm dự đoán 
    def predict(self, X):
        # cho từng cây dự đoán 
        tree_preds=np.array([tree.predict(X) for tree in self.trees] )

        # Chuyển vị để dễ lấy kết quả theo từng mẫu
        # tree_preds có dạng [[mảng dự đoán cây 1], [mảng dự đoán cây 2],[mảng dự đoán cây 3], ... , [mảng dự đoán cây n]]
        #  chuyển sang dạng [[danh sách đự doán mẫu 1] [danh sách dự đoán mẫu 2 ], .... [danh sách dự doán mẫu n ]]
        # tree_preds=tree_preds.T
        tree_preds = np.swapaxes(tree_preds, 0, 1)

        # dự đoán nào nhiều nhất thì chọn 
        predictions=[np.bincount(pred).argmax() for pred in  tree_preds]

        # trả về mảng dự đoán
        return np.array(predictions)
    
    # def predict(self, X, threshold=0.5):
    #     # Lấy xác suất dự đoán của từng mẫu
    #     # Kết quả có dạng:
    #     # [
    #     #   [P(class0), P(class1)],
    #     #   [P(class0), P(class1)],
    #     #   ...
    #     # ]
    #     proba = self.predict_proba(X)
    #     #   [0.7, 0.3],
    #     #   [0.4, 0.6]
    #     # proba[:,1] => [0.3, 0.6]
    #     churn_prob = proba[:, 1]

    #     predictions = (churn_prob >= threshold).astype(int)

    #     # Trả về mảng dự đoán cuối cùng
    #     return predictions

    # ===============================================================================================
    # ======sau khi  xây dựng xong các hàm dự đoán => xây dựng hàm đánh giá độ chính xác của rừng====
    # ===============================================================================================

    # Xây dựng hàm tính độ chính xác của rừng accuracy= true positive + true negative / tổng số mẫu
    def accuracy(self, X, y):
        y_pred=self.predict(X)
        return np.sum(y_pred==y)/len(y)
    
    # Xây dựng hàm tính độ chính xác của rừng precision= true positive / (true positive + false positive)
    def precision(self, X, y):
        y_pred=self.predict(X)
        true_positive=np.sum((y_pred==1) & (y==1))
        false_positive=np.sum((y_pred==1) & (y==0))
        if (true_positive + false_positive) == 0:
            return 0.0
        return true_positive/(true_positive+false_positive)
    
    # Xây dựng hàm tính độ chính xác của rừng recall= true positive / (true positive + false negative)
    def recall(self, X, y):
        y_pred=self.predict(X)
        true_positive=np.sum((y_pred==1) & (y==1))
        false_negative=np.sum((y_pred==0) & (y==1))
        if (true_positive + false_negative) == 0:
            return 0.0
        return true_positive/(true_positive+false_negative)
    
    # Xây dựng hàm tính độ chính xác của rừng f1_score= 2 * (precision * recall) / (precision + recall)
    def f1_score(self, X, y):
        precision=self.precision(X,y)
        recall=self.recall(X,y)
        if (precision + recall) == 0:
            return 0.0
        return 2 * (precision * recall) / (precision + recall)
    
    # xây dựng ma trận nhầm lẫn confusion_matrix
    def confusion_matrix(self, X, y):
        y_pred=self.predict(X)
        true_positive=np.sum((y_pred==1) & (y==1))
        true_negative=np.sum((y_pred==0) & (y==0))
        false_positive=np.sum((y_pred==1) & (y==0))
        false_negative=np.sum((y_pred==0) & (y==1))
        return np.array([
                    [true_negative, false_positive],
                    [false_negative, true_positive]
                ])
    

    # Hàm in ra tỷ lệ dự đoán cho từng mẫu được đưa ra bởi các cây trong rừng
    def predict_proba(self, X):
        tree_preds=np.array([tree.predict(X) for tree in self.trees] )
        tree_preds = np.swapaxes(tree_preds, 0, 1)

        proba=[]
        for pred in tree_preds:
            # thêm minlenght để đảm bảo rằng nếu có lớp nào không được dự đoán thì vẫn có xác suất 0 cho lớp đó
            counts = np.bincount(pred, minlength=2)
            proba.append(counts/counts.sum())
        
        return np.array(proba)
    
    # hàm tính oob score
    def oob_score(self, X, y):
        # tạo một danh sách để lưu trữ các dự đoán của các cây cho từng mẫu
        votes = [[] for _ in range(len(X))]

        # cho từng cây và các chỉ số của mẫu không được chọn (oob_idx) trong quá trình sinh ngẫu nhiên
        for tree, oob_idx in zip(
            self.trees,
            self.oob_indices
        ):
            # nếu không có mẫu nào không được chọn thì bỏ qua cây này
            if len(oob_idx) == 0:
                continue
            
            # dự đoán cho các mẫu không được chọn bằng cây hiện tại
            preds = tree.predict(X[oob_idx])

            # thêm các dự đoán vào danh sách votes cho từng mẫu
            for idx, pred in zip(oob_idx, preds):
                votes[idx].append(pred)

        # tính độ chính xác dựa trên các dự đoán của các cây cho từng mẫu
        y_true = []
        y_pred = []
        # duyệt qua từng mẫu và lấy dự đoán của các cây cho mẫu đó, nếu có dự đoán thì lấy dự đoán nhiều nhất làm dự đoán cuối cùng cho mẫu đó
        for i in range(len(X)):
            # nếu không có cây nào dự đoán cho mẫu này thì bỏ qua mẫu này
            if len(votes[i]) == 0:
                continue

            # lấy dự đoán nhiều nhất làm dự đoán cuối cùng cho mẫu đó
            pred = np.bincount(votes[i]).argmax()

            y_true.append(y[i])
            y_pred.append(pred)

        # tính độ chính xác dựa trên các dự đoán của các cây cho từng mẫu
        return np.mean(np.array(y_true) == np.array(y_pred))

    # hàm tính độ quan trọng của đặc trưng dựa trên điểm cải thiện gini_gain của các cây trong rừng
    def feature_importances(self):
        return self.feature_importances_
    
    

    
    


# if __name__ == "__main__":
#     # Giả sử bạn đã có code của class Node và class DecisionTree ở trên
#     X = np.array([[20, 10], [25, 20], [40, 50], [50, 80], [22, 12], [45, 60]])
#     y = np.array([0, 0, 1, 1, 0, 1])

#     # Khởi tạo Rừng với 10 cây
#     forest = RandomForest(n_estimators=100, max_depth=4,max_feature=None, min_sample=2, random_state=42)

#     # Huấn luyện
#     forest.fit(X, y)

#     # Dự đoán
#     ket_qua = forest.predict(np.array([[21, 11], [48, 70]]))
#     print(f"Dự đoán của Rừng: {ket_qua}")
    
