import { TiThMenuOutline } from "react-icons/ti";

import React from 'react'
import { useSidebar } from "@/lib/SidebarProvider";

export default function Sidebar() {

  const { expanded, toggleSidebar } = useSidebar();

  const sampleChatHistory = [
    {
      id: 1,
      title: "Customer Data Analysis",
      timestamp: "2024-01-15",
      preview: "Show me all customers from last month"
    },
    {
      id: 2,
      title: "Sales Report Query",
      timestamp: "2024-01-14",
      preview: "Generate sales report for Q4"
    },
    {
      id: 3,
      title: "Inventory Check",
      timestamp: "2024-01-13",
      preview: "Find products with low stock"
    },
    {
      id: 4,
      title: "User Activity Log",
      timestamp: "2024-01-12",
      preview: "Show user login activity"
    },
    {
      id: 5,
      title: "Financial Summary",
      timestamp: "2024-01-11",
      preview: "Calculate total revenue this year"
    }
  ];

  return (
    <div className={`border-r-2 h-full transition-all duration-200 ease-in-out ${expanded ? 'w-60' : 'w-fit' }`}>
      <div className="py-3 px-3 overflow-hidden flex flex-col gap-20 h-full">
        {/*-----icon-----*/}
        <div onClick={toggleSidebar} className="w-fit transition-all duration-200 ease-in-out hover:bg-black/10 p-2 rounded-full"><TiThMenuOutline className="size-7" /></div>
        {/*-----content-----*/}
        <ul className={`flex flex-col w-full ${expanded ? 'w-12' : 'w-0'}`}>
          {sampleChatHistory.map((item) => (
            <li 
              key={item.id} 
              className={`text-sm truncate cursor-pointer hover:bg-black/10 transition-all duration-300 ease-out p-1 rounded-lg ${expanded ? 'w-full' : 'hidden w-0'}`} 
            >
              {item.preview}</li>
          ))}
        </ul>
        {/*-----footer-----*/} 
        <div className="mt-auto self-center">
          <svg 
            width="38" 
            height="30" 
            viewBox="0 0 301 216"
            className="transition-opacity duration-200"
          >
            <title>WL logo</title>
            <defs>
              <style>{`.s0 { fill: #ee2d3d } .s1 { fill: #000000 }`}</style>
            </defs>
            <g>
              <path fillRule="evenodd" className="s0" d="m226.5 215.2h-18.3l74.8-211h18.3l-74.8 211z"/>
              <path fillRule="evenodd" className="s0" d="m90.5 215.2h-18.4l74.8-211h18.4l-74.8 211z"/>
              <path fillRule="evenodd" className="s1" d="m18.3 4.2h-18.3l53.3 150.3 9.2-25.9-44.2-124.4z"/>
            </g>
          </svg>
        </div>
      </div>
    </div>
  )
}