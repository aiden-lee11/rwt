## resume worktrees 

- ability to have controlled and tailored resumes and cover letters for each of my applications

- this made my mind think of worktrees so essentially the goal here is a cli tool in which we can do something like 

second arg is enforced name 
`rwt (name) [-l Link] [-ai AI tailoring] [-cv Add a cv latex folder]`

the link would be an optional param for curling the page data if we want to tailor off of that

thinking right now we just have one base template for resume and cover letter but in the future maybe thats a flag or cli interface where we can select mode?

what this command would produce is an isolated folder in the rwt/worktrees directory for ex 

`rwt -n OpenAI -cv`

would produce a directory in `rwt/worktrees/OpenAI` that is populated with a dir for resume/ and cv/ and in both would just have the base .tex file 
