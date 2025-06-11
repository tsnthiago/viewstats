"use client"

import type React from "react"

import { useEffect, useRef } from "react"

interface VideoPlayerProps {
  src: string
  onTimeUpdate?: (time: number) => void
  onLoadedMetadata?: (duration: number) => void
  playerRef?: React.RefObject<HTMLVideoElement> // Allow parent to control player
}

export function VideoPlayer({ src, onTimeUpdate, onLoadedMetadata, playerRef: externalPlayerRef }: VideoPlayerProps) {
  const internalPlayerRef = useRef<HTMLVideoElement>(null)
  const playerRef = externalPlayerRef || internalPlayerRef

  useEffect(() => {
    const videoElement = playerRef.current
    if (!videoElement) return

    const handleTimeUpdate = () => {
      if (onTimeUpdate) {
        onTimeUpdate(videoElement.currentTime)
      }
    }

    const handleLoadedMetadata = () => {
      if (onLoadedMetadata) {
        onLoadedMetadata(videoElement.duration)
      }
    }

    videoElement.addEventListener("timeupdate", handleTimeUpdate)
    videoElement.addEventListener("loadedmetadata", handleLoadedMetadata)

    return () => {
      videoElement.removeEventListener("timeupdate", handleTimeUpdate)
      videoElement.removeEventListener("loadedmetadata", handleLoadedMetadata)
    }
  }, [src, onTimeUpdate, onLoadedMetadata, playerRef])

  return (
    <div className="aspect-video w-full bg-black rounded-xl overflow-hidden shadow-2xl">
      <video ref={playerRef} src={src} controls className="w-full h-full" preload="metadata">
        Your browser does not support the video element.
      </video>
    </div>
  )
}
