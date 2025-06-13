"use client"

import { useState } from "react"
import Link from "next/link"
import { ChevronRight, ChevronDown } from "lucide-react"
import { Topic } from "@/lib/types"
import { useRouter } from "next/navigation"

interface TaxonomySidebarProps {
  taxonomy: Topic[]
}

const TopicItem = ({ topic, level }: { topic: Topic; level: number }) => {
  const [isOpen, setIsOpen] = useState(level === 0)
  const hasChildren = topic.children && topic.children.length > 0
  const router = useRouter();

  if (level > 2) return null; // Limitar a 3 níveis

  return (
    <div style={{ paddingLeft: `${level * 1}rem` }}>
      <div className="flex items-center justify-between py-2 px-3 rounded-md hover:bg-muted">
        <span
          className="flex-grow lowercase text-sm font-medium text-foreground hover:text-brand cursor-pointer"
          onClick={e => {
            e.preventDefault();
            e.stopPropagation();
            router.push(`/search?q=${encodeURIComponent(topic.name.toLowerCase())}`);
          }}
        >
          {topic.name}
        </span>
        {hasChildren && level < 2 && (
          <div className="ml-2 cursor-pointer" onClick={e => { e.stopPropagation(); setIsOpen(!isOpen); }}>
            {isOpen ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
          </div>
        )}
      </div>
      {isOpen && hasChildren && level < 2 && (
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
