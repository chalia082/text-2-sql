import React from 'react'

export default function page() {
  return (
    <div className="py-10 px-8">
      <div className='grid gap-8 items-start justify-center'>
        <div className="relative">
          <div className='absolute inset-0.5 rounded-2xl opacity-80' style={{background: "linear-gradient(90deg, #EE2D3D 0%, #602CF3 20%, #48B9FD 40%, #100A50 60%, #872CC1 80%, #C10D68 100%)"}} ></div>
          <div className='relative bg-white w-40 h-12 rounded-2xl'>Hello</div>
        </div>
      </div>
    </div>
  )
}
