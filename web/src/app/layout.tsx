import type { Metadata } from "next";
import type { ReactNode } from "react";
import "./globals.css";

export const metadata: Metadata = {
  title: "Meal Prep Atlas",
  description: "Build a consumer meal-prep planner that turns a weekly grocery and cooking inspiration video into a prep schedule, groce",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
