import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "AI Tutor Assistant | Multi-Agent Educational AI by Soham",
  description: "Advanced multi-agent AI tutoring system powered by Gemini AI. Get intelligent help with math calculations, physics problems, and general learning. Built by Soham with FastAPI and Next.js.",
  keywords: ["AI tutor", "multi-agent", "education", "math", "physics", "learning", "AI assistant", "Soham"],
  authors: [{ name: "Soham", url: "https://sohambuilds.github.io" }],
  creator: "Soham",
  robots: "index, follow",
  openGraph: {
    title: "AI Tutor Assistant | Multi-Agent Educational AI",
    description: "Advanced AI tutoring system with specialized agents for math, physics, and general learning",
    url: "https://sohambuilds.github.io",
    siteName: "AI Tutor Assistant",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "AI Tutor Assistant | Multi-Agent Educational AI",
    description: "Advanced AI tutoring system with specialized agents for math, physics, and general learning",
    creator: "@neuralxtract",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
