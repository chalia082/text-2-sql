'use client';

import Header from "@/components/Header";
import Sidebar from "@/components/Sidebar";
import { SignedIn, SignedOut } from "@clerk/nextjs";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

const { useSidebar, SidebarProvider } = require("@/lib/SidebarProvider");

export default function InterfaceLayout({ children }) {
  return (
    <SidebarProvider>
      <LayoutContent>{children}</LayoutContent>
    </SidebarProvider>
  );
}

function SignedOutRedirect() {
  const router = useRouter();
  useEffect(() => {
    router.replace('/login');
  }, [router]);
  return null;
}

function LayoutContent({ children }) {
  const { expanded } = useSidebar();

  return (
    <div className="h-full flex w-full">
      <SignedIn>
        <div className=""><Sidebar /></div>
        <main className="w-full">{children}</main>
        <footer className=""> </footer>
      </SignedIn>
      <SignedOut>
        <SignedOutRedirect />
      </SignedOut>
    </div>
  )
}