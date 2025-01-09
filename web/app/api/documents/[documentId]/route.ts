import prisma from "@/lib/prisma";
import { NextResponse } from "next/server";
import { getSession } from "@/lib/auth";

export async function GET(
    req: Request,
    { params }: { params: { documentId: string } }
) {
    try {
        const session = await getSession();
        if (!session) {
            return new NextResponse("Unauthorized", { status: 401 });
        }
        const document = await prisma.document.findUnique({
            where: {
                id: params.documentId,
                userId: session.user.id,
            },
        });
        if (!document) {
            return new NextResponse("Document not found", { status: 404 });
        }
        return NextResponse.json(document);
    } catch (error) {
        return new NextResponse("Internal Error", { status: 500 });
    }
}

export async function PATCH(
    req: Request,
    { params }: { params: { documentId: string } }
) {
    try {
        const session = await getSession();
        if (!session) {
            return new NextResponse("Unauthorized", { status: 401 });
        }
        const body = await req.json();
        const document = await prisma.document.update({
            where: {
                id: params.documentId,
                userId: session.user.id,
            },
            data: {
                content: body.content,
            },
        });
        return NextResponse.json(document);
    } catch (error) {
        return new NextResponse("Internal Error", { status: 500 });
    }
} 