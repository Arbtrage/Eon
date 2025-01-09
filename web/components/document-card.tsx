"use client";

import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { FileText } from "lucide-react";
import { useRouter } from "next/navigation";

export const DocumentCard = ({ document }: { document: any }) => {
    const router = useRouter();

    return (
        <Card
            className="hover:opacity-75 cursor-pointer transition"
            onClick={() => router.push(`/sources/${document.id}`)}
        >
            <CardHeader className="flex flex-row items-center gap-4">
                <FileText className="h-8 w-8" />
                <CardTitle className="truncate">{document.name}</CardTitle>
            </CardHeader>
        </Card>
    );
}; 