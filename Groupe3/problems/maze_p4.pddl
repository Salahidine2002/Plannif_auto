(define (problem maze_p1)
  (:domain maze)
  (:objects x1 x2 x3 x4 x5 x6 x7 x8 x9 x10 x11 x12 x13 x14 x15 y1 y2 y3 y4 y5 y6 y7 y8 y9 y10 y11 y12 y13 y14 y15 - position maxime - agent)
  (:init
    (wall x3 y1) (wall x4 y1) (wall x5 y1) (wall x6 y1) (wall x7 y1) (wall x8 y1) (wall x9 y1) (wall x10 y1) 
										                                                       (wall x10 y2)
    (wall x3 y3) (wall x4 y3) (wall x5 y3) 		        (wall x7 y3) (wall x8 y3) (wall x9 y3) (wall x10 y3) 
                              (wall x5 y4)		        (wall x7 y4)
                              (wall x5 y5)              (wall x7 y5) (wall x8 y5) (wall x9 y5) (wall x10 y5) (wall x11 y5) (wall x12 y5)
                              (wall x5 y6)										                                           (wall x12 y6)
                              (wall x5 y7)										                                           (wall x12 y7) (wall x13 y7) (wall x14 y7)
                              (wall x5 y8)		        (wall x7 y8) (wall x8 y8) (wall x9 y8) (wall x10 y8)					                       (wall x14 y8)
                              (wall x5 y9)		        (wall x7 y9) 										                                           (wall x14 y9)
                              (wall x5 y10)		        (wall x7 y10)	          (wall x9 y10) (wall x10 y10) (wall x11 y10) (wall x12 y10)	       (wall x14 y10)
                              (wall x5 y11)		        (wall x7 y11) 							                              (wall x12 y11)	       (wall x14 y11)
                              (wall x5 y12)		        (wall x7 y12)	          (wall x9 y12) (wall x10 y12) (wall x11 y12) (wall x12 y12)	       (wall x14 y12)
                              (wall x5 y13)		        (wall x7 y13) 							                              (wall x12 y13)	       (wall x14 y13)
                              (wall x5 y14)		        (wall x7 y14) 							                              (wall x12 y14)	       (wall x14 y14)
                              (wall x5 y15)		        (wall x7 y15) 							                              (wall x12 y15)
    (can_jump maxime)
    (inc x1 x2) (inc x2 x3) (inc x3 x4) (inc x4 x5) (inc x5 x6) (inc x6 x7) (inc x7 x8) (inc x8 x9) (inc x9 x10) (inc x10 x11) (inc x11 x12) (inc x12 x13) (inc x13 x14) (inc x14 x15)
    (dec x2 x1) (dec x3 x2) (dec x4 x3) (dec x5 x4) (dec x6 x5) (dec x7 x6) (dec x8 x7) (dec x9 x8) (dec x10 x9) (dec x11 x10) (dec x12 x11) (dec x13 x12) (dec3 x14 x1) (dec x15 x14)
    (inc y1 y2) (inc y2 y3) (inc y3 y4) (inc y4 y5) (inc y5 y6) (inc y6 y7) (inc y7 y8) (inc y8 y9) (inc y9 y10) (inc y10 y11) (inc y11 y12) (inc y12 y13) (inc y13 y14) (inc y14 y15)
    (dec y2 y1) (dec y3 y2) (dec y4 y3) (dec y5 y4) (dec y6 y5) (dec y7 y6) (dec y8 y7) (dec y9 y8) (dec y10 y9) (dec y11 y10) (dec y12 y11) (dec y13 y12) (dec3 y14 y1) (dec y15 y14)
    (at maxime x1 y1))
  (:goal
    (at maxime x11 y15))
  )