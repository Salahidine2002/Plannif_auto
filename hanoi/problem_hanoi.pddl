(define (problem pb-5discs-3pegs)
    (:domain hanoi)
    (:requirements :strips)
    (:objects d0 d1 d2 d3 d4 p0 p1 p2)
    (:init (clear d0) (clear p1) (clear p2) (on d0 d1) (on d1 d2) (on d2 d3) (on d3 d4) (on d4 p0) (smaller d0 d1) (smaller d0 d2) (smaller d0 d3) (smaller d0 d4) (smaller d0 p0) (smaller d0 p1) (smaller d0 p2) (smaller d1 d2) (smaller d1 d3) (smaller d1 d4) (smaller d1 p0) (smaller d1 p1) (smaller d1 p2) (smaller d2 d3) (smaller d2 d4) (smaller d2 p0) (smaller d2 p1) (smaller d2 p2) (smaller d3 d4) (smaller d3 p0) (smaller d3 p1) (smaller d3 p2) (smaller d4 p0) (smaller d4 p1) (smaller d4 p2))
    (:goal (and (on d4 p2) (on d0 d1) (on d1 d2) (on d2 d3) (on d3 d4)))
)