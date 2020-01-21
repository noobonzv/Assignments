(define (problem prob)
	(:domain cube)
	(:objects r o y g b w -color)
	(:init 	(p1 r y g)(p2 y o b)(p3 w b r)(p4 o g w)
			(p5 o w b)(p6 w r g)(p7 r y b)(p8 y o g)
	)

	(:goal 	(and(p1 y r b)(p2 y o b)(p3 w o b)(p4 w r b)
				(p5 y r g)(p6 y o g)(p7 w o g)(p8 w r g)
			)
	)
)

; y-w r-o b-g
; case 3