(define (problem prob)
	(:domain cube)
	(:objects r o y g b w -color)
	(:init 	(p1 b r w)(p2 w g r)(p3 r y g)(p4 o b y)
			(p5 g o y)(p6 r b y)(p7 o g w)(p8 b w o)
	)

	(:goal 	(and(p1 w b r)(p2 w g r)(p3 y g r)(p4 y b r)
				(p5 w b o)(p6 w g o)(p7 y g o)(p8 y b o)
			)
	)
)

; y-w r-o b-g
; case 2