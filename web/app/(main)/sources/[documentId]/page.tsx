"use client";

import { useParams } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useState } from "react";
import { toast } from "sonner";
import { ArrowLeft } from "lucide-react";
import Link from "next/link";

export default function DocumentPage() {
    const params = useParams();
    const [content, setContent] = useState("");
    const [loading, setLoading] = useState(false);

    const { data: document } = useQuery({
        queryKey: ["document", params.documentId],
        queryFn: async () => {
            const response = await axios.get(`/api/documents/${params.documentId}`);
            setContent(response.data.content || "");
            return response.data;
        },
    });

    const onSave = async () => {
        try {
            setLoading(true);
            await axios.patch(`/api/documents/${params.documentId}`, { content });
            toast.success("Document saved successfully");
        } catch (error) {
            toast.error("Failed to save document");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="h-full p-4 space-y-4">
            <div className="flex items-center gap-4">
                <Link href="/sources">
                    <Button variant="ghost" size="sm">
                        <ArrowLeft className="h-4 w-4 mr-2" />
                        Back
                    </Button>
                </Link>
                <h1 className="text-2xl font-bold">{document?.name}</h1>
            </div>
            <div className="flex flex-col gap-4">
                <Textarea
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    className="flex-1 min-h-[500px] p-4 font-mono"
                    placeholder="Enter your markdown content here..."
                />
                <Button onClick={onSave} disabled={loading}>
                    Save Changes
                </Button>
            </div>
        </div>
    );
} 