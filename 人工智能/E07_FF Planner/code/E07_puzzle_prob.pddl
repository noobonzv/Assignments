(define (problem prob)
    (:domain puzzle)
    (:objects n0 n1 n2 n3 n4 n5 n6 n7 n8 - num 
              l1 l2 l3 l4 l5 l6 l7 l8 l9 - loc)

    (:init  (at n1 l1) (at n2 l2) (at n3 l3)
			(at n7 l4) (at n8 l5) (at n0 l6)
			(at n6 l7) (at n4 l8) (at n5 l9)
			
			(adj l1 l2) (adj l1 l4) 
			(adj l2 l1) (adj l2 l3) (adj l2 l5)
			(adj l3 l2) (adj l3 l6) 
            (adj l4 l1) (adj l4 l5) (adj l4 l7)
            (adj l5 l4) (adj l5 l2) (adj l5 l6) (adj l5 l8) 
            (adj l6 l3) (adj l6 l5) (adj l6 l9) 
			(adj l7 l4) (adj l7 l8) 
            (adj l8 l7) (adj l8 l9) (adj l8 l5)
			(adj l9 l6) (adj l9 l8) 
    )

    (:goal (and 
				(at n1 l1) (at n2 l2) (at n3 l3) 
				(at n4 l4) (at n5 l5) (at n6 l6) 
				(at n7 l7) (at n8 l8) (at n0 l9)
			)
    )
)