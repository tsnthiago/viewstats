import {
  Code,
  Atom,
  Music,
  BookOpen,
  Palette,
  Calculator,
} from "lucide-react"
import Link from "next/link"

const topics = [
  {
    name: "Programming",
    icon: Code,
    href: "/search?q=programming",
  },
  {
    name: "Science",
    icon: Atom,
    href: "/search?q=science",
  },
  {
    name: "Music Theory",
    icon: Music,
    href: "/search?q=music+theory",
  },
  {
    name: "Literature",
    icon: BookOpen,
    href: "/search?q=literature",
  },
  {
    name: "Art History",
    icon: Palette,
    href: "/search?q=art+history",
  },
  {
    name: "Mathematics",
    icon: Calculator,
    href: "/search?q=mathematics",
  },
]

export function FeaturedTopics() {
  return (
    <section className="w-full py-12 md:py-20 lg:py-24 bg-muted/40">
      <div className="container px-4 md:px-6">
        <div className="flex flex-col items-center justify-center space-y-4 text-center">
          <div className="space-y-2">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">
              Explore Popular Topics
            </h2>
            <p className="max-w-[900px] text-muted-foreground text-base sm:text-lg md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
              Dive into curated topics and expand your knowledge.
            </p>
          </div>
        </div>
        <div className="mx-auto grid grid-cols-2 sm:grid-cols-3 md:grid-cols-3 lg:grid-cols-6 gap-4 sm:gap-6 mt-10 sm:mt-12">
          {topics.map((topic) => (
            <Link
              key={topic.name}
              href={topic.href}
              className="group flex flex-col items-center justify-center space-y-2 rounded-lg border bg-card text-card-foreground p-4 sm:p-6 transition-all hover:bg-accent hover:shadow-lg"
            >
              <topic.icon className="h-8 w-8 sm:h-10 sm:w-10 text-brand transition-transform group-hover:scale-110" />
              <span className="text-sm sm:text-base font-semibold text-center">{topic.name}</span>
            </Link>
          ))}
        </div>
      </div>
    </section>
  )
} 