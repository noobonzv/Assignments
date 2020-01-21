(define (problem prob)
	(:domain cube)
	(:objects r o y g b w -color)
	(:init 	(p1 b o y)(p2 r y b)(p3 o b w)(p4 g r w)
			(p5 o y g)(p6 o w g)(p7 y r g)(p8 b r w)
	)

	(:goal 	(and(p1 r w b)(p2 r y b)(p3 o y b)(p4 o w b)
				(p5 r w g)(p6 r y g)(p7 o y g)(p8 o w g)
			)
	)
)

; y-w r-o b-g
; case 1