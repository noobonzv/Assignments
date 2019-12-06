(define (domain puzzle)
    (:requirements :strips :equality :typing)
    (:types num loc)
    (:predicates (at ?x - num ?y - loc)
                 (adj ?m - loc ?n - loc))

    (:action slide
        :parameters (?mov_num - num ?cur_loc - loc ?blank_loc - loc)
        :precondition (and 
						  (at ?mov_num ?cur_loc) 
						  (at n0 ?blank_loc)
                          (adj ?cur_loc ?blank_loc)
                      ) 
        :effect (and
					(at ?mov_num ?blank_loc)
					(not (at ?mov_num ?cur_loc))
					(at n0 ?cur_loc)
					(not (at n0 ?blank_loc))
				) 
    )
)
