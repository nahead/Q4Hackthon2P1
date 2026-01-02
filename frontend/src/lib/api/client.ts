/**
 * Centralized API client for Phase II Full-Stack Web Application
 * Handles communication with the FastAPI backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/v1";

export type ApiRequestConfig = RequestInit & {
  params?: Record<string, string>;
};

class ApiClient {
  private async request<T>(path: string, config: ApiRequestConfig = {}): Promise<T> {
    const { params, headers, ...rest } = config;

    // Construct URL with query parameters
    let fullPath = path.startsWith('/') ? path : `/${path}`;
    if (!fullPath.endsWith('/')) {
      // Add trailing slash to avoid 307 Redirect CORS issues
      fullPath += '/';
    }
    const url = new URL(`${API_BASE_URL}${fullPath}`);
    if (params) {
      Object.entries(params).forEach(([key, value]) => url.searchParams.append(key, value));
    }

    // Default headers
    const defaultHeaders: Record<string, string> = {
      "Content-Type": "application/json",
      "Accept": "application/json",
    };

    // Merge headers
    const mergedHeaders = { ...defaultHeaders, ...headers };

    try {
      const response = await fetch(url.toString(), {
        ...rest,
        headers: mergedHeaders,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData?.error?.message || `API error: ${response.status}`);
      }

      // Handle 204 No Content
      if (response.status === 204) {
        return {} as T;
      }

      return await response.json();
    } catch (error) {
      console.error("API Request Failed:", error);
      throw error;
    }
  }

  get<T>(path: string, config: ApiRequestConfig = {}) {
    return this.request<T>(path, { ...config, method: "GET" });
  }

  post<T>(path: string, data?: any, config: ApiRequestConfig = {}) {
    return this.request<T>(path, {
      ...config,
      method: "POST",
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  put<T>(path: string, data?: any, config: ApiRequestConfig = {}) {
    return this.request<T>(path, {
      ...config,
      method: "PUT",
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  delete<T>(path: string, config: ApiRequestConfig = {}) {
    return this.request<T>(path, { ...config, method: "DELETE" });
  }
}

export const apiClient = new ApiClient();
