import type React from "react"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"
import { ThemeProvider } from "@/components/theme-provider"
import { ThemeToggleButton } from "@/components/theme-toggle-button"
import Link from "next/link"
import { VideoIcon } from "lucide-react"

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" })

export const metadata: Metadata = {
  title: "Semantic Video Search",
  description: "Find knowledge in videos intelligently.",
    generator: 'v0.dev'
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.variable} font-sans antialiased min-h-screen flex flex-col`}>
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem={false} // Disabling system preference to enforce default
          disableTransitionOnChange
        >
          <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="container flex h-14 max-w-screen-2xl items-center justify-between px-4 sm:px-6 lg:px-8">
              <Link
                href="/"
                className="flex items-center space-x-2 text-foreground hover:text-foreground/80 transition-colors"
              >
                <VideoIcon className="h-6 w-6" />
                <span className="font-bold text-lg">VideoSearch</span>
              </Link>
              <ThemeToggleButton />
            </div>
          </header>
          <main className="flex-grow container py-6 sm:py-8">{children}</main>
          <footer className="py-6 md:py-0 border-t">
            <div className="container flex flex-col items-center justify-center gap-2 md:h-16 md:flex-row">
              <p className="text-balance text-center text-xs sm:text-sm leading-loose text-muted-foreground">
                Semantic Video Search MVP &copy; {new Date().getFullYear()}
              </p>
            </div>
          </footer>
        </ThemeProvider>
      </body>
    </html>
  )
}
