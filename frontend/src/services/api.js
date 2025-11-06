/**
 * API service layer for Agentic Platform frontend
 * Provides centralized API communication with error handling
 */

import axios from "axios";

// Base API configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // 10 second timeout
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor for logging (development)
apiClient.interceptors.request.use(
  (config) => {
    if (process.env.NODE_ENV === "development") {
      console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle common error scenarios
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;
      console.error(`API Error ${status}:`, data);

      // Create standardized error object
      const apiError = {
        status,
        message: data.detail || data.message || "An error occurred",
        data: data,
      };

      return Promise.reject(apiError);
    } else if (error.request) {
      // Network error
      console.error("Network Error:", error.message);
      return Promise.reject({
        status: 0,
        message: "Network error - please check your connection",
        data: null,
      });
    } else {
      // Other error
      console.error("Request Error:", error.message);
      return Promise.reject({
        status: 0,
        message: error.message || "An unexpected error occurred",
        data: null,
      });
    }
  }
);

/**
 * People API Service
 * Handles all people-related API operations
 */
export const peopleService = {
  /**
   * Get all people
   * @returns {Promise} List of all people with metadata
   */
  async getAllPeople() {
    try {
      const response = await apiClient.get("/api/people");
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  /**
   * Get person by ID
   * @param {number} personId - ID of the person to retrieve
   * @returns {Promise} Person data
   */
  async getPersonById(personId) {
    try {
      const response = await apiClient.get(`/api/people/${personId}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  /**
   * Create new person
   * @param {Object} personData - Person data to create
   * @param {string} personData.name - Person's name
   * @param {string} personData.role - Person's role
   * @param {string} personData.department - Person's department
   * @param {string} personData.staffing_status - Staffing status (staffed, bench, available)
   * @returns {Promise} Created person data
   */
  async createPerson(personData) {
    try {
      const response = await apiClient.post("/api/people", personData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  /**
   * Update existing person
   * @param {number} personId - ID of person to update
   * @param {Object} updateData - Fields to update
   * @returns {Promise} Updated person data
   */
  async updatePerson(personId, updateData) {
    try {
      const response = await apiClient.put(
        `/api/people/${personId}`,
        updateData
      );
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  /**
   * Delete person
   * @param {number} personId - ID of person to delete
   * @returns {Promise} Deletion confirmation
   */
  async deletePerson(personId) {
    try {
      const response = await apiClient.delete(`/api/people/${personId}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

/**
 * Beach API Service
 * Handles beach-related business logic API operations
 */
export const beachService = {
  /**
   * Get people currently on the beach
   * @returns {Promise} List of people on the beach with metadata
   */
  async getPeopleOnBeach() {
    try {
      const response = await apiClient.get("/api/beach");
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

/**
 * Documents API Service
 * Handles document retrieval and management
 */
export const documentsService = {
  /**
   * Get list of available documents
   * @returns {Promise} List of available policy documents
   */
  async getAvailableDocuments() {
    try {
      const response = await apiClient.get("/api/docs");
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  /**
   * Get document content by filename
   * @param {string} filename - Name of the document file
   * @returns {Promise} Document content (blob for binary files)
   */
  async getDocument(filename) {
    try {
      const response = await apiClient.get(`/api/docs/${filename}`, {
        responseType: "blob", // Handle binary files like PDFs
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  /**
   * Get document metadata
   * @param {string} filename - Name of the document file
   * @returns {Promise} Document metadata
   */
  async getDocumentInfo(filename) {
    try {
      const response = await apiClient.get(`/api/docs/${filename}/info`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  /**
   * Get document URL for direct access
   * @param {string} filename - Name of the document file
   * @returns {string} Direct URL to document
   */
  getDocumentUrl(filename) {
    return `${API_BASE_URL}/api/docs/${filename}`;
  },
};

/**
 * System API Service
 * Handles system-level operations
 */
export const systemService = {
  /**
   * Get system health status
   * @returns {Promise} System health information
   */
  async getHealthStatus() {
    try {
      const response = await apiClient.get("/health");
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  /**
   * Get system information
   * @returns {Promise} System information and available endpoints
   */
  async getSystemInfo() {
    try {
      const response = await apiClient.get("/");
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

/**
 * Utility functions for API service
 */
export const apiUtils = {
  /**
   * Check if error is a network error
   * @param {Object} error - Error object from API call
   * @returns {boolean} True if network error
   */
  isNetworkError(error) {
    return error.status === 0;
  },

  /**
   * Check if error is a client error (4xx)
   * @param {Object} error - Error object from API call
   * @returns {boolean} True if client error
   */
  isClientError(error) {
    return error.status >= 400 && error.status < 500;
  },

  /**
   * Check if error is a server error (5xx)
   * @param {Object} error - Error object from API call
   * @returns {boolean} True if server error
   */
  isServerError(error) {
    return error.status >= 500 && error.status < 600;
  },

  /**
   * Format error message for user display
   * @param {Object} error - Error object from API call
   * @returns {string} User-friendly error message
   */
  formatErrorMessage(error) {
    if (this.isNetworkError(error)) {
      return "Unable to connect to the server. Please check your internet connection.";
    }

    if (this.isServerError(error)) {
      return "Server error occurred. Please try again later.";
    }

    return error.message || "An unexpected error occurred.";
  },
};

// Export the configured axios instance for advanced usage
export { apiClient };

// Export default object with all services
export default {
  people: peopleService,
  beach: beachService,
  documents: documentsService,
  system: systemService,
  utils: apiUtils,
};
