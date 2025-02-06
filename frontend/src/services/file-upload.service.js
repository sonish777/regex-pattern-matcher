import axios from "axios";

class FileService {
    constructor(baseURL) {
        this._service = axios.create({
            baseURL,
            headers: { "Content-Type": "multipart/form-data" }
        });
    }

    async uploadFile(file, pattern, replacement, applyTransformations) {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("pattern", pattern);
        formData.append("replacement", replacement);
        formData.append("apply_transformations", applyTransformations);

        try {
            const response = await this._service.post("/upload/", formData);
            return response.data;
        } catch (error) {
            throw error.response?.data || { status: "error", errors: {} };
        }
    }

    async getProcessedData(sessionId, { page, rowsPerPage } = { page: 1, rowsPerPage: 5 }) {
        try {
            const response = await this._service.get("/processed-data/", {
                params: { session_id: sessionId, page, page_size: rowsPerPage }
            });
            return response.data;
        } catch (error) {
            throw error.response?.data || { status: "error", error: {} };
        }
    }
}

export const fileService = new FileService("http://localhost:8000/api");
