import React from 'react'

export default function Suggestions() {

	const suggestions = [
    {name:'Show me the total number of employees in each department.'},
    {name:'Get the names and salaries of employees who earn more than $100,000.'},
    {name:'Find the average bonus for employees who joined after 2020.'}
  ]
	
  return (
    <div>
      <h2 className="font-bold text-xl pb-2">Suggestions:</h2>
			<ul className="flex flex-col">
				{suggestions.map((item, i) => (
					<li key={i} className="flex">
						<span className="mr-2">{ i+1 + '.' }</span>{item.name}
					</li>
				))}
			</ul>
    </div>
  )
}
