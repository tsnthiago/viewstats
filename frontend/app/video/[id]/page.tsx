"use client" // For useState, useEffect, useRef

import { useEffect, useState, useRef, Suspense } from "react"
import { useParams, useSearchParams } from "next/navigation"
import { fetchVideoById } from "@/lib/data"
import type { Video as VideoType } from "@/lib/types"
import { VideoPlayer } from "@/components/video-player"
import { InteractiveTranscript } from "@/components/interactive-transcript"
import { Badge } from "@/components/ui/badge"
import { Skeleton } from "@/components/ui/skeleton"
import { AlertTriangle, Film } from "lucide-react"
import Link from "next/link"
import { Button } from "@/components/ui/button"

function VideoPageContent() {
  const params = useParams()
  const searchParams = useSearchParams()
  const videoId = params.id as string
  const searchTerm = searchParams.get("q") // Get search term if navigated from search

  const [video, setVideo] = useState<VideoType | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [currentTime, setCurrentTime] = useState(0)

  const playerRef = useRef<HTMLVideoElement>(null)

  useEffect(() => {
    if (!videoId) return
    async function loadVideo() {
      setIsLoading(true)
      setError(null)
      try {
        const videoData = await fetchVideoById(videoId)
        if (videoData) {
          setVideo(videoData)
        } else {
          setError("Video not found.")
        }
      } catch (err) {
        console.error("Failed to load video:", err)
        setError("Unable to load video. Please try again later.")
      } finally {
        setIsLoading(false)
      }
    }
    loadVideo()
  }, [videoId])

  const handleTimeUpdate = (time: number) => {
    setCurrentTime(time)
  }

  const handleTranscriptClick = (time: number) => {
    if (playerRef.current) {
      playerRef.current.currentTime = time
      playerRef.current.play()
    }
  }

  if (isLoading) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-8">
        <Skeleton className="w-full aspect-video rounded-xl mb-6" />
        <div className="grid md:grid-cols-3 gap-8">
          <div className="md:col-span-2 space-y-4">
            <Skeleton className="h-8 w-3/4" />
            <Skeleton className="h-4 w-1/2" />
            <Skeleton className="h-20 w-full" />
          </div>
          <div className="space-y-3">
            <Skeleton className="h-6 w-1/3 mb-2" />
            <Skeleton className="h-40 w-full" />
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center text-center py-10 max-w-2xl mx-auto">
        <AlertTriangle className="w-16 h-16 text-destructive mb-4" />
        <p className="text-xl font-semibold text-destructive">An error occurred</p>
        <p className="text-muted-foreground mb-6">{error}</p>
        <Button asChild>
          <Link href="/">Back to homepage</Link>
        </Button>
      </div>
    )
  }

  if (!video) {
    return (
      // Should be covered by error state, but as a fallback
      <div className="flex flex-col items-center justify-center text-center py-10 max-w-2xl mx-auto">
        <Film className="w-16 h-16 text-muted-foreground mb-4" />
        <p className="text-xl font-semibold">Video not found</p>
        <Button asChild className="mt-4">
          <Link href="/">Back to homepage</Link>
        </Button>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto px-0 sm:px-4 py-2 sm:py-8">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-x-8 gap-y-6">
        <div className="md:col-span-2">
          <VideoPlayer src={video.videoUrl} onTimeUpdate={handleTimeUpdate} playerRef={playerRef} />
          <div className="mt-6">
            <h1 className="text-3xl font-bold mb-2 text-foreground">{video.title}</h1>
            <div className="flex flex-wrap gap-2 mb-4">
              {video.topics.map((topic) => (
                <Badge key={topic} variant="secondary" className="capitalize bg-muted hover:bg-muted/80">
                  {topic.replace("-", " ")}
                </Badge>
              ))}
            </div>
            <p className="text-muted-foreground leading-relaxed">{video.description}</p>
          </div>
        </div>
        <div className="md:col-span-1">
          <InteractiveTranscript
            transcript={video.transcript}
            currentTime={currentTime}
            onTranscriptClick={handleTranscriptClick}
            searchTerm={searchTerm}
          />
        </div>
      </div>
    </div>
  )
}

export default function VideoPage() {
  return (
    <Suspense fallback={<div>Loading video...</div>}>
      <VideoPageContent />
    </Suspense>
  )
}
