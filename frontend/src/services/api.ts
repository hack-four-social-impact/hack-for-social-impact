import axios from "axios";

// Use environment variable for API base URL, fallback to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export interface PdfProcessResponse {
  success: boolean;
  filename: string;
  file_size: number;
  extracted_text_length: number;
  markdown_summary: string;
  summary_type: string;
}

export interface ParoleSummaryResponse {
  success: boolean;
  filename: string;
  file_size: number;
  extracted_text_length: number;
  markdown_summary: string;
  demographics: ClientDemographics;
  summary_type: string;
}

export interface ClientDemographics {
  clientInfo: {
    name: string;
    cdcrNumber: string;
    dateOfBirth: string;
    contactInfo: string;
  };
  introduction: {
    shortSummary: string;
  };
  evidenceUsedToConvict: string[];
  potentialTheory: string;
  convictionInfo: {
    dateOfCrime: string;
    locationOfCrime: string;
    dateOfArrest: string;
    charges: string;
    dateOfConviction: string;
    sentenceLength: string;
    county: string;
    trialOrPlea: string;
  };
  appealInfo: {
    directAppealFiled: string;
    appellateCourtCaseNumber: string;
    dateDecided: string;
    result: string;
    habenasFilings: string[];
  };
  attorneyInfo: {
    currentAttorneyForIncarceratedPerson: {
      name: string;
      title: string;
      firm: string;
      address: string;
      phone: string;
      email: string;
      presentAtHearing: boolean;
      representationContext: string;
    };
    trialAttorney: {
      name: string;
      address: string;
      phone: string;
      caseNumber: string;
      appointedOrRetained: string;
    };
    appellateAttorney: {
      name: string;
      address: string;
      phone: string;
      caseNumbers: string;
      courtLevel: string;
    };
    otherLegalRepresentation: Array<{
      name: string;
      role?: string;
      organization?: string;
    }>;
  };
  newEvidence: string[];
  codefendants: string;
  physicalDescription: {
    height: string;
    weight: string;
    race: string;
    build: string;
    distinguishingMarks: string;
  };
  victimInfo: {
    name: string;
    relationship: string;
  };
  prisonRecord: {
    conduct: string;
    programming: string;
    support: string;
  };
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

export async function generateParoleSummary(file: File): Promise<ParoleSummaryResponse> {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await axios.post<ParoleSummaryResponse>(`${API_BASE_URL}/pdf/parole-summary`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    console.log("Parole summary response", response);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      const errorData = error.response.data as PdfProcessError;
      throw new Error(errorData.detail || "Failed to generate parole summary");
    }
    throw new Error("Network error: Unable to connect to server");
  }
}
