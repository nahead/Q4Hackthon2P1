import { betterAuth } from "better-auth";

export const auth = betterAuth({
    database: {
        // In a production app, you would use a database adapter here.
        // For Phase II, we're using a simple setup that will communicate with the backend.
        // Better Auth will handle the session/cookie management.
        type: "sqlite", // Placeholder or simple adapter
    },
    emailAndPassword: {
        enabled: true,
    },
    // We'll plug in the backend API URL for any required server-side callbacks
    baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
});
