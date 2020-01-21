(define (problem prob)
	(:domain cube)
	(:objects r o y g b w -color)
	(:init 	(p1 b o y)(p2 b o w)(p3 r g w)(p4 w o g)
			(p5 g y r)(p6 b y r)(p7 r b w)(p8 y o g)
	)

	(:goal 	(and(p1 b r w)(p2 b o w)(p3 g o w)(p4 g r w)
				(p5 b r y)(p6 b o y)(p7 g o y)(p8 g r y)
			)
	)
)

; y-w r-o b-g
; case 4