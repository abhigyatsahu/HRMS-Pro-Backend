// src/features/auth/types/auth.types.ts

export interface AuthUser {
  uuid: string;

  username: string;

  email: string;

  first_name: string;
  last_name: string;
  full_name: string;

  is_staff: boolean;
  is_superuser: boolean;
}


export interface LoginCredentials {
  username: string;
  password: string;
}


export interface LoginResponse {
  success: boolean;
  message: string;
}


export interface CurrentUserResponse {
  success: boolean;
  message: string;
  data: AuthUser;
}


export interface CsrfResponse {
  success: boolean;

  data: {
    csrfToken: string;
  };
}