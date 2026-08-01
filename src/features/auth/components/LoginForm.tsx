// src/features/auth/components/LoginForm.tsx

import { useState } from "react";

import {
  Eye,
  EyeOff,
  Loader2,
  LogIn,
} from "lucide-react";

import { zodResolver } from "@hookform/resolvers/zod";

import {
  useForm,
} from "react-hook-form";

import { useLocation,useNavigate } from "react-router-dom";

import {
  Alert,
  AlertDescription,
} from "@/components/ui/alert";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

import { getApiErrorMessage } from "@/api/errors";

import { ROUTES } from "@/routes/routeConfig";

import { useLogin } from "../hooks";

import {
  loginSchema,
  type LoginFormValues,
} from "../schemas";

export function LoginForm() {
  const navigate = useNavigate();
  const location = useLocation();
  const loginMutation = useLogin();

  const from =
  location.state?.from?.pathname ??
  ROUTES.DASHBOARD;

  const [
    showPassword,
    setShowPassword,
  ] = useState(false);

  const {
    register,
    handleSubmit,
    formState: {
      errors,
      isSubmitting,
    },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),

    defaultValues: {
      username: "",
      password: "",
    },
  });

  const onSubmit = async (
    values: LoginFormValues,
  ) => {
    try {
      await loginMutation.mutateAsync(values);

      navigate(from, {
        replace: true,
      });
    } catch {
      // Error displayed below.
    }
  };

  const loading =
    isSubmitting ||
    loginMutation.isPending;

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="space-y-5"
      noValidate
    >
      {loginMutation.isError && (
        <Alert variant="destructive">
          <AlertDescription>
            {getApiErrorMessage(
              loginMutation.error,
            )}
          </AlertDescription>
        </Alert>
      )}

      <div className="space-y-2">
        <Label htmlFor="username">
          Username
        </Label>

        <Input
          id="username"
          type="text"
          autoComplete="username"
          placeholder="Enter your username"
          disabled={loading}
          aria-invalid={
            Boolean(errors.username)
          }
          {...register("username")}
        />

        {errors.username && (
          <p className="text-sm text-destructive">
            {errors.username.message}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <Label htmlFor="password">
            Password
          </Label>

          <button
            type="button"
            className="text-sm text-primary hover:underline"
            onClick={() => {
              // Forgot password route later.
            }}
          >
            Forgot password?
          </button>
        </div>

        <div className="relative">
          <Input
            id="password"
            type={
              showPassword
                ? "text"
                : "password"
            }
            autoComplete="current-password"
            placeholder="Enter your password"
            disabled={loading}
            className="pr-10"
            aria-invalid={
              Boolean(errors.password)
            }
            {...register("password")}
          />

          <button
            type="button"
            onClick={() =>
              setShowPassword(
                (previous) => !previous,
              )
            }
            className="
              absolute right-3 top-1/2
              -translate-y-1/2
              text-muted-foreground
              hover:text-foreground
            "
            aria-label={
              showPassword
                ? "Hide password"
                : "Show password"
            }
          >
            {showPassword ? (
              <EyeOff className="size-4" />
            ) : (
              <Eye className="size-4" />
            )}
          </button>
        </div>

        {errors.password && (
          <p className="text-sm text-destructive">
            {errors.password.message}
          </p>
        )}
      </div>

      <Button
        type="submit"
        className="w-full"
        disabled={loading}
      >
        {loading ? (
          <>
            <Loader2 className="animate-spin" />
            Signing in...
          </>
        ) : (
          <>
            <LogIn />
            Sign in
          </>
        )}
      </Button>
    </form>
  );
}