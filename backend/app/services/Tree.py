# Tree.py
import numpy as np
# xây dựng 1 node lá trong cây 
class Node:
    # feature la cau hoi cau node nay 
    # threshold la nguong so sanh de chuyen sang nhanh left hoac right
    # left right la nhanh ben trai va phai cau nguowng
    # value la gia tri neu dau la nhanh la , la None neu ko la nhanh la

    def __init__(self, feature=None, threshold=None, left=None,right=None, value=None):
        self.feature= feature
        self.threshold=threshold
        self.left=left
        self.right=right
        self.value=value

    def is_final_node(self):
        return self.value is not None


# Xay dung ham tinh gini tinh  độ  trong, sạch của nhánh, 0-0.5, càng gần 0  càng tốt, giống loss funtion
def gini(data,class_weight={0:1, 1:1}):
    if len(data) == 0: 
        return 0
    
    # Đếm số lượng thực tế
    counts = np.bincount(data, minlength=2)
    
    # Nhân với trọng số (Class 0 nhân 1, Class 1 nhân 3)
    weights_array = np.array([class_weight.get(0, 1), class_weight.get(1, 1)])
    weighted_counts = counts * weights_array
    
    total_weight = np.sum(weighted_counts)
    if total_weight == 0:
        return 0
        
    # Tính Gini dựa trên trọng số
    mean = weighted_counts / total_weight
    return 1 - np.sum(mean * mean)



# khai bao cấu trúc cây quyết định
class DecisionTree:
    #  Khai bao giới hạn số node, độ sâu của cây, max_depth
    #root đánh dấu cái node gốc
    # xây dựng randum forest nên có thêm max_feature

    def __init__(self,max_depth = 5, max_feature=None, min_sample=5,class_weight=None): #độ sâu mặc định là 5
        self.max_depth=max_depth
        self.root=None  #mạc định đẻ NOne là rỗng
        self.max_feature=max_feature #số đặc trưng tối đa
        self.min_sample=min_sample # số lượng mẫu tối thiểu để chia node, nếu số lượng mẫu nhỏ hơn min_sample thì sẽ không chia nữa và tạo node lá
        self.feature_importances_ = None # để lưu giữ tầm quan trọng của đặc trưng => dùng để đánh giá feature
        self.class_weight = class_weight # để lưu giữ trọng số của các lớp => dùng để xử lý dữ liệu mất cân bằng

    # Hàm trông cây từ dữ liệu dầu vào 
    # X là dữ liệu dầu vào 
    # y là nhãn của dữ liêu
    def fit(self, X, y):
        # khởi tạo mẳng đặc trưng
        self.feature_importances_ = np.zeros(X.shape[1])
        # khởi tạo node gôcc của cây
        self.root=self._build_tree(X,y,depth=0)

        # chuẩn hóa tầm quan trọng của đặc trưng bằng cách chia cho tổng điểm cải thiện gini_gain của tất cả các đặc trưng
        total = np.sum(self.feature_importances_)
        if total > 0:
            self.feature_importances_ /= total

    
    # Hàm Xây dựng các nhánh của cây sử dụng đệ quy
    # X,y  tương tự trên 
    # depth là độ xâu của node hiện tại dùng để dừng nếu như độ  sạch gini của nhánh chưa phù hợp
    def _build_tree(self, X, y, depth):
        # lấy số hàng và số cột của dữ liệu dầu vào
        num_samples,  num_feature=X.shape

        # check điều kiện dừng
        # 1.  độ sâu đến giới hạn max_depth
        # 2.  dữ liệu còn lại chỉ có 1 nhẵn nên tỷ lệ đoán là 100%
        # 3. đã đến số lượng mẫu tối thiểu để chia node, nếu số lượng mẫu nhỏ hơn min_sample thì sẽ không chia nữa và tạo node lá
        if depth >= self.max_depth or len(np.unique(y))<2 or num_samples< self.min_sample:
            counts = np.bincount(y, minlength=2)

            weighted_counts = counts * np.array([self.class_weight[0], self.class_weight[1]])
            
            # Chọn nhãn có tổng TRỌNG SỐ lớn nhất, thay vì số lượng đông nhất
            most_val = weighted_counts.argmax() 
            return Node(value=most_val)
        
        #tìm  câu hỏi tốt nhật hiện tại
        # khai báo các biến best  tốt nhật 
        best_gain = -1
        best_feature, best_threhold=None,None


        # giá trị gini hiện tại
        val_curren_gini=gini(y,self.class_weight)

        # check xem max_feature dạng j 
        if self.max_feature is None:
            m = max(1, int(np.sqrt(num_feature)))
            num_feature_indx = np.random.choice(num_feature,m,replace=False)
        else:
            num_feature_indx=np.random.choice(num_feature,min(self.max_feature, num_feature),replace=False)

        # duyệt từng cột 1 
        for i in num_feature_indx:
            # lấy giá trị của cột
            colum_val=X[:,i]
            # lấy số lượng phần tử của cột đó
            unique_vals = np.unique(colum_val)
            # duyệt từng phần tử trong cột
            for j in range(len(unique_vals) - 1):
                # tính threshold là trung bình của 2 giá trị liên tiếp trong cột
                threshold=(unique_vals[j]+ unique_vals[j+1])/2
                # chia dữ liệu làm 2 phần dự trên threshold hiện tại
                # where trong numpy dùng để lấy các giá trị phù hợp điều kiện bên trong vì nó trả về dạng tuple(aray ) có 1 phần tử nên cần lấy chỉ số đầu tiên là 0 để lấy aray ra 
                left_data=np.where(colum_val <= threshold)[0] 
                right_data=np.where(colum_val > threshold)[0]

                # check xem dữ liệu đã  ok hay chưa nếu 1 bên đã chiếm hết giá trị 
                if(len(left_data) == 0 or len(right_data) == 0):
                    continue
                # tính gini của 2 nhánh sau khi chia
                gini_left=gini(y[left_data],self.class_weight)
                gini_right=gini(y[right_data],self.class_weight)
                
                #  tính số lượng node được chia cho mỗi nhanh 
                total_node_right, total_node_left=len(right_data),len(left_data)

                # tính trung bình gini sau khi chia ((n_left/N) *gini_left +(n_right/N)*gini_right)
                weighted_gini=(total_node_left/num_samples)*gini_left+(total_node_right/num_samples)*gini_right

                # tính điểm cải thiện của độ hỗn loạn vì ước muốn gini càng nhỏ càng tốt dữ liệu càng sạch nên mong muốn cái gini_gain  càng lớn càng tốt 
                # gini_gain là điểm cải thiện của cách chia này so với trc khi  bước vào nhánh 
                gini_gain=val_curren_gini- weighted_gini

                # so sách với best gini nếu tốt hơn thì cập nhật thôi
                if gini_gain >best_gain:
                    best_gain=gini_gain
                    best_feature=i
                    best_threhold=threshold

        # nếu không tìm được cách chia nào tốt hơn thì tạo node lá với giá trị lớn nhất hiện tại
        if best_gain == -1:
            counts = np.bincount(y, minlength=2)

            weighted_counts = counts * np.array([self.class_weight[0], self.class_weight[1]])
            
            # Chọn nhãn có tổng TRỌNG SỐ lớn nhất, thay vì số lượng đông nhất
            most_val = weighted_counts.argmax() 
            return Node(value=most_val)
        
        # cập nhật tầm quan trọng của đặc trưng đã chọn dựa trên điểm cải thiện gini_gain
        self.feature_importances_[best_feature] += best_gain

        # sau khi  tìm được cách chia tốt nhất thì chia nhánh
        # cái left right la mảng chỉ số cảu các phần tử 
        left_data=np.where(X[:, best_feature]<= best_threhold)[0]
        right_data=np.where(X[:,best_feature]>best_threhold)[0]

        # dùng để quy để tính lại chính nhánh left right đã tính ra
        left_child=self._build_tree(X[left_data],y[left_data],depth+1)
        right_child=self._build_tree(X[right_data],y[right_data],depth+1)

        # trả về node hiện tại và 2 nhánh tiếp theo
        return Node(feature=best_feature,threshold=best_threhold,left=left_child,right=right_child)


    # sau khi  đã xây dụng được các nhánh nhờ hàm buld và huấn luyện hay tạo ra cây nhờ hàm fit()
    # cần tạo ra hàm dự đoán từ những j đã xây trước đó 
    def predict(self,X):
        return np.array([self._predict_one_sample(self.root,sample) for sample in X])
    
    # hàm đi dọc từ  node _root xuống từng nhánh đến node final thì dừng lại
    def _predict_one_sample(self,node:Node,sample):
        # check xem có là node lá final ko  
        if node.is_final_node():
            return node.value
        
        # kiểm tra xem nên đi sang trái hay phải theo ngưỡng threshold cúa node
        if sample[node.feature]<=node.threshold:
            return self._predict_one_sample(node.left,sample)
        else:
            return self._predict_one_sample(node.right, sample)


# if __name__ == "__main__":
#     # 1. Tạo dữ liệu giả lập (X là các đặc trưng, y là nhãn kết quả)
#     # Ví dụ: [Tuổi, Thu nhập] - [Không mua (0), Mua (1)]
#     X = np.array([[20, 10], [25, 20], [40, 50], [50, 80]])
#     y = np.array([0, 0, 1, 1])

#     # 2. Khởi tạo và Huấn luyện (Đây chính là lúc máy "trồng rừng")
#     tree = DecisionTree(max_depth=3)
#     tree.fit(X, y)

#     # 3. Dự đoán với dữ liệu mới
#     data_moi = np.array([[22, 12], [45, 60]])
#     ket_qua = tree.predict(data_moi)

#     print(f"Dự đoán cho dữ liệu mới: {ket_qua}") 
#     # Kết quả sẽ là [0, 1] vì máy đã học được logic từ dữ liệu cũ