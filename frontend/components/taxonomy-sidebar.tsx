"use client"

import type { Topic } from "@/lib/types"
import Link from "next/link"
import { useSearchParams } from "next/navigation"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { ChevronRight } from "lucide-react"

interface TaxonomySidebarProps {
  taxonomy: Topic[]
  currentTopicId?: string
}

interface TopicNodeProps {
  topic: Topic
  level: number
  currentTopicId?: string
  currentSearchQuery?: string | null
}

function TopicNode({ topic, level, currentTopicId, currentSearchQuery }: TopicNodeProps) {
  const isActive = topic.id === currentTopicId && !currentSearchQuery
  const linkHref = `/search?topic=${topic.id}`

  if (!topic.children || topic.children.length === 0) {
    return (
      <Link
        href={linkHref}
        className={`block py-2 px-3 rounded-md text-sm hover:bg-muted transition-colors ${isActive ? "bg-primary/10 text-primary font-semibold" : "text-muted-foreground hover:text-foreground"}`}
        style={{ paddingLeft: `${1 + level * 0.75}rem` }}
      >
        <div className="flex items-center justify-between">
          <span>{topic.name}</span>
          {topic.videoCount !== undefined && (
            <span className="text-xs bg-muted px-1.5 py-0.5 rounded-full">{topic.videoCount}</span>
          )}
        </div>
      </Link>
    )
  }

  return (
    <AccordionItem value={topic.id} className="border-none">
      <AccordionTrigger
        className={`py-2 px-3 rounded-md text-sm hover:bg-muted transition-colors justify-start hover:no-underline ${isActive ? "bg-primary/10 text-primary font-semibold" : "text-muted-foreground hover:text-foreground"}`}
        style={{ paddingLeft: `${1 + level * 0.75}rem` }}
      >
        <ChevronRight className="h-4 w-4 mr-1 shrink-0 transition-transform duration-200 group-[&[data-state=open]]:rotate-90" />
        <Link href={linkHref} onClick={(e) => e.stopPropagation()} className="flex-1 text-left">
          <div className="flex items-center justify-between">
            <span>{topic.name}</span>
            {topic.videoCount !== undefined && (
              <span className="text-xs bg-muted px-1.5 py-0.5 rounded-full">{topic.videoCount}</span>
            )}
          </div>
        </Link>
      </AccordionTrigger>
      <AccordionContent className="pb-0">
        {topic.children?.map((child) => (
          <TopicNode
            key={child.id}
            topic={child}
            level={level + 1}
            currentTopicId={currentTopicId}
            currentSearchQuery={currentSearchQuery}
          />
        ))}
      </AccordionContent>
    </AccordionItem>
  )
}

export function TaxonomySidebar({ taxonomy, currentTopicId }: TaxonomySidebarProps) {
  const searchParams = useSearchParams()
  const currentSearchQuery = searchParams.get("q")

  return (
    <aside className="w-full md:w-72 lg:w-80 md:sticky md:top-20 md:max-h-[calc(100vh-6rem)] md:overflow-y-auto pr-4">
      <h2 className="text-xl font-semibold mb-4 text-foreground">Explore Topics</h2>
      <Accordion type="multiple" className="w-full space-y-1">
        {taxonomy.map((topic) => (
          <TopicNode
            key={topic.id}
            topic={topic}
            level={0}
            currentTopicId={currentTopicId}
            currentSearchQuery={currentSearchQuery}
          />
        ))}
      </Accordion>
    </aside>
  )
}
