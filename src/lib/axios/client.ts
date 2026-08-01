// src/lib/axios/client.ts

import axios from "axios";

import { ENV } from "@/config/env";

export const apiClient = axios.create({
  baseURL: ENV.API_URL,
  withCredentials: true,
  withXSRFToken:true,
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFToken",
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});