"use client"

import { SearchBarWithSuggestions } from "@/components/search-bar-with-suggestions"
import { FeaturedTopics } from "@/components/featured-topics"
import { ValueProposition } from "@/components/value-proposition"
import Link from "next/link"
import { useEffect, useState } from "react"
import { TaxonomySidebar } from "@/components/taxonomy-sidebar"
import { fetchTaxonomy } from "@/lib/data"
import type { Topic } from "@/lib/types"

export default function HomePage() {
  const [taxonomy, setTaxonomy] = useState<Topic[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadTaxonomy() {
      setIsLoading(true)
      setError(null)
      try {
        const data = await fetchTaxonomy()
        setTaxonomy(data)
      } catch (err) {
        setError("Unable to load taxonomy.")
      } finally {
        setIsLoading(false)
      }
    }
    loadTaxonomy()
  }, [])

  return (
    <div className="flex flex-row gap-8">
      <div className="hidden md:block w-72 lg:w-80 flex-shrink-0">
        {isLoading ? (
          <div className="p-4">Loading topics...</div>
        ) : error ? (
          <div className="p-4 text-destructive">{error}</div>
        ) : (
          <TaxonomySidebar taxonomy={taxonomy} />
        )}
      </div>
      <div className="flex-1 flex flex-col">
        <section className="w-full pt-16 sm:pt-20 md:pt-32 lg:pt-40 pb-10 md:pb-16 lg:pb-20">
          <div className="container px-4 md:px-6 text-center">
            <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold tracking-tighter mb-4 sm:mb-6 text-foreground">
              Find Knowledge in Video
            </h1>
            <p className="text-base sm:text-lg text-muted-foreground mb-8 sm:mb-10 max-w-3xl mx-auto">
              Explore a universe of videos through intelligent semantic search or
              browse organized topics. Unlock a world of learning with a powerful
              search engine at your fingertips.
            </p>
            <div className="w-full max-w-2xl mx-auto mb-6">
              <SearchBarWithSuggestions placeholder="Type what you want to learn..." />
            </div>
            <p className="text-muted-foreground">
              Or{" "}
              <Link
                href="/search"
                className="font-medium text-brand hover:underline"
              >
                explore our topic collections
              </Link>
            </p>
          </div>
        </section>
        <ValueProposition />
        <FeaturedTopics />
      </div>
    </div>
  )
}
