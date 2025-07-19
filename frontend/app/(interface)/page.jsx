'use client';

import Input from "@/components/Input";
import Suggestions from "@/components/Suggestions"; 
import { useQueryContext } from "@/lib/QueryProvider";
import Output from "@/components/Output";
import Header from "@/components/Header";
import { useSidebar } from "@/lib/SidebarProvider";
import Footer from "@/components/Footer";
import QueryAPICall from "@/components/QueryAPICall";


export default function Home() {

  const { isSubmitted } = useQueryContext();
  const { expanded } = useSidebar();

  return ( 
    <div className="h-full relative flex flex-col">
      <header className=''><Header /></header>
      <div className={`container mx-auto relative flex flex-col xl:px-60 px-10 h-full ${isSubmitted ? 'overflow-x-auto' : 'justify-between'}`}>
        <div className={`text-center transition-all delay-150 duration-300 ease-in-out ${ isSubmitted ? 'hidden opacity-100' : 'mt-10 opacity-100'}`}> <h1 className="text-3xl font-bold">Welcome</h1> </div>
        <div className={`h-fit mb-14 transition-discrete delay-200 ${ isSubmitted ? 'flex' : 'hidden'}`}> <Output /> </div>
        <div> <QueryAPICall /> </div>
        <div className={`fixed w-full xl:px-80 md:px-40 transition-all duration-200 delay-75 ease-in-out z-10 ${isSubmitted ? 'bottom-0 mb-8' : 'bottom-1/2'} ${expanded ? 'left-30' : ' left-0'}`}> <Input /> </div>
        <div className={`px-0 transition-all delay-150 duration-300 ease-in-out ${ isSubmitted ? 'hidden' : ' flex flex-col'}`}> <Suggestions /> </div>
        {isSubmitted && ( <footer className="mt-auto"><Footer /></footer> )}
      </div>
      
    </div>
  );
}

