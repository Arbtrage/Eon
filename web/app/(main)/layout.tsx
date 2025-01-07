import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "../globals.css";
import { AppSidebar } from "@/components/app-sidebar"
import {
    SidebarInset,
    SidebarProvider,
    SidebarTrigger,
} from "@/components/ui/sidebar"
import { getSession } from "@/lib/auth";
import { redirect } from "next/navigation";


export default async function AppLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    const session = await getSession();
    if (!session) {
        return redirect("/auth");
    }
    return (
        <SidebarProvider>
            <AppSidebar />
            <SidebarInset >
                {children}
            </SidebarInset>
        </SidebarProvider>

    );
}
