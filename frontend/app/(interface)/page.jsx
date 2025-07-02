'use client';

import Header from "@/components/Header";
import Input from "@/components/Input";
import Suggestions from "@/components/Suggestions"; 
import { useQueryContext } from "@/lib/QueryProvider";
import Output from "@/components/Output";
import APICall from "@/components/APICall";
import { SignedIn, SignedOut } from "@clerk/nextjs";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

function SignedOutRedirect() {
  const router = useRouter();
  useEffect(() => {
    router.replace('/login');
  }, [router]);
  return null;
}

export default function Home() {

  const { isSubmitted } = useQueryContext();

  return (
    
    <div className="h-full">
      <SignedIn>
        <header className=''><Header /></header>
        <main className={`container mx-auto relative flex flex-col xl:px-60 px-10 h-[calc(100%-120px)] ${isSubmitted ? 'overflow-x-auto' : 'justify-between mt-10 pb-52'}`}>
          <div className={`text-center transition-all delay-150 duration-300 ease-in-out ${ isSubmitted ? 'hidden' : ''}`}> <h1 className="text-3xl font-bold">Welcome</h1> </div>
          <div className={`h-fit mb-14 transition-discrete delay-200 ${ isSubmitted ? 'flex' : 'hidden'}`}> <Output /> </div>
          <div className={`h-fit mb-14 transition-discrete delay-200 ${ isSubmitted ? 'flex justify-start' : 'hidden'}`}> <APICall /> </div>
          <div className={`fixed w-full left-0 xl:px-80 md:px-40 transition-all delay-150 duration-300 ease-in-out z-10 ${isSubmitted ? 'bottom-0 mb-8' : 'bottom-1/2'}`}> <Input /> </div>
          <div className={`px-0 transition-all delay-150 duration-300 ease-in-out ${ isSubmitted ? 'hidden' : ' flex flex-col'}`}> <Suggestions /> </div>
        </main>
        <footer className=""> </footer>
      </SignedIn>
      <SignedOut>
        <SignedOutRedirect />
      </SignedOut>
    </div>
  );
}

