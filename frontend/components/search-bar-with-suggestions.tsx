"use client"

import type React from "react"

import { useState, useEffect, useRef, type FormEvent } from "react"
import { useRouter, useSearchParams } from "next/navigation"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Search, Hash, User } from "lucide-react"
import { fetchSearchSuggestions } from "@/lib/data"
import type { SearchSuggestion } from "@/lib/types"

interface SearchBarWithSuggestionsProps {
  initialQuery?: string
  placeholder?: string
  className?: string
}

export function SearchBarWithSuggestions({
  initialQuery = "",
  placeholder = "Search videos, channels, or topics...",
  className,
}: SearchBarWithSuggestionsProps) {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [query, setQuery] = useState(initialQuery || searchParams.get("q") || "")
  const [suggestions, setSuggestions] = useState<SearchSuggestion[]>([])
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [selectedIndex, setSelectedIndex] = useState(-1)
  const inputRef = useRef<HTMLInputElement>(null)
  const suggestionsRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const loadSuggestions = async () => {
      if (query.length >= 2) {
        const results = await fetchSearchSuggestions(query)
        setSuggestions(results)
        setShowSuggestions(true)
      } else {
        setSuggestions([])
        setShowSuggestions(false)
      }
    }

    const timeoutId = setTimeout(loadSuggestions, 300)
    return () => clearTimeout(timeoutId)
  }, [query])

  const handleSearch = (searchQuery?: string) => {
    const finalQuery = searchQuery || query
    if (finalQuery.trim()) {
      router.push(`/search?q=${encodeURIComponent(finalQuery.trim())}`)
      setShowSuggestions(false)
      inputRef.current?.blur() // Blur input after search
    }
  }

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    handleSearch()
  }

  const handleSuggestionClick = (suggestion: SearchSuggestion) => {
    setQuery(suggestion.text)
    handleSearch(suggestion.text)
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (!showSuggestions || suggestions.length === 0) return

    switch (e.key) {
      case "ArrowDown":
        e.preventDefault()
        setSelectedIndex((prev) => (prev < suggestions.length - 1 ? prev + 1 : prev))
        break
      case "ArrowUp":
        e.preventDefault()
        setSelectedIndex((prev) => (prev > 0 ? prev - 1 : -1))
        break
      case "Enter":
        if (selectedIndex >= 0 && selectedIndex < suggestions.length) {
          e.preventDefault()
          handleSuggestionClick(suggestions[selectedIndex])
        } else {
          // Allow default form submission if no suggestion is actively selected
          handleSearch()
        }
        break
      case "Escape":
        setShowSuggestions(false)
        setSelectedIndex(-1)
        break
    }
  }

  // Close suggestions when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        inputRef.current &&
        !inputRef.current.contains(event.target as Node) &&
        suggestionsRef.current &&
        !suggestionsRef.current.contains(event.target as Node)
      ) {
        setShowSuggestions(false)
      }
    }
    document.addEventListener("mousedown", handleClickOutside)
    return () => {
      document.removeEventListener("mousedown", handleClickOutside)
    }
  }, [])

  const getSuggestionIcon = (type: SearchSuggestion["type"]) => {
    switch (type) {
      case "topic":
        return <Hash className="h-4 w-4 text-muted-foreground" />
      case "channel":
        return <User className="h-4 w-4 text-muted-foreground" />
      default:
        return <Search className="h-4 w-4 text-muted-foreground" />
    }
  }

  return (
    <div className={`relative ${className}`}>
      <form onSubmit={handleSubmit} className="flex w-full items-center space-x-2">
        <div className="relative flex-grow">
          <Input
            ref={inputRef}
            type="search"
            placeholder={placeholder}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            onFocus={() => query.length >= 2 && suggestions.length > 0 && setShowSuggestions(true)}
            className="text-base h-12 rounded-lg pr-4 focus-visible:ring-ring" // Use theme-aware ring
            aria-label="Video search field"
            autoComplete="off"
          />

          {showSuggestions && suggestions.length > 0 && (
            <div
              ref={suggestionsRef}
              className="absolute top-full left-0 right-0 mt-1 bg-popover border rounded-lg shadow-lg z-50 max-h-60 overflow-y-auto"
            >
              {suggestions.map((suggestion, index) => (
                <button
                  key={`${suggestion.type}-${suggestion.text}-${index}`}
                  type="button"
                  onClick={() => handleSuggestionClick(suggestion)}
                  className={`w-full px-4 py-3 text-left hover:bg-muted transition-colors flex items-center gap-3 ${
                    index === selectedIndex ? "bg-muted" : ""
                  }`}
                >
                  {getSuggestionIcon(suggestion.type)}
                  <span className="flex-grow text-sm text-popover-foreground">{suggestion.text}</span>
                  {suggestion.count && <span className="text-xs text-muted-foreground">{suggestion.count}</span>}
                </button>
              ))}
            </div>
          )}
        </div>

        <Button
          type="submit"
          size="lg"
          className="h-12 rounded-lg bg-brand text-brand-foreground hover:bg-brand/90 shadow-md" // Added shadow for more emphasis
          aria-label="Search"
        >
          <Search className="h-5 w-5" />
        </Button>
      </form>
    </div>
  )
}
