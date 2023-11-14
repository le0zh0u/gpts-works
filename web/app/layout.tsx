import "./globals.css";
import "react-lazy-load-image-component/src/effects/blur.css";

import Footer from "./components/Footer";
import Header from "./components/Header";
import { Inter } from "next/font/google";
import type { Metadata } from "next";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "ILoveGPTs - Let everyone find the right GPTs",
  description:
    "ILoveGPTs is a Third-party GPTs Collection. Let everyone find the right GPTs.",
  keywords:
    "GPTs, GPTs store, GPTs Works, ChatGPT, OpenAI GPTs, vector search GPTs, GPTs hunter, GPTshunter",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" type="image/png" sizes="16x16" href="/logo.png" />
      </head>
      <body className={inter.className}>
        <main>
          <Header />
          {children}
          <Footer />
        </main>

        <script
          defer
          data-domain="ilovegpts.com"
          src="https://plausible.io/js/script.js"
        ></script>
      </body>
    </html>
  );
}
