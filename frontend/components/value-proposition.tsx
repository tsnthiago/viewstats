import { ShieldCheck, BrainCircuit, Library, Video } from "lucide-react"

const features = [
  {
    name: "Comprehensive Content",
    description:
      "Access a vast library of videos covering a wide range of topics, from academic lectures to practical tutorials.",
    icon: Video,
  },
  {
    name: "Intelligent Search",
    description:
      "Our semantic search understands the meaning behind your queries to deliver the most relevant video results.",
    icon: BrainCircuit,
  },
  {
    name: "Curated Topics",
    description:
      "Explore hand-picked collections of videos organized into topics by experts, making learning structured and easy.",
    icon: Library,
  },
  {
    name: "Trustworthy & Verified",
    description:
      "We prioritize quality and accuracy, ensuring the content you find is reliable and from reputable sources.",
    icon: ShieldCheck,
  },
]

export function ValueProposition() {
  return (
    <section className="w-full py-12 md:py-20 lg:py-24 bg-background">
      <div className="container px-4 md:px-6">
        <div className="flex flex-col items-center justify-center space-y-4 text-center">
          <div className="space-y-2">
            <div className="inline-block rounded-lg bg-muted px-3 py-1 text-sm">
              Key Features
            </div>
            <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">
              Why VideoSearch?
            </h2>
            <p className="max-w-[900px] text-muted-foreground text-base sm:text-lg md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
              Discover the advantages that make our platform the ultimate
              destination for video-based knowledge.
            </p>
          </div>
        </div>
        <div className="mx-auto grid max-w-5xl grid-cols-1 items-start gap-8 sm:grid-cols-2 md:gap-12 lg:grid-cols-4 lg:gap-16 mt-10 sm:mt-12">
          {features.map((feature) => (
            <div key={feature.name} className="grid gap-2 sm:gap-4 text-center">
                <div className="flex justify-center items-center mb-2">
                    <feature.icon className="h-8 w-8 sm:h-10 sm:w-10 text-brand" />
                </div>
              <h3 className="text-base sm:text-lg font-bold">{feature.name}</h3>
              <p className="text-xs sm:text-sm text-muted-foreground">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
} 