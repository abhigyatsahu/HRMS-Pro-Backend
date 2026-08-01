// src/config/navigation/profile.ts

export interface ProfileMenuItem {
  title: string;
  path: string;
  icon?: string;
}

export const PROFILE_NAVIGATION: ProfileMenuItem[] = [
  {
    title: "My Profile",
    path: "/profile",
  },
  {
    title: "Account Settings",
    path: "/settings/account",
  },
  {
    title: "Change Password",
    path: "/settings/change-password",
  },
  {
    title: "Logout",
    path: "/logout",
  },
];