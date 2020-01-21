(define (domain cube)
	(:requirements :strips :equality :typing)
	(:predicates 
		(p1 ?x ?y ?z -color)
		(p2 ?x ?y ?z -color)
		(p3 ?x ?y ?z -color)
		(p4 ?x ?y ?z -color)
		(p5 ?x ?y ?z -color)
		(p6 ?x ?y ?z -color)
		(p7 ?x ?y ?z -color)
		(p8 ?x ?y ?z -color)
		)
	
	
	
	
	
	(:action UUU
		:parameters()
		:effect
		(and
			(forall(?x ?y ?z -color)
				(when(p5 ?x ?y ?z)
					(and(not(p5 ?x ?y ?z))(p8 ?y ?x ?z)))
			)
			(forall(?x ?y ?z -color)
				(when(p6 ?x ?y ?z)
					(and(not(p6 ?x ?y ?z))(p5 ?y ?x ?z)))
			)
			(forall(?x ?y ?z -color)
				(when(p7 ?x ?y ?z)
					(and(not(p7 ?x ?y ?z))(p6 ?y ?x ?z)))
			)
			(forall(?x ?y ?z -color)
				(when(p8 ?x ?y ?z)
					(and(not(p8 ?x ?y ?z))(p7 ?y ?x ?z)))
			)
		)
	)
	
	
	(:action F
		:parameters()
		:effect
		(and
			(forall(?x ?y ?z -color)
				(when(p1 ?x ?y ?z)
					(and(not(p1 ?x ?y ?z))(p5 ?z ?y ?x)))
			)
			(forall(?x ?y ?z -color)
				(when(p5 ?x ?y ?z)
					(and(not(p5 ?x ?y ?z))(p8 ?z ?y ?x)))
			)
			(forall(?x ?y ?z -color)
				(when(p8 ?x ?y ?z)
					(and(not(p8 ?x ?y ?z))(p4 ?z ?y ?x)))
			)
			(forall(?x ?y ?z -color)
				(when(p4 ?x ?y ?z)
					(and(not(p4 ?x ?y ?z))(p1 ?z ?y ?x)))
			)
		)
	)

	(:action FFF
		:parameters()
		:effect
		(and
			(forall(?x ?y ?z -color)
				(when(p1 ?x ?y ?z)
					(and(not(p1 ?x ?y ?z))(p4 ?z ?y ?x)))
			)
			(forall(?x ?y ?z -color)
				(when(p5 ?x ?y ?z)
					(and(not(p5 ?x ?y ?z))(p1 ?z ?y ?x)))
			)
			(forall(?x ?y ?z -color)
				(when(p8 ?x ?y ?z)
					(and(not(p8 ?x ?y ?z))(p5 ?z ?y ?x)))
			)
			(forall(?x ?y ?z -color)
				(when(p4 ?x ?y ?z)
					(and(not(p4 ?x ?y ?z))(p8 ?z ?y ?x)))
			)
		)
	)
	
	
	(:action R
		:parameters()
		:effect
		(and
			(forall(?x ?y ?z -color)
				(when(p3 ?x ?y ?z)
					(and(not(p3 ?x ?y ?z))(p4 ?x ?z ?y)))
			)
			(forall(?x ?y ?z -color)
				(when(p4 ?x ?y ?z)
					(and(not(p4 ?x ?y ?z))(p8 ?x ?z ?y)))
			)
			(forall(?x ?y ?z -color)
				(when(p8 ?x ?y ?z)
					(and(not(p8 ?x ?y ?z))(p7 ?x ?z ?y)))
			)
			(forall(?x ?y ?z -color)
				(when(p7 ?x ?y ?z)
					(and(not(p7 ?x ?y ?z))(p3 ?x ?z ?y)))
			)
		)
	)	

	(:action RRR
		:parameters()
		:effect
		(and
			(forall(?x ?y ?z -color)
				(when(p3 ?x ?y ?z)
					(and(not(p3 ?x ?y ?z))(p7 ?x ?z ?y)))
			)
			(forall(?x ?y ?z -color)
				(when(p4 ?x ?y ?z)
					(and(not(p4 ?x ?y ?z))(p3 ?x ?z ?y)))
			)
			(forall(?x ?y ?z -color)
				(when(p8 ?x ?y ?z)
					(and(not(p8 ?x ?y ?z))(p4 ?x ?z ?y)))
			)
			(forall(?x ?y ?z -color)
				(when(p7 ?x ?y ?z)
					(and(not(p7 ?x ?y ?z))(p8 ?x ?z ?y)))
			)
		)
	)
	
	(:action U
		:parameters()
		:effect
		(and
			(forall(?x ?y ?z -color)
				(when(p5 ?x ?y ?z)
					(and(not(p5 ?x ?y ?z))(p6 ?y ?x ?z)))
			)
			(forall(?x ?y ?z -color)
				(when(p6 ?x ?y ?z)
					(and(not(p6 ?x ?y ?z))(p7 ?y ?x ?z)))
			)
			(forall(?x ?y ?z -color)
				(when(p7 ?x ?y ?z)
					(and(not(p7 ?x ?y ?z))(p8 ?y ?x ?z)))
			)
			(forall(?x ?y ?z -color)
				(when(p8 ?x ?y ?z)
					(and(not(p8 ?x ?y ?z))(p5 ?y ?x ?z)))
			)
		)
	)
	
)
