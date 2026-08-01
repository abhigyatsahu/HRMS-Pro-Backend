// src/lib/zod/commonSchemas.ts

import { z } from "zod";

export const uuidSchema =
    z.uuid();

export const emailSchema =
    z.email();

export const phoneSchema =
    z
        .string()
        .min(10)
        .max(15);