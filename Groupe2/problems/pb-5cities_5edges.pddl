(define (problem pb-5cities_5edges)
    (:domain tps)
    (:requirements :strips)
    (:objects c0 c1 c2 c3 c4)
    (:init (connected c0 c1) (connected c0 c2) (connected c0 c3) (connected c0 c4) (connected c1 c3) (in c0) (not (delivered c0)) (not (in c1)) (not (in c2)) (not (in c3)) (not 
(in c4)))
    (:goal [Predicate(delivered, c0), Predicate(delivered, c1), Predicate(delivered, c2), Predicate(delivered, c3), Predicate(delivered, c4)])
)