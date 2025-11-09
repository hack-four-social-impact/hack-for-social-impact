import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

export interface PdfProcessResponse {
  success: boolean;
  filename: string;
  file_size: number;
  extracted_text_length: number;
  markdown_summary: string;
  summary_type: string;
}

export interface PdfProcessError {
  detail: string;
}

export async function uploadPdfForProcessing(
  file: File,
  prompt?: string,
  maxTokens?: number
): Promise<PdfProcessResponse> {
  const formData = new FormData();
  formData.append("file", file);

  if (prompt) {
    formData.append("prompt", prompt);
  }

  if (maxTokens) {
    formData.append("max_tokens", maxTokens.toString());
  }

  try {
    const response = await axios.post<PdfProcessResponse>(`${API_BASE_URL}/pdf/process`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    console.log("response", response);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      const errorData = error.response.data as PdfProcessError;
      throw new Error(errorData.detail || "Failed to process PDF");
    }
    throw new Error("Network error: Unable to connect to server");
  }
}
