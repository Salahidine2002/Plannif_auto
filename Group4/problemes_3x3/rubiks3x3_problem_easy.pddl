(define
(problem test)
(:domain rubiks-cube)
(:objects yellow white blue green orange red)
(:init
    (cube1 blue red white)
    (cube2 green white orange)
    (cube3 blue orange white)
    (cube4 blue yellow red)
    (cube5 green orange yellow)
    (cube6 green white red)
    (cube7 green red yellow)
    (cube8 blue yellow orange)
    (edge12 white orange)
    (edge24 orange blue)
    (edge34 yellow red)
    (edge13 blue white)
    (edge15 red green)
    (edge26 green white)
    (edge48 blue yellow)
    (edge37 red blue)
    (edge56 white red)
    (edge68 orange green)
    (edge78 yellow orange)
    (edge57 green yellow)
)
(:goal
    (and
        (cube1 red white blue)
        (cube2 orange white blue)
        (cube3 red yellow blue)
        (cube4 orange yellow blue)
        (cube5 red white green)
        (cube6 orange white green)
        (cube7 red yellow green)
        (cube8 orange yellow green)

        (edge12 white blue)
        (edge24 orange blue)
        (edge34 yellow blue)
        (edge13 red blue)

        (edge15 red white)
        (edge26 orange white)
        (edge48 orange yellow)
        (edge37 red yellow)

        (edge56 white green)
        (edge68 orange green)
        (edge78 yellow green)
        (edge57 red green)

    )
)
)