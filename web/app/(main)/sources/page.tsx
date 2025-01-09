"use client";

import { Button } from "@/components/ui/button";
import { PlusCircle } from "lucide-react";
import { useState } from "react";
import { CreateDocumentModal } from "../../../components/create-document-modal";
import { DocumentCard } from "@/components/document-card";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";

export default function SourcesPage() {
    const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);

    const { data: documents, refetch } = useQuery({
        queryKey: ["documents"],
        queryFn: async () => {
            const response = await axios.get("/api/documents");
            return response.data;
        },
    });

    return (
        <div className="h-full p-4 space-y-4">
            <div className="flex items-center justify-between">
                <h1 className="text-2xl font-bold">Knowledge Base</h1>
                <Button
                    onClick={() => setIsCreateModalOpen(true)}
                    className="flex items-center gap-2"
                >
                    <PlusCircle className="h-4 w-4" />
                    Create Document
                </Button>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {documents?.map((doc: any) => (
                    <DocumentCard key={doc.id} document={doc} />
                ))}
            </div>

            <CreateDocumentModal
                isOpen={isCreateModalOpen}
                onClose={() => setIsCreateModalOpen(false)}
                onSuccess={() => {
                    setIsCreateModalOpen(false);
                    refetch();
                }}
            />
        </div>
    );
}
