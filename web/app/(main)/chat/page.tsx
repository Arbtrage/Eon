'use client'

import { useEffect, useRef, useState } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Bot, Send, User } from 'lucide-react'
import { EmptyState } from '@/components/EmptyState'
import ReactMarkdown from 'react-markdown'
import rehypeRaw from 'rehype-raw'
import rehypeSanitize from 'rehype-sanitize'
import rehypeHighlight from 'rehype-highlight'
import 'highlight.js/styles/github-dark.css'

interface Message {
    id: string
    content: string
    sender: 'user' | 'bot' | 'system'
    timestamp: Date
}

export default function ChatPage() {
    const [messages, setMessages] = useState<Message[]>([])
    const [input, setInput] = useState('')
    const scrollAreaRef = useRef<HTMLDivElement>(null)
    const inputRef = useRef<HTMLInputElement>(null)
    const [status, setStatus] = useState<string>('')


    const scrollToBottom = () => {
        if (scrollAreaRef.current) {
            scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight
        }
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages])

    const addMessage = (content: string, sender: 'user' | 'bot') => {
        setMessages(prev => [...prev, {
            id: Date.now().toString(),
            content,
            sender,
            timestamp: new Date()
        }])
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!input.trim()) return

        addMessage(input, 'user')
        const userInput = input
        setInput('')

        try {
            const data = {
                input: userInput,
                chat_id: "12322"
            }
            const response = await fetch('http://localhost:5010/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            })

            const reader = response.body?.getReader()
            if (!reader) return

            let assistantMessage = ''

            while (true) {
                const { done, value } = await reader.read()
                if (done) break

                const chunk = new TextDecoder().decode(value)
                const lines = chunk.split('\n')

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = JSON.parse(line.slice(5))

                        if (data.type === 'system') {
                            setStatus(data.text)
                        } else if (data.type === 'error') {
                            console.error(data.text)
                            setStatus(`Error: ${data.text}`)
                        } else {
                            assistantMessage += data.text
                            setMessages(prev => {
                                const lastMessage = prev[prev.length - 1]
                                if (lastMessage?.sender === 'bot') {
                                    return prev.map(msg =>
                                        msg.id === lastMessage.id
                                            ? { ...msg, content: assistantMessage }
                                            : msg
                                    )
                                } else {
                                    return [...prev, {
                                        id: Date.now().toString(),
                                        content: assistantMessage,
                                        sender: 'bot',
                                        timestamp: new Date()
                                    }]
                                }
                            })
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Error:', error)
            setStatus('Error occurred while processing the request')
        } finally {
            setStatus('')
        }
    }

    const handleExampleClick = (example: string) => {
        addMessage(example, 'user')
    }

    return (
        <div className='h-full flex-1 '>
            <div className="flex flex-col h-[calc(100vh-4rem)] rounded-xl">
                {status && (
                    <div className="px-6 py-2 bg-slate-100 dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700">
                        <p className="text-sm text-slate-600 dark:text-slate-400 text-center italic">
                            {status}
                        </p>
                    </div>
                )}

                <ScrollArea className="flex-1 relative" ref={scrollAreaRef}>
                    {messages.length === 0 ? (
                        <EmptyState onExampleClick={handleExampleClick} />
                    ) : (
                        <div className="p-6 space-y-6 max-w-4xl mx-auto">
                            {messages.map((message, index) => (
                                <div
                                    key={message.id}
                                    className={`flex items-end gap-3 ${message.sender === 'user' ? 'flex-row-reverse' : ''}`}
                                >
                                    <Avatar className="h-8 w-8 border border-slate-200 dark:border-slate-700">
                                        {message.sender === 'bot' ? (
                                            <>
                                                <AvatarImage src="/bot-avatar.png" alt="Bot Avatar" />
                                                <AvatarFallback className="bg-slate-100 dark:bg-slate-800">
                                                    <Bot className="h-5 w-5 text-slate-600 dark:text-slate-400" />
                                                </AvatarFallback>
                                            </>
                                        ) : (
                                            <>
                                                <AvatarImage src="/user-avatar.png" alt="User Avatar" />
                                                <AvatarFallback className="bg-slate-100 dark:bg-slate-800">
                                                    <User className="h-5 w-5 text-slate-600 dark:text-slate-400" />
                                                </AvatarFallback>
                                            </>
                                        )}
                                    </Avatar>
                                    <div
                                        className={`rounded-lg px-4 py-2 max-w-[80%] ${index === messages.length - 1 ? 'animate-fadeIn' : ''}`}
                                    >
                                        <div className="prose dark:prose-invert max-w-none">
                                            <ReactMarkdown
                                                rehypePlugins={[rehypeRaw, rehypeSanitize, rehypeHighlight]}
                                                className="text-sm leading-relaxed"
                                            >
                                                {message.content}
                                            </ReactMarkdown>
                                        </div>
                                        <time className="text-[10px] mt-1 block text-slate-500 dark:text-slate-400">
                                            {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                        </time>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </ScrollArea>

                <div className=" p-6 sticky bottom-0">
                    <form onSubmit={handleSubmit} className="flex gap-3 max-w-4xl mx-auto">
                        <Input
                            ref={inputRef}
                            type="text"
                            placeholder="Type your message..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            className="flex-1 rounded-full bg-slate-100 dark:bg-slate-700 border-0 focus-visible:ring-2 focus-visible:ring-blue-500 dark:focus-visible:ring-blue-400"
                        />
                        <Button
                            type="submit"
                            size="icon"
                            className="rounded-full bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 transition-all duration-300 shadow-md hover:shadow-lg"
                        >
                            <Send className="h-4 w-4 text-white" />
                            <span className="sr-only">Send message</span>
                        </Button>
                    </form>
                </div>
            </div>
        </div>

    )
}

