'use client'

import { motion } from 'framer-motion'
import { Brain, Sparkles, Terminal, ArrowRight } from 'lucide-react'
import { Button } from "@/components/ui/button"


export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 text-white">
      {/* Navigation */}
      <nav className="fixed w-full top-0 z-50 bg-slate-950/50 backdrop-blur-md border-b border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
              className="flex items-center"
            >
              <span className="flex items-center gap-2">
                <span className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-violet-400">
                  Eon
                </span>
                <span className="text-sm font-normal text-slate-400">
                  Intelligent Knowledge Retrieval
                </span>
              </span>
            </motion.div>
            <div className="flex items-center space-x-4">
              <Button variant="ghost" className="text-slate-300 hover:text-white">
                Documentation
              </Button>
              <Button className="bg-gradient-to-r from-blue-500 to-violet-500 hover:from-blue-600 hover:to-violet-600 text-white">
                <a href="/auth">Get Started</a>
              </Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="pt-32 pb-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          {/* Mobile Banner */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="mb-12 flex justify-center"
          >
            <div className="inline-flex items-center space-x-2 bg-slate-800/50 backdrop-blur-sm px-4 py-2 rounded-full border border-slate-700">
              <Sparkles className="w-4 h-4 text-blue-400" />
              <span className="text-sm text-slate-300">New: AI-powered document analysis available now</span>
              <ArrowRight className="w-4 h-4 text-slate-400" />
            </div>
          </motion.div>

          {/* Hero Section */}
          <div className="text-center mb-16">
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.2 }}
              className="text-4xl sm:text-6xl lg:text-7xl font-bold tracking-tight"
            >
              <span className="text-slate-400">The</span>{" "}
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-violet-400 to-purple-400">
                intelligent agent
              </span>{" "}
              <span className="text-slate-400">for</span>{" "}
              <br className="hidden sm:block" />
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-violet-400">
                knowledge retrieval
              </span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.4 }}
              className="mt-6 text-lg sm:text-xl text-slate-400 max-w-3xl mx-auto"
            >
              Transform your data into actionable insights with our advanced RAG system.
              Powered by cutting-edge AI to deliver precise and contextual information retrieval.
            </motion.p>
          </div>

          {/* Feature Preview */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.6 }}
            className="relative"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-violet-500/10 rounded-2xl blur-3xl" />
            <div className="relative bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-8 overflow-hidden">
              <div className="grid md:grid-cols-3 gap-8">
                <FeatureCard
                  icon={Brain}
                  title="Intelligent Processing"
                  description="Advanced AI algorithms understand and process your queries with human-like comprehension"
                />
                <FeatureCard
                  icon={Terminal}
                  title="Precise Retrieval"
                  description="Get exactly what you need with our context-aware search system"
                />
                <FeatureCard
                  icon={Sparkles}
                  title="Smart Analysis"
                  description="Automated insights and patterns discovery from your knowledge base"
                />
              </div>
            </div>
          </motion.div>
        </div>
      </main>
    </div>
  )
}

function FeatureCard({ icon: Icon, title, description }: { icon: any, title: string, description: string }) {
  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      className="relative group"
    >
      <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-violet-500/10 rounded-xl blur-xl transition-all duration-300 group-hover:blur-2xl" />
      <div className="relative bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl p-6 transition-all duration-300">
        <div className="mb-4 inline-block bg-gradient-to-r from-blue-500/20 to-violet-500/20 rounded-lg p-3">
          <Icon className="w-6 h-6 text-blue-400" />
        </div>
        <h3 className="text-lg font-semibold text-white mb-2">{title}</h3>
        <p className="text-slate-400 text-sm">{description}</p>
      </div>
    </motion.div>
  )
}

