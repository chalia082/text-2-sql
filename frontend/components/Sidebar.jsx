import { TiThMenuOutline } from "react-icons/ti";
import { BsLayoutSidebarInset } from "react-icons/bs";
import { IoMdSearch } from "react-icons/io";

import { BiSolidEdit } from "react-icons/bi";

import React from "react";
import { useSidebar } from "@/lib/SidebarProvider";
import { Tooltip, TooltipContent, TooltipTrigger } from "./ui/tooltip";

const transition_custom = 'transition-all duration-200 ease-in-out'

const options = [
  {
    label: 'New Chat',
    icon: BiSolidEdit
  },
  {
    label: 'Search Chats',
    icon: IoMdSearch
  }
]


export default function Sidebar() {
  const { expanded, toggleSidebar } = useSidebar();

  const sampleChatHistory = [
    {
      id: 1,
      title: "Customer Data Analysis",
      timestamp: "2024-01-15",
      preview: "Show me all customers from last month",
    },
    {
      id: 2,
      title: "Sales Report Query",
      timestamp: "2024-01-14",
      preview: "Generate sales report for Q4",
    },
    {
      id: 3,
      title: "Inventory Check",
      timestamp: "2024-01-13",
      preview: "Find products with low stock",
    },
    {
      id: 4,
      title: "User Activity Log",
      timestamp: "2024-01-12",
      preview: "Show user login activity",
    },
    {
      id: 5,
      title: "Financial Summary",
      timestamp: "2024-01-11",
      preview: "Calculate total revenue this year",
    },
  ];

  return (
    <div className={`border-r-1 h-full w-fit`} >
      <div className={`p-3 overflow-hidden flex flex-col gap-10 h-full ${transition_custom} ${ expanded ? "w-60" : "w-fit" }`} >
        <div className="flex flex-col gap-3">
          <Tooltip>
            <TooltipTrigger asChild>
              <div onClick={toggleSidebar} className={`w-fit hover:bg-black/10 p-2 rounded-full cursor-pointer ${transition_custom} ${expanded ? 'self-end' : 'self-start'}`} >
                <BsLayoutSidebarInset className={`size-5 text-[#6f6f6f]`} />
              </div>
            </TooltipTrigger>
            <TooltipContent>
              {expanded ? <p>Close sidebar</p> : <p>Open sidebar</p>}
            </TooltipContent>
          </Tooltip>
          <div className={`w-full space-y-3 ${transition_custom}`}>
            {options.map((option, o) => (
              <div key={o} className={`flex items-center hover:bg-black/10 p-2 cursor-pointer ${transition_custom} ${expanded ? "w-full gap-1 rounded-xl" : "w-fit gap-0 rounded-full"}`}>
                <Tooltip>
                  <TooltipTrigger asChild disabled={expanded}>
                    <option.icon className="size-5 text-[#6f6f6f]"/>
                  </TooltipTrigger>
                  <TooltipContent className={expanded ? "opacity-0 pointer-events-none" : 'opacity-100'}>{option.label}</TooltipContent>
                </Tooltip>
                <span className={`text-sm truncate leading-none ${transition_custom} ${ expanded ? 'w-32' : 'w-0 opacity-100' }`}>
                  {option.label}
                </span>
              </div>
            ))}
          </div>
        </div>
        <div className="flex flex-col">
          <h3 className={`text-sm px-2  text-[#6f6f6f] truncate text-nowrap ${transition_custom} ${ expanded ? "w-fit opacity-100" : "w-0 opacity-0" }`} >Chat history</h3>
          <ul className={`flex flex-col py-2 ${ expanded ? "w-full opacity-100" : "w-0 opacity-0" }`} >
            {sampleChatHistory.map((item) => (
              <li
                key={item.id}
                className={`text-sm truncate tracking-tight cursor-pointer hover:bg-black/10 p-2 rounded-lg 
                  ${transition_custom} 
                  ${expanded ? "w-full opacity-100" : "w-0 opacity-0" }
                `}
              >
                {item.preview}
              </li>
            ))}
          </ul>
        </div>
        {/*-----footer-----*/}
        <div className="mt-auto justify-self-start p-1">
          <svg
            width="28"
            height="20"
            viewBox="0 0 301 216"
            className="transition-opacity duration-200"
          >
            <title>WL logo</title>
            <defs>
              <style>{`.s0 { fill: #ee2d3d } .s1 { fill: #000000 }`}</style>
            </defs>
            <g>
              <path
                fillRule="evenodd"
                className="s0"
                d="m226.5 215.2h-18.3l74.8-211h18.3l-74.8 211z"
              />
              <path
                fillRule="evenodd"
                className="s0"
                d="m90.5 215.2h-18.4l74.8-211h18.4l-74.8 211z"
              />
              <path
                fillRule="evenodd"
                className="s1"
                d="m18.3 4.2h-18.3l53.3 150.3 9.2-25.9-44.2-124.4z"
              />
            </g>
          </svg>
        </div>
      </div>
    </div>
  );
}