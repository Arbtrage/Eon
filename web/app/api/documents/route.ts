import prisma from "@/lib/prisma";
import { NextResponse } from "next/server";
import { getSession } from "@/lib/auth";

export async function POST(req: Request) {
    try {
        const session = await getSession();
        if (!session?.user?.id) {
            return new NextResponse("Unauthorized", { status: 401 });
        }

        const body = await req.json();
        const document = await prisma.document.create({
            data: {
                name: body.name,
                content: "",
                userId: session.user.id,
            },
        });

        return NextResponse.json({
            id: document.id,
            name: document.name,
            content: document.content,
            userId: document.userId,
            createdAt: document.createdAt,
            updatedAt: document.updatedAt,
            status: document.status
        });
    } catch (error) {
        console.error("POST Error:", error);
        return new NextResponse("Internal Error", { status: 500 });
    }
}

export async function GET() {
    try {
        const session = await getSession();
        if (!session?.user?.id) {
            return new NextResponse("Unauthorized", { status: 401 });
        }

        const documents = await prisma.document.findMany({
            where: {
                userId: session.user.id,
            },
            orderBy: {
                createdAt: "desc",
            },
            select: {
                id: true,
                name: true,
                content: true,
                userId: true,
                createdAt: true,
                updatedAt: true,
                status: true
            }
        });

        return NextResponse.json(documents);
    } catch (error) {
        console.error("GET Error:", error);
        return new NextResponse("Internal Error", { status: 500 });
    }
} 