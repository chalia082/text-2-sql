'use client';

import React, { useEffect, useState } from 'react'

export default function page() {

  const [data, setData] = useState(null);

  const apiURI = process.env.NEXT_PUBLIC_TEST_API_URI;
  

  useEffect(() => {
    fetch(apiURI)
      .then(response => response.json())
      .then(json => setData(json));
  }, []);
  
  return (
    <div>
      {data ? (
        <div className="">
          <p className="">{data.name}</p>
        </div>
      ) : (
        <p className="">Not fetched yet</p>
      )}
    </div>
  )
}
