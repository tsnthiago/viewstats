"use client"

import { useState, type FormEvent } from "react"
import { useRouter, useSearchParams } from "next/navigation"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Search } from "lucide-react"

interface SearchBarProps {
  initialQuery?: string
  placeholder?: string
  className?: string
}

export function SearchBar({ initialQuery = "", placeholder = "Search videos...", className }: SearchBarProps) {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [query, setQuery] = useState(initialQuery || searchParams.get("q") || "")

  const handleSearch = (e: FormEvent) => {
    e.preventDefault()
    if (query.trim()) {
      router.push(`/search?q=${encodeURIComponent(query.trim())}`)
    } else {
      router.push("/search") // Or homepage if preferred
    }
  }

  return (
    <form onSubmit={handleSearch} className={`flex w-full items-center space-x-2 ${className}`}>
      <Input
        type="search"
        placeholder={placeholder}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="flex-grow text-base h-12 rounded-lg focus-visible:ring-brand-accent-light dark:focus-visible:ring-brand-accent-dark"
        aria-label="Video search field"
      />
      <Button
        type="submit"
        size="lg"
        className="h-12 rounded-lg bg-brand-accent-light hover:bg-brand-accent-light/90 dark:bg-brand-accent-dark dark:hover:bg-brand-accent-dark/90 text-white dark:text-brand-text-dark bg-[rgba(9,9,11,1)]"
        aria-label="Search"
      >
        <Search className="h-5 w-5" />
      </Button>
    </form>
  )
}
