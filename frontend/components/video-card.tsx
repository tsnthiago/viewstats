"use client"

import type React from "react"
import { useEffect, useState } from "react"

import Link from "next/link"
import Image from "next/image"
import type { Video } from "@/lib/types"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Clock, Eye, Calendar } from "lucide-react"
import { useRouter } from "next/navigation"

interface VideoCardProps {
  video: Video
  showRelevance?: boolean
}

const formatViewCount = (count: number): string => {
  if (count >= 1000000) return `${(count / 1000000).toFixed(1)}M`
  if (count >= 1000) return `${(count / 1000).toFixed(1)}K`
  return count.toString()
}

const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now.getTime() - date.getTime())
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 1) return "1 day ago"
  if (diffDays < 7) return `${diffDays} days ago`
  if (diffDays < 30) return `${Math.ceil(diffDays / 7)} weeks ago`
  if (diffDays < 365) return `${Math.ceil(diffDays / 30)} months ago`
  return `${Math.ceil(diffDays / 365)} years ago`
}

// Função utilitária para obter a thumb do YouTube
function getYoutubeThumbUrl(id: string) {
  return `https://img.youtube.com/vi/${id}/hqdefault.jpg`
}

export function VideoCard({ video, showRelevance = false }: VideoCardProps) {
  const router = useRouter()

  const handleChannelClick = (e: React.MouseEvent) => {
    e.preventDefault()
    e.stopPropagation()
    router.push(`/channel/${video.channel.id}`)
  }

  return (
    <Link href={`/video/${video.id}`} className="block group">
      <Card className="overflow-hidden h-full flex flex-col rounded-xl shadow-md hover:shadow-xl transition-shadow duration-300 ease-in-out bg-card">
        <CardHeader className="p-0 relative">
          <Image
            src={getYoutubeThumbUrl(video.id)}
            alt={video.title ? `Thumbnail for ${video.title}` : 'Video thumbnail'}
            width={400}
            height={225}
            className="aspect-video object-cover w-full group-hover:scale-105 transition-transform duration-300"
          />
          {video.duration && (
            <div className="absolute bottom-2 right-2 bg-black/70 text-white px-2 py-1 text-xs rounded flex items-center">
              <Clock size={14} className="mr-1" />
              {video.duration}
            </div>
          )}
          {showRelevance && video.relevanceScore && (
            <div className="absolute top-2 left-2 bg-primary text-primary-foreground px-2 py-1 text-xs rounded">
              {Math.round(video.relevanceScore * 100)}% match
            </div>
          )}
        </CardHeader>
        <CardContent className="p-4 flex-grow">
          {video.title && (
            <CardTitle className="text-lg font-semibold mb-2 leading-tight group-hover:text-primary transition-colors line-clamp-2">
              {video.title}
            </CardTitle>
          )}

          {/* Channel Info */}
          {video.channel && video.channel.name && (
            <div className="flex items-center gap-2 mb-2">
              {video.channel.avatarUrl && (
                <Image
                  src={video.channel.avatarUrl}
                  alt={video.channel.name}
                  width={20}
                  height={20}
                  className="rounded-full"
                />
              )}
              <button
                onClick={handleChannelClick}
                className="text-sm text-muted-foreground hover:text-primary transition-colors text-left"
              >
                {video.channel.name}
              </button>
            </div>
          )}

          {/* Video Metadata */}
          {(video.viewCount !== undefined || video.uploadDate) && (
            <div className="flex items-center gap-4 text-xs text-muted-foreground mb-2">
              {video.viewCount !== undefined && (
                <div className="flex items-center gap-1">
                  <Eye size={12} />
                  {formatViewCount(video.viewCount)} views
                </div>
              )}
              {video.uploadDate && (
                <div className="flex items-center gap-1">
                  <Calendar size={12} />
                  {formatDate(video.uploadDate)}
                </div>
              )}
            </div>
          )}

          {video.semanticSnippet && (
            <p
              className="text-sm text-muted-foreground line-clamp-2 mb-2"
              dangerouslySetInnerHTML={{ __html: video.semanticSnippet }}
            />
          )}
          {!video.semanticSnippet && video.description && (
            <p className="text-sm text-muted-foreground line-clamp-2 mb-2">{video.description}</p>
          )}
        </CardContent>
        <CardFooter className="p-4 pt-0">
          <div className="flex flex-wrap gap-2">
            {(video.topics || []).slice(0, 3).map((topic) => (
              <Badge key={topic} variant="secondary" className="text-xs capitalize">
                {topic.replace("-", " ")}
              </Badge>
            ))}
          </div>
        </CardFooter>
      </Card>
    </Link>
  )
}
