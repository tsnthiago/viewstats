// ATENÇÃO: Sempre mapear yt_id para id ao criar objetos Video, pois o backend pode retornar yt_id (YouTube ID) e o componente de thumb depende disso.
// Simulates API calls
import type { Video, Topic, TranscriptItem, Channel, SearchSuggestion, SearchFilters } from "./types"

const baseUrl = "/api";

const mockTranscript: TranscriptItem[] = [
  {
    id: "t1",
    startTime: 0,
    endTime: 5,
    text: "Hello and welcome to our first video about artificial intelligence.",
  },
  {
    id: "t2",
    startTime: 5,
    endTime: 10,
    text: "Today, we'll explore the basic concepts and how it's changing the world.",
  },
  { id: "t3", startTime: 10, endTime: 15, text: "Artificial intelligence, or AI, is a vast and fascinating field." },
  { id: "t4", startTime: 15, endTime: 20, text: "Many industries are already reaping the benefits of AI." },
  { id: "t5", startTime: 20, endTime: 25, text: "For example, in medicine, AI assists in disease diagnosis." },
]

const mockChannels: Channel[] = [
  {
    id: "channel1",
    handle: "@TechExplained",
    name: "Tech Explained",
    subscribers: 1200000,
    category: "Education",
    topics: ["ai", "ml", "tech"],
    description: "Making complex technology simple to understand",
    avatarUrl: "/placeholder.svg?height=40&width=40&text=TE",
  },
  {
    id: "channel2",
    handle: "@WebDevMastery",
    name: "Web Dev Mastery",
    subscribers: 850000,
    category: "Education",
    topics: ["web-dev", "react", "frontend"],
    description: "Master modern web development",
    avatarUrl: "/placeholder.svg?height=40&width=40&text=WD",
  },
  {
    id: "channel3",
    handle: "@DataScienceHub",
    name: "Data Science Hub",
    subscribers: 650000,
    category: "Education",
    topics: ["data-science", "python", "ml"],
    description: "Your gateway to data science",
    avatarUrl: "/placeholder.svg?height=40&width=40&text=DS",
  },
]

const mockVideos: Video[] = [
  {
    id: "video1",
    title: "Introduction to Artificial Intelligence",
    thumbnailUrl: "/placeholder.svg?height=225&width=400&text=AI%20Introduction",
    duration: "10:23",
    topics: ["ai", "ml"],
    description:
      "A comprehensive overview of the fundamentals of Artificial Intelligence and its real-world applications.",
    transcript: mockTranscript,
    videoUrl: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
    uploadDate: "2024-01-15",
    viewCount: 125000,
    language: "English",
    tags: ["AI", "Machine Learning", "Technology", "Education"],
    channel: mockChannels[0],
  },
  {
    id: "video2",
    title: "Modern Web Development with React",
    thumbnailUrl: "/placeholder.svg?height=225&width=400&text=React%20Web%20Development",
    duration: "25:10",
    topics: ["web-dev", "react"],
    description: "Learn best practices for web development using React, hooks, and the modern ecosystem.",
    transcript: [
      { id: "t1", startTime: 0, endTime: 5, text: "Welcome to the Modern Web Development with React course." },
      { id: "t2", startTime: 5, endTime: 10, text: "In this lesson, we'll set up our development environment." },
    ],
    videoUrl: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
    uploadDate: "2024-02-20",
    viewCount: 89000,
    language: "English",
    tags: ["React", "JavaScript", "Web Development", "Frontend"],
    channel: mockChannels[1],
  },
  {
    id: "video3",
    title: "Machine Learning with Python",
    thumbnailUrl: "/placeholder.svg?height=225&width=400&text=Python%20Machine%20Learning",
    duration: "18:45",
    topics: ["ai", "ml", "python"],
    description:
      "A practical guide to getting started with Machine Learning using Python and popular libraries like Scikit-learn.",
    transcript: [
      { id: "t1", startTime: 0, endTime: 5, text: "Machine Learning with Python is an essential skill nowadays." },
    ],
    videoUrl: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
    uploadDate: "2024-01-28",
    viewCount: 156000,
    language: "English",
    tags: ["Python", "Machine Learning", "Data Science", "Programming"],
    channel: mockChannels[2],
  },
]

// Add search suggestions
const mockSuggestions: SearchSuggestion[] = [
  { text: "artificial intelligence", type: "keyword", count: 45 },
  { text: "machine learning", type: "keyword", count: 38 },
  { text: "react hooks", type: "keyword", count: 22 },
  { text: "python programming", type: "keyword", count: 31 },
  { text: "Tech Explained", type: "channel", count: 12 },
  { text: "Web Development", type: "topic", count: 67 },
]

export const fetchSearchSuggestions = async (query: string): Promise<SearchSuggestion[]> => {
  // This function can remain as a mock or be implemented in the backend later
  const mockSuggestions: SearchSuggestion[] = [
    { text: "artificial intelligence", type: "keyword", count: 45 },
    { text: "machine learning", type: "keyword", count: 38 },
    { text: "react hooks", type: "keyword", count: 22 },
    { text: "python programming", type: "keyword", count: 31 },
    { text: "Tech Explained", type: "channel", count: 12 },
    { text: "Web Development", type: "topic", count: 67 },
  ]
  await new Promise((resolve) => setTimeout(resolve, 200))
  if (!query || query.length < 2) return []

  return mockSuggestions.filter((suggestion) => suggestion.text.toLowerCase().includes(query.toLowerCase())).slice(0, 5)
}

export const fetchChannelById = async (id: string): Promise<Channel | undefined> => {
    // This can be implemented in the backend if channel details are available
    return undefined;
}

export const fetchVideosByChannel = async (channelId: string): Promise<Video[]> => {
    // This can be implemented in the backend if needed
    return [];
}

// Update existing functions to include relevance scoring
export const fetchVideosBySearch = async (
  query: string,
  filters?: SearchFilters,
  page: number = 1,
  limit: number = 10
): Promise<{ videos: Video[]; total: number }> => {
  const body = {
    query: query || "",
    topic_filter: filters?.topics?.[0] || null,
    top_k: limit
  }
  const response = await fetch(`/api/search`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  })
  if (!response.ok) {
    throw new Error("Failed to fetch search results")
  }
  const data = await response.json()
  const videos = (data.results || []).map((video: any) => ({
    id: video.yt_id ?? video.id,
    title: video.title,
    uploadDate: video.uploadDate,
    viewCount: video.viewCount,
    duration: video.duration,
    thumbnailUrl: video.thumbnailUrl,
    description: video.description,
    topics: video.topics_path,
    transcript: video.transcript,
    language: video.language,
    tags: video.tags,
    videoUrl: video.videoUrl,
    relevanceScore: video.score,
    channel: video.channel,
  }))
  return { videos, total: data.total || videos.length }
}

// Keep the rest of the functions the same, just update console.log messages to English
export const fetchVideosByTopic = async (
  topicId: string,
  page: number = 1,
  limit: number = 10
): Promise<{ videos: Video[]; total: number }> => {
  // Garantir que o topicId está decodificado corretamente
  const decodedTopicId = decodeURIComponent(topicId);
  const params = new URLSearchParams({ 
    topic_id: decodedTopicId,
    page: page.toString(),
    limit: limit.toString(),
  });
  const response = await fetch(`${baseUrl}/videos_by_topic?${params.toString()}`);
  if (!response.ok) {
      throw new Error('Failed to fetch videos by topic');
  }
  const data = await response.json();
  const videos = data.videos.map((video: any) => ({
      id: video.yt_id,
      title: video.title,
      uploadDate: video.upload_date,
      viewCount: video.view_count,
      duration: video.duration,
      thumbnailUrl: video.thumbnail,
      description: video.description,
      topics: video.topics,
      transcript: video.transcript,
      language: video.language,
      tags: video.tags,
      videoUrl: video.videoUrl,
      channel: video.channel
  }));
  return { videos, total: data.total }
}

export const fetchVideoById = async (id: string): Promise<Video | undefined> => {
  const response = await fetch(`${baseUrl}/video/${id}`)
  if (!response.ok) return undefined
  const video = await response.json()
  return {
    id: video.yt_id ?? video.id,
    title: video.title,
    uploadDate: video.uploadDate,
    viewCount: video.viewCount,
    duration: video.duration,
    thumbnailUrl: video.thumbnailUrl,
    description: video.description,
    topics: video.topics_path,
    transcript: video.transcript,
    language: video.language,
    tags: video.tags,
    videoUrl: video.videoUrl,
    relevanceScore: video.score,
    channel: video.channel,
  }
}

export const fetchTaxonomy = async (): Promise<Topic[]> => {
  const response = await fetch(`/api/taxonomy`);
  if (!response.ok) {
    throw new Error(`Failed to fetch taxonomy: ${response.statusText}`);
  }
  const data = await response.json();

  const transformTaxonomy = (node: any, path: string[] = []): Topic[] => {
    return Object.keys(node).map(key => {
      const currentPath = [...path, key];
      const children = node[key] ? transformTaxonomy(node[key], currentPath) : [];
      return {
        id: currentPath.join(" > "),
        name: key,
        children: children,
        level: currentPath.length -1
      };
    });
  };

  return transformTaxonomy(data);
};
