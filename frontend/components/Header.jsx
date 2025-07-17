import Image from 'next/image'
import React from 'react'
import { SignedIn, SignedOut, SignInButton, SignUpButton, UserButton } from "@clerk/nextjs";
import { useQueryContext } from '@/lib/QueryProvider';



export default function Header() {

  const { clearChat } = useQueryContext()

  const handleClick = () => {
    clearChat()
  }

  return (
    <div className="relative border-b-4" 
      style={{
        borderImage: "linear-gradient(90deg, #EE2D3D 0%, #602CF3 20%, #48B9FD 40%, #100A50 60%, #872CC1 80%, #C10D68 100%) 1",
        borderBottomStyle: "solid"
      }}
    >
      <div className='relative container mx-auto bg-transparent flex justify-between px-6 py-5 items-center'>
        <div className='cursor-pointer' onClick={handleClick}><Image src={'/WL_logo.png'} height={200} width={200} alt='WorldLink logo'/></div>
        <header className="flex justify-end items-center">
          <SignedOut>
            <SignInButton />
            <SignUpButton>
              <button className="bg-[#6c47ff] text-white rounded-full font-medium text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 cursor-pointer">
                Sign Up
              </button>
            </SignUpButton>
          </SignedOut>
        </header>
        <SignedIn> <UserButton /> </SignedIn>
      </div>
    </div>
  )
}
