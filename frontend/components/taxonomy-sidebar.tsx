"use client"

import { useState } from "react"
import Link from "next/link"
import { ChevronRight, ChevronDown } from "lucide-react"
import { Topic } from "@/lib/types"

interface TaxonomySidebarProps {
  taxonomy: Topic[]
}

const TopicItem = ({ topic, level }: { topic: Topic; level: number }) => {
  const [isOpen, setIsOpen] = useState(level < 1) // Open top-level by default

  const hasChildren = topic.children && topic.children.length > 0

  return (
    <div style={{ paddingLeft: `${level * 1}rem` }}>
      <div
        className="flex items-center justify-between py-2 px-3 rounded-md hover:bg-muted cursor-pointer"
        onClick={() => hasChildren && setIsOpen(!isOpen)}
      >
        <Link href={`/search?topic=${encodeURIComponent(topic.id)}`}>
          <a className="flex-grow capitalize text-sm font-medium text-foreground hover:text-brand">
            {topic.name}
          </a>
        </Link>
        {hasChildren && (
          <div className="ml-2">
            {isOpen ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
          </div>
        )}
      </div>
      {isOpen && hasChildren && (
        <div className="mt-1">
          {topic.children.map(child => (
            <TopicItem key={child.id} topic={child} level={level + 1} />
          ))}
        </div>
      )}
    </div>
  )
}

export const TaxonomySidebar = ({ taxonomy }: TaxonomySidebarProps) => {
  if (!taxonomy || taxonomy.length === 0) {
    return (
      <div className="p-4 text-muted-foreground">No topics available.</div>
    )
  }

  return (
    <nav className="space-y-1 h-full overflow-y-auto">
      <h3 className="text-lg font-semibold px-4 py-2 text-foreground">
        Explore Topics
      </h3>
      {taxonomy.map(topic => (
        <TopicItem key={topic.id} topic={topic} level={0} />
      ))}
    </nav>
  )
}
