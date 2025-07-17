'use client';

import React, { useState } from 'react'
import { Textarea } from "@/components/ui/textarea";
import Image from "next/image";
import { useQueryContext } from '@/lib/QueryProvider';

export default function Input() {

	const [value, setValue] = useState("");
	const { toggleInput, addQuery, isSubmitted, isLoading } = useQueryContext();

	const handleSave = () => {

		if (value.trim()) {
			toggleInput();
			addQuery(value);	
			setValue("");
		} 
	};

	const handleKeyDown = (e) => {
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault();
			handleSave();
		}
	};

  return (
    <div>
      <div className={`card-wrapper group`}>
				<div className="card-content">
					<Textarea 
						className={`resize-none pr-14 w-full items-center transition-all delay-150 duration-300 ease-in-out ${isSubmitted ? 'h-10 px-3 py-5' : 'h-40 p-3'}`}
						placeholder="Ask a question" 
						value={value}
						onChange={e => setValue(e.target.value)}
						onKeyDown={handleKeyDown}
					/>
					<div 
						className={`absolute -translate-y-1/2 p-3 right-2 hover:bg-black/10 rounded-full ${isSubmitted ? 'top-1/2' : 'top-3/4'} ${isLoading ? 'border border-black hover:border-0' : ''}`}
						onClick={handleSave}
					>
						{isLoading ? <div className="w-4 h-4 bg-red-600"></div> : <Image src={'/Magnifying_glass_icon.svg'} width={25} height={25} alt="Search icon" />}
					</div>
				</div>
			</div>
    </div>
  )
}
