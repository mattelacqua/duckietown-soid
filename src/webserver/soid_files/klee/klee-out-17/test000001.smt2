(set-logic ALL)
(declare-fun agent0_pos_x_ackermann!2 () (_ BitVec 32))
(declare-fun agent0_pos_z_ackermann!3 () (_ BitVec 32))
(declare-fun agent0_angle_ackermann!4 () (_ BitVec 32))
(declare-fun agent0_forward_step_ackermann!5 () (_ BitVec 32))
(declare-fun agent0_speed_ackermann!6 () (_ BitVec 32))
(declare-fun agent0_signal_choice_ackermann!8 () (_ BitVec 32))
(declare-fun agent0_turn_choice_ackermann!9 () (_ BitVec 32))
(declare-fun agent0_lookahead_ackermann!7 () (_ BitVec 32))
(declare-fun agent0_intersection_arrival_ackermann!11 () (_ BitVec 32))
(declare-fun agent0_initial_direction_ackermann!10 () (_ BitVec 32))
(declare-fun agent0_patience_ackermann!12 () (_ BitVec 32))
(declare-fun agent0_step_count_ackermann!13 () (_ BitVec 32))
(declare-fun agent1_pos_x_ackermann!23 () (_ BitVec 32))
(declare-fun agent1_pos_z_ackermann!15 () (_ BitVec 32))
(declare-fun agent1_angle_ackermann!17 () (_ BitVec 32))
(declare-fun agent1_forward_step_ackermann!18 () (_ BitVec 32))
(declare-fun agent1_speed_ackermann!16 () (_ BitVec 32))
(declare-fun agent1_turn_choice_ackermann!24 () (_ BitVec 32))
(declare-fun agent1_lookahead_ackermann!20 () (_ BitVec 32))
(declare-fun agent1_intersection_arrival_ackermann!19 () (_ BitVec 32))
(declare-fun agent1_initial_direction_ackermann!21 () (_ BitVec 32))
(declare-fun agent1_patience_ackermann!1 () (_ BitVec 32))
(declare-fun agent1_step_count_ackermann!14 () (_ BitVec 32))
(declare-fun agent1_signal_choice_ackermann!0 () (_ BitVec 32))
(declare-fun __soid__will_proceed_ackermann!22 () (_ BitVec 8))
(assert (fp.eq ((_ to_fp 8 24) agent0_pos_x_ackermann!2) ((_ to_fp 8 24) #x3fcae148)))
(assert (fp.eq ((_ to_fp 8 24) agent0_pos_z_ackermann!3) ((_ to_fp 8 24) #x3feba5e3)))
(assert (fp.eq ((_ to_fp 8 24) agent0_angle_ackermann!4) ((_ to_fp 8 24) #x3fcb4396)))
(assert (fp.eq ((_ to_fp 8 24) agent0_forward_step_ackermann!5)
       ((_ to_fp 8 24) #x3ee147ae)))
(assert (fp.eq ((_ to_fp 8 24) agent0_speed_ackermann!6) ((_ to_fp 8 24) #x3b03126f)))
(assert (= #x00000002 agent0_signal_choice_ackermann!8))
(assert (= #x00000002 agent0_turn_choice_ackermann!9))
(assert (fp.eq ((_ to_fp 8 24) agent0_lookahead_ackermann!7)
       ((_ to_fp 8 24) #x3f15c28f)))
(assert (= #x0000004d agent0_intersection_arrival_ackermann!11))
(assert (= #x00000000 agent0_initial_direction_ackermann!10))
(assert (= #x00000000 agent0_patience_ackermann!12))
(assert (= #x0000006d agent0_step_count_ackermann!13))
(assert (fp.eq ((_ to_fp 8 24) agent1_pos_x_ackermann!23) ((_ to_fp 8 24) #x3f939581)))
(assert (fp.eq ((_ to_fp 8 24) agent1_pos_z_ackermann!15) ((_ to_fp 8 24) #x3fcb020c)))
(assert (fp.eq ((_ to_fp 8 24) agent1_angle_ackermann!17) ((_ to_fp 8 24) #x3c8b4396)))
(assert (fp.eq ((_ to_fp 8 24) agent1_forward_step_ackermann!18)
       ((_ to_fp 8 24) #x3ee147ae)))
(assert (fp.eq ((_ to_fp 8 24) agent1_speed_ackermann!16) ((_ to_fp 8 24) #x3e3020c5)))
(assert (= #x00000002 agent1_turn_choice_ackermann!24))
(assert (fp.eq ((_ to_fp 8 24) agent1_lookahead_ackermann!20)
       ((_ to_fp 8 24) #x3f15c28f)))
(assert (= #x0000003c agent1_intersection_arrival_ackermann!19))
(assert (= #x00000002 agent1_initial_direction_ackermann!21))
(assert (= #x00000000 agent1_patience_ackermann!1))
(assert (= #x0000006d agent1_step_count_ackermann!14))
(assert (= #x00000000 agent1_signal_choice_ackermann!0))
(assert (let ((a!1 (fp.mul roundNearestTiesToEven
                   (fp.div roundNearestTiesToEven
                           ((_ to_fp 11 53)
                             roundNearestTiesToEven
                             ((_ to_fp 8 24) agent0_angle_ackermann!4))
                           ((_ to_fp 11 53) #x40091eb851eb851f))
                   ((_ to_fp 11 53) #x4066800000000000))))
  (fp.gt ((_ to_fp 8 24) roundNearestTiesToEven a!1)
         ((_ to_fp 8 24) #x42340000))))
(assert (let ((a!1 (fp.mul roundNearestTiesToEven
                   (fp.div roundNearestTiesToEven
                           ((_ to_fp 11 53)
                             roundNearestTiesToEven
                             ((_ to_fp 8 24) agent0_angle_ackermann!4))
                           ((_ to_fp 11 53) #x40091eb851eb851f))
                   ((_ to_fp 11 53) #x4066800000000000))))
  (fp.leq ((_ to_fp 8 24) roundNearestTiesToEven a!1)
          ((_ to_fp 8 24) #x43070000))))
(assert (let ((a!1 (fp.mul roundNearestTiesToEven
                   (fp.div roundNearestTiesToEven
                           ((_ to_fp 11 53)
                             roundNearestTiesToEven
                             ((_ to_fp 8 24) agent1_angle_ackermann!17))
                           ((_ to_fp 11 53) #x40091eb851eb851f))
                   ((_ to_fp 11 53) #x4066800000000000))))
  (not (and (fp.gt ((_ to_fp 8 24) roundNearestTiesToEven a!1)
                   ((_ to_fp 8 24) #x42340000))
            (fp.leq ((_ to_fp 8 24) roundNearestTiesToEven a!1)
                    ((_ to_fp 8 24) #x43070000))))))
(assert (let ((a!1 (fp.mul roundNearestTiesToEven
                   (fp.div roundNearestTiesToEven
                           ((_ to_fp 11 53)
                             roundNearestTiesToEven
                             ((_ to_fp 8 24) agent1_angle_ackermann!17))
                           ((_ to_fp 11 53) #x40091eb851eb851f))
                   ((_ to_fp 11 53) #x4066800000000000))))
  (not (and (fp.gt ((_ to_fp 8 24) roundNearestTiesToEven a!1)
                   ((_ to_fp 8 24) #x43070000))
            (fp.leq ((_ to_fp 8 24) roundNearestTiesToEven a!1)
                    ((_ to_fp 8 24) #x43610000))))))
(assert (let ((a!1 ((_ fp.to_sbv 32)
             roundTowardZero
             (fp.div roundNearestTiesToEven
                     ((_ to_fp 11 53)
                       roundNearestTiesToEven
                       ((_ to_fp 8 24) agent0_pos_x_ackermann!2))
                     ((_ to_fp 11 53) #x3fe2b851e0000000)))))
  (= #x00000002
     ((_ fp.to_sbv 32)
       roundTowardZero
       ((_ to_fp 11 53) roundNearestTiesToEven a!1)))))
(assert (not (fp.lt ((_ to_fp 8 24) agent0_pos_x_ackermann!2)
            ((_ to_fp 8 24) #x00000000))))
(assert (not (fp.lt ((_ to_fp 8 24) agent0_pos_z_ackermann!3)
            ((_ to_fp 8 24) #x00000000))))
(assert (not (fp.gt ((_ to_fp 8 24) agent0_pos_x_ackermann!2)
            ((_ to_fp 8 24) #x403b3333))))
(assert (not (fp.gt ((_ to_fp 8 24) agent0_pos_z_ackermann!3)
            ((_ to_fp 8 24) #x403b3333))))
(assert (let ((a!1 ((_ fp.to_sbv 32)
             roundTowardZero
             (fp.div roundNearestTiesToEven
                     ((_ to_fp 11 53)
                       roundNearestTiesToEven
                       ((_ to_fp 8 24) agent0_pos_z_ackermann!3))
                     ((_ to_fp 11 53) #x3fe2b851e0000000)))))
  (= #x00000003
     ((_ fp.to_sbv 32)
       roundTowardZero
       ((_ to_fp 11 53) roundNearestTiesToEven a!1)))))
(assert (fp.gt ((_ to_fp 11 53)
         roundNearestTiesToEven
         ((_ to_fp 8 24) agent0_pos_z_ackermann!3))
       ((_ to_fp 11 53) #x3ffb810603333333)))
(assert (fp.lt ((_ to_fp 8 24) agent0_pos_z_ackermann!3) ((_ to_fp 8 24) #x3ff7ae14)))
(assert (not (fp.lt ((_ to_fp 8 24) agent1_pos_x_ackermann!23)
            ((_ to_fp 8 24) #x00000000))))
(assert (not (fp.lt ((_ to_fp 8 24) agent1_pos_z_ackermann!15)
            ((_ to_fp 8 24) #x00000000))))
(assert (not (fp.gt ((_ to_fp 8 24) agent1_pos_x_ackermann!23)
            ((_ to_fp 8 24) #x403b3333))))
(assert (not (fp.gt ((_ to_fp 8 24) agent1_pos_z_ackermann!15)
            ((_ to_fp 8 24) #x403b3333))))
(assert (let ((a!1 (fp.mul roundNearestTiesToEven
                   (fp.div roundNearestTiesToEven
                           ((_ to_fp 11 53)
                             roundNearestTiesToEven
                             ((_ to_fp 8 24) agent1_angle_ackermann!17))
                           ((_ to_fp 11 53) #x40091eb851eb851f))
                   ((_ to_fp 11 53) #x4066800000000000))))
(let ((a!2 (ite (and (fp.gt ((_ to_fp 8 24) roundNearestTiesToEven a!1)
                            ((_ to_fp 8 24) #x43610000))
                     (fp.leq ((_ to_fp 8 24) roundNearestTiesToEven a!1)
                             ((_ to_fp 8 24) #x439d8000)))
                #x00000001
                #x00000002)))
  (= #x00000002 a!2))))
(assert (let ((a!1 ((_ fp.to_sbv 32)
             roundTowardZero
             (fp.div roundNearestTiesToEven
                     ((_ to_fp 11 53)
                       roundNearestTiesToEven
                       ((_ to_fp 8 24) agent1_pos_x_ackermann!23))
                     ((_ to_fp 11 53) #x3fe2b851e0000000)))))
  (= #x00000001
     ((_ fp.to_sbv 32)
       roundTowardZero
       ((_ to_fp 11 53) roundNearestTiesToEven a!1)))))
(assert (let ((a!1 ((_ fp.to_sbv 32)
             roundTowardZero
             (fp.div roundNearestTiesToEven
                     ((_ to_fp 11 53)
                       roundNearestTiesToEven
                       ((_ to_fp 8 24) agent1_pos_z_ackermann!15))
                     ((_ to_fp 11 53) #x3fe2b851e0000000)))))
  (= #x00000002
     ((_ fp.to_sbv 32)
       roundTowardZero
       ((_ to_fp 11 53) roundNearestTiesToEven a!1)))))
(assert (fp.gt ((_ to_fp 8 24) agent1_pos_x_ackermann!23) ((_ to_fp 8 24) #x3f7d70a3)))
(assert (fp.lt ((_ to_fp 11 53)
         roundNearestTiesToEven
         ((_ to_fp 8 24) agent1_pos_x_ackermann!23))
       ((_ to_fp 11 53) #x3ff34bc69ccccccd)))
(assert (let ((a!1 ((_ to_fp 8 24)
             roundNearestTiesToEven
             (fp.div roundNearestTiesToEven
                     ((_ to_fp 11 53)
                       roundNearestTiesToEven
                       ((_ to_fp 8 24) agent0_lookahead_ackermann!7))
                     ((_ to_fp 11 53) #x4024000000000000)))))
  (not (fp.geq ((_ to_fp 8 24) agent1_pos_x_ackermann!23)
               (fp.sub roundNearestTiesToEven
                       ((_ to_fp 8 24) agent0_pos_x_ackermann!2)
                       a!1)))))
(assert (fp.geq ((_ to_fp 8 24) agent0_pos_x_ackermann!2)
        ((_ to_fp 8 24) agent1_pos_x_ackermann!23)))
(assert (fp.leq ((_ to_fp 8 24) agent0_pos_x_ackermann!2)
        (fp.add roundNearestTiesToEven
                ((_ to_fp 8 24) agent1_pos_x_ackermann!23)
                ((_ to_fp 8 24) agent1_lookahead_ackermann!20))))
(assert (fp.geq ((_ to_fp 8 24) agent0_pos_z_ackermann!3)
        ((_ to_fp 8 24) agent1_pos_x_ackermann!23)))
(assert (not (fp.leq ((_ to_fp 8 24) agent0_pos_z_ackermann!3)
             (fp.add roundNearestTiesToEven
                     ((_ to_fp 8 24) agent1_pos_x_ackermann!23)
                     ((_ to_fp 8 24) agent1_lookahead_ackermann!20)))))
(assert (not (fp.geq ((_ to_fp 8 24) agent0_pos_x_ackermann!2)
             (fp.add roundNearestTiesToEven
                     ((_ to_fp 8 24) agent1_pos_x_ackermann!23)
                     ((_ to_fp 8 24) agent1_lookahead_ackermann!20)))))
(assert (fp.geq ((_ to_fp 8 24) agent0_pos_x_ackermann!2)
        (fp.sub roundNearestTiesToEven
                (fp.sub roundNearestTiesToEven
                        ((_ to_fp 8 24) agent1_pos_x_ackermann!23)
                        ((_ to_fp 8 24) agent1_lookahead_ackermann!20))
                ((_ to_fp 8 24) #x3e3851ec))))
(assert (not (fp.leq ((_ to_fp 8 24) agent0_pos_x_ackermann!2)
             (fp.sub roundNearestTiesToEven
                     ((_ to_fp 8 24) agent1_pos_x_ackermann!23)
                     ((_ to_fp 8 24) #x3e3851ec)))))
(assert (not (= ((_ extract 0 0) __soid__will_proceed_ackermann!22) #b1)))
(check-sat)
(exit)
