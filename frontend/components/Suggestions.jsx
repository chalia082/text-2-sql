import React from 'react'

const transition_custom = 'transition-all duration-200 ease-in-out'


export default function Suggestions() {

	const suggestions = [
    {name:'Show me the total number of employees in each department.'},
    {name:'Get the names and salaries of employees who earn more than $100,000.'},
    {name:'Find the average bonus for employees who joined after 2020.'}
  ]
	
  return (
    <div className='pb-20'>
      <h2 className="font-bold text-xl pb-2 pl-2">Suggestions:</h2>
			<ul className={`flex flex-col `}>
				{suggestions.map((item, i) => (
					<li key={i} className={`flex w-fit hover:scale-102 hover:bg-black/10 rounded-xl px-2 py-1 cursor-pointer ${transition_custom}`}>
						<span className="mr-2">{ i+1 + '.' }</span>{item.name}
					</li>
				))}
			</ul>
    </div>
  )
}
