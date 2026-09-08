import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const api = {
  // Reports
  getOccupancyReport: () => apiClient.get("/reports/occupancy").then(res => res.data),
  getRentCollection: () => apiClient.get("/reports/rent-collection").then(res => res.data),
  getMaintenancePerformance: () => apiClient.get("/reports/maintenance-performance").then(res => res.data),
  getTenantPayments: () => apiClient.get("/reports/tenant-payments").then(res => res.data),
  
  // Public Listings
  getPublicListings: () => apiClient.get("/listings/").then(res => res.data),
  getPublicListing: (id) => apiClient.get(`/listings/${id}`).then(res => res.data),
  
  // Entities (basic)
  getProperties: () => apiClient.get("/properties/").then(res => res.data),
  createProperty: (data) => apiClient.post("/properties/", data).then(res => res.data),
  
  // Uploads
  uploadImage: (formData) => apiClient.post("/upload/image", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  }).then(res => res.data),
  
  getUnits: () => apiClient.get("/units/").then(res => res.data),
  createUnit: (data) => apiClient.post("/units/", data).then(res => res.data),
  
  getTenants: () => apiClient.get("/tenants/").then(res => res.data),
  createTenant: (data) => apiClient.post("/tenants/", data).then(res => res.data),
  
  getSupportTickets: () => apiClient.get("/support/").then(res => res.data),
  createSupportTicket: (data) => apiClient.post("/support/", data).then(res => res.data),
  
  // Auth
  login: (data) => {
    // URL encoded form data required for OAuth2
    const params = new URLSearchParams();
    params.append('username', data.username);
    params.append('password', data.password);
    return apiClient.post("/auth/login", params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }).then(res => res.data);
  },
  signup: (data) => apiClient.post("/auth/signup", data).then(res => res.data),
  getMe: () => apiClient.get("/auth/me").then(res => res.data),
};

export default apiClient;
