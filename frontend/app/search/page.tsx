"use client" // Required for useSearchParams and client-side data fetching hooks

import { useEffect, useState, Suspense } from "react"
import { useSearchParams } from "next/navigation"
import { SearchBarWithSuggestions } from "@/components/search-bar-with-suggestions"
import { VideoCard } from "@/components/video-card"
import { TaxonomySidebar } from "@/components/taxonomy-sidebar"
import { fetchVideosBySearch, fetchVideosByTopic, fetchTaxonomy } from "@/lib/data"
import type { Video, Topic } from "@/lib/types"
import { Skeleton } from "@/components/ui/skeleton"
import { AlertTriangle, SearchX } from "lucide-react"
import { SearchFilters as SearchFiltersType } from "@/lib/types"
import { SearchFilters } from "@/components/search-filters"
import { Pagination, PaginationContent, PaginationItem, PaginationPrevious, PaginationNext, PaginationLink, PaginationEllipsis } from "@/components/ui/pagination"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

function SearchResultsContent() {
  const searchParams = useSearchParams()
  const query = searchParams.get("q")
  const topicId = searchParams.get("topic")

  const [videos, setVideos] = useState<Video[]>([])
  const [taxonomy, setTaxonomy] = useState<Topic[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [filters, setFilters] = useState<SearchFiltersType>({})
  
  // Pagination state
  const [page, setPage] = useState(1)
  const [videosPerPage, setVideosPerPage] = useState(12)
  const [totalVideos, setTotalVideos] = useState(0)

  const totalPages = Math.ceil(totalVideos / videosPerPage)

  useEffect(() => {
    // Reset page to 1 when query, topic, or filters change
    setPage(1)
  }, [query, topicId, filters])

  useEffect(() => {
    async function loadData() {
      setIsLoading(true)
      setError(null)
      try {
        const taxPromise = fetchTaxonomy()
        let videosPromise

        if (query) {
          videosPromise = fetchVideosBySearch(query, filters, page, videosPerPage)
        } else if (topicId) {
          videosPromise = fetchVideosByTopic(topicId, page, videosPerPage)
        } else {
          // Default search when no query or topic is provided
          videosPromise = fetchVideosBySearch("", filters, page, videosPerPage)
        }

        const [taxData, videosResponse] = await Promise.all([taxPromise, videosPromise])
        
        setTaxonomy(taxData)
        setVideos(videosResponse.videos)
        setTotalVideos(videosResponse.total)

      } catch (err) {
        setError("Unable to load data. Please try again later.")
      } finally {
        setIsLoading(false)
      }
    }
    loadData()
  }, [query, topicId, filters, page, videosPerPage])

  const handlePageChange = (newPage: number) => {
    if (newPage > 0 && newPage <= totalPages) {
      setPage(newPage)
      window.scrollTo(0, 0) // Scroll to top on page change
    }
  }

  const renderPagination = () => {
    if (totalPages <= 1) return null

    const pageNumbers = []
    const displayPages = 5 // Number of page links to show
    
    let startPage = Math.max(1, page - Math.floor(displayPages / 2))
    let endPage = Math.min(totalPages, startPage + displayPages - 1)

    if (endPage - startPage + 1 < displayPages) {
      startPage = Math.max(1, endPage - displayPages + 1)
    }

    for (let i = startPage; i <= endPage; i++) {
      pageNumbers.push(i)
    }

    return (
      <Pagination>
        <PaginationContent>
          <PaginationItem>
            <PaginationPrevious onClick={() => handlePageChange(page - 1)} className={page <= 1 ? "pointer-events-none opacity-50" : ""} />
          </PaginationItem>
          {startPage > 1 && (
            <>
              <PaginationItem>
                <PaginationLink onClick={() => handlePageChange(1)}>1</PaginationLink>
              </PaginationItem>
              {startPage > 2 && <PaginationEllipsis />}
            </>
          )}
          {pageNumbers.map(num => (
            <PaginationItem key={num}>
              <PaginationLink isActive={num === page} onClick={() => handlePageChange(num)}>
                {num}
              </PaginationLink>
            </PaginationItem>
          ))}
          {endPage < totalPages && (
            <>
              {endPage < totalPages - 1 && <PaginationEllipsis />}
              <PaginationItem>
                <PaginationLink onClick={() => handlePageChange(totalPages)}>{totalPages}</PaginationLink>
              </PaginationItem>
            </>
          )}
          <PaginationItem>
            <PaginationNext onClick={() => handlePageChange(page + 1)} className={page >= totalPages ? "pointer-events-none opacity-50" : ""} />
          </PaginationItem>
        </PaginationContent>
      </Pagination>
    )
  }

  const pageTitle = query
    ? `Results for "${query}"`
    : topicId
      ? `Videos about "${taxonomy.find((t) => t.id === topicId)?.name || taxonomy.flatMap((t) => t.children || []).find((c) => c.id === topicId)?.name || topicId}"`
      : "Explore Our Videos"

  return (
    <div className="flex flex-col md:flex-row gap-8">
      <TaxonomySidebar taxonomy={taxonomy} currentTopicId={topicId || undefined} />
      <div className="flex-1">
        <div className="mb-6">
          <SearchBarWithSuggestions initialQuery={query || ""} />
        </div>

        <SearchFilters filters={filters} onFiltersChange={setFilters} className="mb-6" />

        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold text-foreground">{pageTitle}</h1>
          {!isLoading && !error && totalVideos > 0 && (
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <span>{totalVideos} video{totalVideos !== 1 ? "s" : ""} found</span>
              <Select value={videosPerPage.toString()} onValueChange={(value) => setVideosPerPage(Number(value))}>
                <SelectTrigger className="w-[120px] h-8 text-xs">
                  <SelectValue placeholder="Results per page" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="12">12 per page</SelectItem>
                  <SelectItem value="24">24 per page</SelectItem>
                  <SelectItem value="36">36 per page</SelectItem>
                </SelectContent>
              </Select>
            </div>
          )}
        </div>

        {/* Rest of the component remains the same */}
        {isLoading && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="space-y-3">
                <Skeleton className="h-[180px] w-full rounded-xl" />
                <Skeleton className="h-4 w-[250px]" />
                <Skeleton className="h-4 w-[200px]" />
              </div>
            ))}
          </div>
        )}

        {!isLoading && error && (
          <div className="flex flex-col items-center justify-center text-center py-10 bg-muted rounded-lg">
            <AlertTriangle className="w-16 h-16 text-destructive mb-4" />
            <p className="text-xl font-semibold text-destructive">An error occurred</p>
            <p className="text-muted-foreground">{error}</p>
          </div>
        )}

        {!isLoading && !error && videos.length === 0 && (
          <div className="flex flex-col items-center justify-center text-center py-10 bg-muted rounded-lg">
            <SearchX className="w-16 h-16 text-muted-foreground mb-4" />
            <p className="text-xl font-semibold text-foreground">No videos found</p>
            <p className="text-muted-foreground">Try searching for different terms or explore different topics.</p>
          </div>
        )}

        {!isLoading && !error && videos.length > 0 && (
          <div className="flex flex-col gap-y-8">
            <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-x-6 gap-y-8">
              {videos.map((video) => (
                <VideoCard key={video.id} video={video} showRelevance={!!query} />
              ))}
            </div>
            {renderPagination()}
          </div>
        )}
      </div>
    </div>
  )
}

export default function SearchPage() {
  // Suspense is used because useSearchParams() needs to be read by a Client Component.
  // The SearchResultsContent component handles its own data fetching and state.
  return (
    <Suspense fallback={<div>Carregando...</div>}>
      <SearchResultsContent />
    </Suspense>
  )
}
