// Add channel information and enhance video metadata
export interface Channel {
  id: string
  handle: string
  name: string
  subscribers: number
  category: string
  topics: string[]
  description?: string
  avatarUrl?: string
}

export interface Video {
  id: string
  title: string
  thumbnailUrl: string
  duration: string // e.g., "12:35"
  semanticSnippet?: string // Highlighted text snippet
  topics: string[] // Topic IDs or names
  transcript: TranscriptItem[]
  description: string
  videoUrl: string // URL for the video player
  // Add missing metadata from requirements
  uploadDate: string
  viewCount: number
  language: string
  tags: string[]
  channel: Channel
  relevanceScore?: number // For search ranking
}

export interface TranscriptItem {
  id: string
  startTime: number // in seconds
  endTime: number // in seconds
  text: string
}

export interface Topic {
  id: string
  name: string
  children?: Topic[]
  videoCount?: number // Show how many videos are in each topic
}

export interface SearchSuggestion {
  text: string
  type: "topic" | "channel" | "keyword"
  count?: number
}

export interface SearchFilters {
  duration?: "short" | "medium" | "long" // <4min, 4-20min, >20min
  uploadDate?: "day" | "week" | "month" | "year"
  language?: string
  minViews?: number
  topics?: string[]
}
