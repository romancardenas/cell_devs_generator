
[top]
components : House1

[House1]
type : cell
dim : (300,300)
delay : transport
defaultDelayTime : 1000
border : nonwrapped

neighbors :           House1(0,-1)
neighbors : House1(-1,0)  House1(0,0)  House1(1,0) 
neighbors :           House1(0,1)

initialValue : 0
initialCellsValue : House1.val
localtransition : rules

[rules]

% ...

rule: {(0,0)}   0   { t }
