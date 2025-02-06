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
}

export const fileService = new FileService("http://localhost:8000/api");
