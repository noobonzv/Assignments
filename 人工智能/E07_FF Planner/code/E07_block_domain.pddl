(define (domain blocks)
    (:requirements :strips :typing :equality 
     :universal-preconditions :conditional-effects)
    (:types physob)
    (:predicates (ontable ?x - physob)
                 (clear ?x - physob)
                 (on ?x ?y - physob))
				 
    (:action move
        :parameters (?x ?y - physob)
        :precondition (and 
						  (clear ?x)
						  (clear ?y)
					   )
					   
        :effect (and
					(
						forall (?z - physob)
							(when (on ?x ?z)
								(and (clear ?z) (not (on ?x ?z)))
							)
					) 
                    (not (clear ?y))
					(on ?x ?y)
                )
    )
	
    (:action moveToTable
        :parameters (?x - physob)
        :precondition (and 
						  (clear ?x)
						  (not (ontable ?x))
					   )
        :effect (and 
					(
						forall (?z - physob) 
							(when (on ?x ?z) 
								(and (clear ?z) (not (on ?x ?z) ) )
							)
					) 
					(ontable ?x)
                )
    )
)
