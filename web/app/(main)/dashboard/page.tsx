'use client'

import { useEffect, useRef, useState } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Bot, Send, User } from 'lucide-react'
import { EmptyState } from '@/components/EmptyState'

interface Message {
    id: string
    content: string
    sender: 'user' | 'bot'
    timestamp: Date
}

export default function ChatPage() {
    const [messages, setMessages] = useState<Message[]>([])
    const [input, setInput] = useState('')
    const scrollAreaRef = useRef<HTMLDivElement>(null)
    const inputRef = useRef<HTMLInputElement>(null)

    const scrollToBottom = () => {
        if (scrollAreaRef.current) {
            scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight
        }
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages])

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        if (!input.trim()) return
        addMessage(input, 'user')
    }

    const addMessage = (content: string, sender: 'user' | 'bot') => {
        const newMessage: Message = {
            id: Date.now().toString(),
            content,
            sender,
            timestamp: new Date()
        }
        setMessages(prev => [...prev, newMessage])
        setInput('')
        inputRef.current?.focus()

        if (sender === 'user') {
            setTimeout(() => {
                addMessage("Thank you for your message. I'm processing your request and will respond shortly.", 'bot')
            }, 1000)
        }
    }

    const handleExampleClick = (example: string) => {
        addMessage(example, 'user')
    }

    return (
        <div className='h-full flex-1 '>
            <div className="flex flex-col h-[calc(100vh-4rem)] rounded-xl">

                <ScrollArea className="flex-1 relative" ref={scrollAreaRef}>
                    {messages.length === 0 ? (
                        <EmptyState onExampleClick={handleExampleClick} />
                    ) : (
                        <div className="p-6 space-y-6 max-w-4xl mx-auto">
                            {messages.map((message, index) => (
                                <div
                                    key={message.id}
                                    className={`flex items-end gap-3 ${message.sender === 'user' ? 'flex-row-reverse' : ''
                                        }`}
                                >
                                    <Avatar className="h-10 w-10 border-2 border-white dark:border-slate-700 shadow-md">
                                        {message.sender === 'bot' ? (
                                            <>
                                                <AvatarImage src="/bot-avatar.png" alt="Bot Avatar" />
                                                <AvatarFallback className="bg-gradient-to-br from-blue-500 to-indigo-500">
                                                    <Bot className="h-6 w-6 text-white" />
                                                </AvatarFallback>
                                            </>
                                        ) : (
                                            <>
                                                <AvatarImage src="/user-avatar.png" alt="User Avatar" />
                                                <AvatarFallback className="bg-gradient-to-br from-indigo-500 to-purple-500">
                                                    <User className="h-6 w-6 text-white" />
                                                </AvatarFallback>
                                            </>
                                        )}
                                    </Avatar>
                                    <div
                                        className={`rounded-2xl px-5 py-3 max-w-[80%] shadow-md transition-all duration-300 ease-in-out ${message.sender === 'user'
                                            ? 'bg-gradient-to-br from-indigo-500 to-purple-500 text-white'
                                            : 'bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700'
                                            } ${index === messages.length - 1 ? 'animate-fadeIn' : ''}`}
                                    >
                                        <p className="text-sm leading-relaxed">{message.content}</p>
                                        <time className="text-[10px] mt-2 block opacity-70">
                                            {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                        </time>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </ScrollArea>

                <div className="border-t border-slate-200 dark:border-slate-700 p-6 sticky bottom-0">
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

