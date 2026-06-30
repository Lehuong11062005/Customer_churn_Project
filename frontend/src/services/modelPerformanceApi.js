import axiosClient from "./axiosClient";

const modelPerformanceApi = {
    getPerformance: async () => {
        const response = await axiosClient.get("/model/performance");
        return response.data;
    },
};

export default modelPerformanceApi;