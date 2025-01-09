"use client"

import * as React from "react"
import {
  BookOpen,
  Bot,
  Command,
  File,
  LifeBuoy,
  LogOut,
  Map,
  PieChart,
  Send,
  Settings2,
  SquareTerminal,
} from "lucide-react"
import { signOut } from "next-auth/react"

import { NavMain } from "@/components/nav-main"
import { Separator } from "@/components/ui/separator"
import { Button } from "@/components/ui/button"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"

const data = {
  user: {
    name: "shadcn",
    email: "m@example.com",
    avatar: "/avatars/shadcn.jpg",
  },
  navMain: [
    {
      title: "Chat",
      url: "/chat",
      icon: SquareTerminal,
      isActive: true,
      items: [

      ],
    },
    {
      title: "Documents",
      url: "/documents",
      icon: File,
      isActive: true,
      items: [

      ],
    },
    {
      title: "Data Sources",
      url: "/data-sources",
      icon: Bot,
      items: [

      ],
    },
    {
      title: "Agents",
      url: "/agents",
      icon: BookOpen,
      items: [

      ],
    },
    {
      title: "Settings",
      url: "/settings",
      icon: Settings2,
      items: [

      ],
    },
  ],

}

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar variant="inset" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" asChild>
              <a href="#">
                <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
                  <Command className="size-4" />
                </div>
                <div className="grid flex-1 text-left text-sm leading-tight">
                  <span className="truncate font-semibold">Acme Inc</span>
                  <span className="truncate text-xs">Enterprise</span>
                </div>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={data.navMain} />
      </SidebarContent>
      <SidebarFooter>
        <Separator />
        <Button variant="ghost" className="w-full justify-between flex flex-row text-md gap-2" onClick={() => signOut()}>
          Logout <LogOut className="size-4" />
        </Button>
      </SidebarFooter>
    </Sidebar>
  )
}
