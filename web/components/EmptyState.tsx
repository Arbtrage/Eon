import { Bot, MessageSquare } from 'lucide-react'
import { Button } from "@/components/ui/button"

interface EmptyStateProps {
    onExampleClick: (message: string) => void;
}

export function EmptyState({ onExampleClick }: EmptyStateProps) {
    const examples = [
        "What are the key principles of effective project management?",
        "Can you explain the concept of emotional intelligence?",
        "How can I improve my public speaking skills?"
    ];

    return (
        <div className="absolute inset-0 flex flex-col items-center justify-center h-full text-center px-4">
            <Bot className="h-16 w-16 text-blue-500 mb-6" />
            <h2 className="text-2xl font-semibold text-slate-800 dark:text-slate-100 mb-2">
                Welcome to Professional Chat Assistant
            </h2>
            <p className="text-slate-600 dark:text-slate-300 mb-8 max-w-md">
                I'm here to help you with any questions or tasks you may have. Feel free to ask me anything!
            </p>
            <div className="grid gap-4 w-full max-w-md">
                {examples.map((example, index) => (
                    <Button
                        key={index}
                        variant="outline"
                        className="justify-start text-left h-auto py-3 px-4"
                        onClick={() => onExampleClick(example)}
                    >
                        <MessageSquare className="h-5 w-5 mr-3 flex-shrink-0" />
                        <span className="line-clamp-2">{example}</span>
                    </Button>
                ))}
            </div>
        </div>
    )
}
