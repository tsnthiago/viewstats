"use client"

import type { TranscriptItem } from "@/lib/types"
import { ScrollArea } from "@/components/ui/scroll-area"

interface InteractiveTranscriptProps {
  transcript: TranscriptItem[]
  currentTime: number // Current time of the video in seconds
  onTranscriptClick: (time: number) => void // Callback to seek video
  searchTerm?: string | null // Optional search term to highlight
}

// Helper to highlight search term
const highlightText = (text: string, term: string | null | undefined) => {
  if (!term || term.trim() === "") return text
  const regex = new RegExp(`(${term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")})`, "gi")
  return text.split(regex).map((part, index) =>
    regex.test(part) ? (
      <strong key={index} className="bg-yellow-300 dark:bg-yellow-500 text-black px-0.5 rounded">
        {part}
      </strong>
    ) : (
      part
    ),
  )
}

export function InteractiveTranscript({
  transcript,
  currentTime,
  onTranscriptClick,
  searchTerm,
}: InteractiveTranscriptProps) {
  return (
    <div className="md:sticky md:top-20">
      <h3 className="text-xl font-semibold mb-3 text-foreground">Interactive Transcript</h3>
      <ScrollArea className="h-[300px] md:h-[calc(100vh-10rem)] w-full rounded-lg border p-1 bg-muted/30">
        <div className="p-3 space-y-3">
          {transcript.map((item) => {
            const isActive = currentTime >= item.startTime && currentTime < item.endTime
            return (
              <button
                key={item.id}
                onClick={() => onTranscriptClick(item.startTime)}
                className={`w-full text-left p-3 rounded-md transition-all duration-150 ease-in-out focus:outline-none focus-visible:ring-2 focus-visible:ring-primary
                ${
                  isActive
                    ? "bg-primary/20 dark:bg-primary/30 scale-[1.01] shadow-md"
                    : "hover:bg-primary/10 dark:hover:bg-primary/20"
                }
              `}
              >
                <p
                  className={`text-sm leading-relaxed ${isActive ? "font-medium text-foreground" : "text-muted-foreground"}`}
                >
                  {highlightText(item.text, searchTerm)}
                </p>
              </button>
            )
          })}
        </div>
      </ScrollArea>
    </div>
  )
}
