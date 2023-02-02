; start Z3 query
(declare-fun __soid__will_proceed_ackermann!639 () (_ BitVec 8))
(assert (not (not (= ((_ extract 0 0) __soid__will_proceed_ackermann!639) #b1))))
(check-sat)
(reset)
; end Z3 query
